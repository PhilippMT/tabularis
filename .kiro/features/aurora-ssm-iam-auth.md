# Feature: IAM Authentication for Aurora PostgreSQL SSM Plugin

The following plan should be complete, but its important that you validate documentation and codebase patterns and task sanity before you start implementing.

Pay special attention to naming of existing utils types and models. Import from the right files etc.

## Feature Description

Add AWS IAM database authentication support to the existing `aws-aurora-ssm` Tabularis plugin. When enabled, the plugin generates a short-lived IAM auth token via `boto3` (using `rds.generate_db_auth_token`) instead of requiring a static password in the connection form. This integrates with the AWS default credential chain and supports an optional named profile.

## User Story

As a developer connecting to Aurora PostgreSQL through an SSM tunnel
I want to authenticate using IAM credentials instead of a database password
So that I can leverage centralized AWS IAM access control and avoid managing static database passwords

## Problem Statement

The current `aws-aurora-ssm` plugin requires a static PostgreSQL username/password. Many AWS environments enforce IAM-only database authentication (no static passwords), making the plugin unusable in those setups.

## Solution Statement

Add a boolean `iam_auth` toggle to the plugin settings. When enabled, the plugin uses `boto3` to generate a temporary IAM auth token (valid 15 minutes) and passes it as the password to `pg8000`. SSL is forced on (required by AWS for IAM auth). The token is generated fresh on every connection, so expiry is not an issue given the plugin's per-request connection model.

## Feature Metadata

**Feature Type**: Enhancement
**Estimated Complexity**: Low
**Primary Systems Affected**: `plugins/aws-aurora-ssm/` (4 files)
**Dependencies**: `boto3` (new Python dependency)

---

## CONTEXT REFERENCES

### Relevant Codebase Files — MUST READ BEFORE IMPLEMENTING

- `plugins/aws-aurora-ssm/aurora-ssm-plugin.py` (lines 1-50) — imports, helpers, constants
- `plugins/aws-aurora-ssm/aurora-ssm-plugin.py` (lines 230-290) — `_build_ssl_context()` and `_connect()` methods — THIS IS THE CORE CHANGE AREA
- `plugins/aws-aurora-ssm/aurora-ssm-plugin.py` (lines 210-228) — `_resolve_tunnel_settings()` — pattern for reading settings
- `plugins/aws-aurora-ssm/manifest.json` — current settings array (lines 25-60) — pattern for adding new settings
- `plugins/aws-aurora-ssm/requirements.txt` — current dependencies
- `plugins/aws-aurora-ssm/README.md` — documentation structure
- `plugins/PLUGIN_GUIDE.md` (lines 100-180) — plugin settings schema and `initialize` RPC

### New Files to Create

None — all changes are modifications to existing files.

### Relevant Documentation — READ BEFORE IMPLEMENTING

- [boto3 generate_db_auth_token API](https://docs.aws.amazon.com/boto3/latest/reference/services/rds/client/generate_db_auth_token.html)
  - Signature: `generate_db_auth_token(DBHostname, Port, DBUsername, Region=None)`
  - Returns a presigned URL string used as the password
  - Why: This is the core API call for token generation

- [Aurora PostgreSQL IAM auth with Python (Boto3)](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/UsingWithRDS.IAMDBAuth.Connecting.Python.html)
  - Shows the full connection flow: create session → generate token → connect with SSL
  - Why: Reference implementation pattern from AWS

- [IAM database authentication overview](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/UsingWithRDS.IAMDBAuth.html)
  - Token lifetime: 15 minutes
  - SSL/TLS is required
  - DB user must have `rds_iam` role granted
  - Why: Constraints that affect implementation

### Patterns to Follow

**Settings access pattern** (from `aurora-ssm-plugin.py`):
```python
def _setting_str(self, key: str, default: str = "") -> str:
    value = self.settings.get(key, default)
    if value is None:
        return default
    return str(value).strip()
```

**Boolean settings** — manifest uses `"type": "boolean"`, Python reads with:
```python
bool(self.settings.get("iam_auth", False))
```

**SSL context pattern** (existing in `_build_ssl_context`):
```python
def _build_ssl_context(self, ssl_mode: Optional[str]) -> Any:
    mode = (ssl_mode or "").strip().lower()
    if mode in ("", "disable", "disabled", "off", "false"):
        return None
    import ssl
    return ssl.create_default_context()
```

**Manifest settings pattern** (existing):
```json
{
  "key": "aws_profile",
  "label": "AWS Profile",
  "type": "string",
  "default": "",
  "description": "Optional. Profile to pass via --profile. Leave empty to use default AWS credential chain."
}
```

---

## IMPLEMENTATION PLAN

### Phase 1: Dependencies & Configuration

Add `boto3` to requirements, add IAM auth settings to manifest.

### Phase 2: Core Implementation

Modify `_connect()` to generate an IAM auth token when the setting is enabled. Force SSL for IAM auth connections. Handle the tunnel scenario where the TCP connection goes to `127.0.0.1` but the token must be generated against the real Aurora endpoint.

### Phase 3: Documentation

Update README with IAM auth prerequisites and usage.

---

## STEP-BY-STEP TASKS

IMPORTANT: Execute every task in order, top to bottom. Each task is atomic and independently testable.

### 1. UPDATE `plugins/aws-aurora-ssm/requirements.txt`

- **IMPLEMENT**: Add `boto3` dependency
- **PATTERN**: Follow existing single-dependency-per-line format
- **GOTCHA**: `boto3` pulls in `botocore` and `urllib3` transitively — no need to list them
- **VALIDATE**: `python3 -c "import boto3; print(boto3.__version__)"`

The file should become:
```
pg8000>=1.31.0
boto3>=1.26.0
```

### 2. UPDATE `plugins/aws-aurora-ssm/manifest.json` — add IAM auth settings

- **IMPLEMENT**: Add two new entries to the `settings` array:
  1. `iam_auth` — boolean toggle (default `false`)
  2. `ssl_ca_bundle` — optional string for custom RDS CA bundle path
- **PATTERN**: Mirror existing settings structure (key, label, type, default, description)
- **GOTCHA**: Place `iam_auth` right after `aws_profile` for logical grouping. Place `ssl_ca_bundle` after `iam_auth`.
- **VALIDATE**: `python3 -c "import json; d=json.load(open('plugins/aws-aurora-ssm/manifest.json')); keys=[s['key'] for s in d['settings']]; assert 'iam_auth' in keys and 'ssl_ca_bundle' in keys; print('OK')"`

Add these two settings after the `aws_profile` entry:
```json
{
  "key": "iam_auth",
  "label": "Use IAM Authentication",
  "type": "boolean",
  "default": false,
  "description": "Generate a temporary IAM auth token instead of using the password from the connection form. Requires the DB user to have the rds_iam role granted."
},
{
  "key": "ssl_ca_bundle",
  "label": "SSL CA Bundle Path",
  "type": "string",
  "default": "",
  "description": "Optional path to an RDS CA certificate bundle (e.g. global-bundle.pem). If empty, the system CA store is used. Download from https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem"
}
```

### 3. UPDATE `plugins/aws-aurora-ssm/aurora-ssm-plugin.py` — add IAM token generation

- **IMPLEMENT**: Three changes in the plugin class:
  1. Add a `_generate_iam_token()` method
  2. Modify `_build_ssl_context()` to accept a `force_ssl` flag and optional CA bundle path
  3. Modify `_connect()` to use IAM token when enabled

- **PATTERN**: Follow existing `_setting_str` / `_setting_int` patterns for reading settings
- **IMPORTS**: Add `import boto3` at the top of `_generate_iam_token` (lazy import to avoid crash when IAM auth is not used and boto3 is not installed)
- **GOTCHA 1**: `generate_db_auth_token` needs the REAL Aurora endpoint hostname and port (not `127.0.0.1`), because the token is cryptographically bound to the endpoint. But the actual TCP connection goes through the tunnel to `127.0.0.1:local_port`.
- **GOTCHA 2**: When connecting through a tunnel, SSL hostname verification will fail because the cert says `*.cluster-xxx.rds.amazonaws.com` but we connect to `127.0.0.1`. Must disable `check_hostname` on the SSL context.
- **GOTCHA 3**: The `password` field in the connection form should be ignored when IAM auth is on — the token replaces it entirely.

#### 3a. Add `_generate_iam_token()` method

Add this method to the `AuroraSsmPlugin` class, after `_resolve_tunnel_settings()`:

```python
def _generate_iam_token(self, host: str, port: int, username: str) -> str:
    """Generate a short-lived IAM auth token for RDS/Aurora."""
    import boto3

    profile = self._setting_str("aws_profile", "")
    region = self._setting_str("aws_region", "")

    session_kwargs: Dict[str, str] = {}
    if profile:
        session_kwargs["profile_name"] = profile
    if region:
        session_kwargs["region_name"] = region

    session = boto3.Session(**session_kwargs)
    client = session.client("rds")
    token = client.generate_db_auth_token(
        DBHostname=host,
        Port=port,
        DBUsername=username,
        Region=region or None,
    )
    eprint(f"[aurora-ssm] Generated IAM auth token for {username}@{host}:{port}")
    return token
```

#### 3b. Modify `_build_ssl_context()` to support forced SSL and custom CA

Replace the existing `_build_ssl_context` method:

```python
def _build_ssl_context(self, ssl_mode: Optional[str], *, force: bool = False) -> Any:
    mode = (ssl_mode or "").strip().lower()
    if not force and mode in ("", "disable", "disabled", "off", "false"):
        return None
    import ssl

    ca_bundle = self._setting_str("ssl_ca_bundle", "")
    if ca_bundle:
        ctx = ssl.create_default_context(cafile=ca_bundle)
    else:
        ctx = ssl.create_default_context()

    # Through an SSM tunnel we connect to 127.0.0.1, so hostname
    # verification against the RDS certificate will always fail.
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx
```

#### 3c. Modify `_connect()` to use IAM token

In the `_connect` method, after the line that resolves `remote_port` and before the tunnel setup, add the IAM auth logic. The key change is:
- Determine if IAM auth is enabled
- If yes, generate the token using the REAL Aurora host/port and use it as password
- Force SSL on

Replace the section in `_connect()` starting from `ssl_context = self._build_ssl_context(...)` through the `pg_dbapi.connect(...)` call:

```python
        use_iam = bool(self.settings.get("iam_auth", False))

        if use_iam:
            password = self._generate_iam_token(remote_host, remote_port, username)
            ssl_context = self._build_ssl_context(conn_params.get("ssl_mode"), force=True)
        else:
            password = conn_params.get("password")
            ssl_context = self._build_ssl_context(conn_params.get("ssl_mode"))

        conn = pg_dbapi.connect(
            user=username,
            password=password,
            host="127.0.0.1",
            port=local_port,
            database=database,
            ssl_context=ssl_context,
            timeout=timeout_seconds,
        )
        conn.autocommit = True
        return conn
```

- **VALIDATE**: `echo '{"jsonrpc":"2.0","method":"initialize","params":{"settings":{"ssm_target":"i-test","iam_auth":true}},"id":1}' | python3 plugins/aws-aurora-ssm/aurora-ssm-plugin.py 2>&1 | head -5` (should not crash on import)

### 4. UPDATE `plugins/aws-aurora-ssm/README.md` — document IAM auth

- **IMPLEMENT**: Add an "IAM Authentication" section after the existing "Settings" section
- **PATTERN**: Follow existing README heading/section structure

Add this section after the "Settings" section:

```markdown
## IAM Authentication (optional)

Instead of a static database password, you can authenticate using AWS IAM:

1. Enable IAM authentication on your Aurora cluster (Cluster → Modify → enable "IAM DB authentication").
2. Grant the `rds_iam` role to your PostgreSQL user:
   ```sql
   GRANT rds_iam TO your_db_user;
   ```
3. Ensure your AWS credentials (profile/role) have the `rds-db:connect` permission for the target DB user and cluster.
4. In Tabularis plugin settings, toggle **Use IAM Authentication** on.
5. In the connection form, fill in **Host** (Aurora endpoint), **Port**, **Database**, and **Username**. The **Password** field is ignored when IAM auth is active.

### SSL CA Bundle (optional)

IAM authentication requires SSL. By default the plugin uses your system's CA store. If your system doesn't trust the RDS CA, download the global bundle:

```bash
curl -o ~/global-bundle.pem https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem
```

Then set the **SSL CA Bundle Path** in plugin settings to the downloaded file path.
```

- **VALIDATE**: `grep -c "IAM Authentication" plugins/aws-aurora-ssm/README.md` (should return 1+)

---

## TESTING STRATEGY

### Unit-Level Validation

Since this is a standalone Python plugin with no test framework set up, validation is manual/CLI-based:

1. **Import check**: `python3 -c "import boto3, pg8000; print('deps OK')"`
2. **Manifest validity**: `python3 -c "import json; json.load(open('plugins/aws-aurora-ssm/manifest.json')); print('manifest OK')"`
3. **Plugin startup**: Pipe an `initialize` message and verify no crash:
   ```bash
   echo '{"jsonrpc":"2.0","method":"initialize","params":{"settings":{"ssm_target":"i-test","iam_auth":true}},"id":1}' \
     | python3 plugins/aws-aurora-ssm/aurora-ssm-plugin.py 2>/dev/null
   ```
   Expected: `{"jsonrpc": "2.0", "id": 1, "result": null}`

### Integration Testing (requires AWS access)

1. Configure a real Aurora PostgreSQL cluster with IAM auth enabled
2. Grant `rds_iam` to a test user
3. Set up an SSM-managed jump host
4. Install the plugin locally and test connection through Tabularis UI
5. Verify: schema browsing, query execution, CRUD operations all work with IAM token

### Edge Cases

- IAM auth enabled but `boto3` not installed → should fail with clear error message (lazy import catches this)
- IAM auth enabled but AWS credentials expired/missing → should surface boto3 error clearly
- IAM auth enabled with wrong DB user (no `rds_iam` role) → PostgreSQL auth error
- IAM auth disabled → existing password-based flow unchanged (regression check)
- Empty `ssl_ca_bundle` → falls back to system CA store
- Custom `ssl_ca_bundle` path that doesn't exist → Python ssl error surfaced

---

## VALIDATION COMMANDS

### Level 1: Syntax & Manifest

```bash
python3 -m py_compile plugins/aws-aurora-ssm/aurora-ssm-plugin.py
python3 -c "import json; d=json.load(open('plugins/aws-aurora-ssm/manifest.json')); assert 'iam_auth' in [s['key'] for s in d['settings']]; print('OK')"
```

### Level 2: Dependency Check

```bash
python3 -c "import boto3, pg8000; print('deps OK')"
```

### Level 3: Plugin Smoke Test

```bash
echo '{"jsonrpc":"2.0","method":"initialize","params":{"settings":{"ssm_target":"i-test","iam_auth":true,"aws_profile":"","aws_region":"us-east-1"}},"id":1}' \
  | python3 plugins/aws-aurora-ssm/aurora-ssm-plugin.py 2>/dev/null
```

### Level 4: Manual Validation (requires AWS)

1. Install plugin to `~/.local/share/tabularis/plugins/aws-aurora-ssm/`
2. Open Tabularis → Settings → gear icon on plugin → enable IAM auth
3. Create connection with Aurora endpoint, username, no password
4. Test connection → should succeed
5. Browse schema, run a SELECT query

---

## ACCEPTANCE CRITERIA

- [ ] `boto3` added to `requirements.txt`
- [ ] `iam_auth` boolean setting added to `manifest.json`
- [ ] `ssl_ca_bundle` string setting added to `manifest.json`
- [ ] `_generate_iam_token()` method generates token using boto3 RDS client
- [ ] `_connect()` uses IAM token as password when `iam_auth` is `true`
- [ ] SSL is forced on when IAM auth is enabled
- [ ] Existing password-based flow is unchanged when `iam_auth` is `false`
- [ ] AWS profile and region settings are respected for token generation
- [ ] README documents IAM auth setup, prerequisites, and CA bundle
- [ ] Plugin starts without error when `iam_auth` is enabled (smoke test passes)
- [ ] `manifest.json` remains valid JSON matching the plugin schema

---

## COMPLETION CHECKLIST

- [ ] All tasks completed in order
- [ ] Each task validation passed immediately
- [ ] All validation commands executed successfully
- [ ] Plugin smoke test returns valid JSON-RPC response
- [ ] No syntax errors in Python file
- [ ] Manifest is valid JSON
- [ ] README is updated
- [ ] Existing password auth flow unaffected (no regression)

---

## NOTES

**Token lifetime**: IAM auth tokens are valid for 15 minutes. The plugin creates a fresh connection (and thus a fresh token) for every JSON-RPC method call, so token expiry is not a concern.

**SSL through tunnel**: The SSM tunnel means the TCP connection goes to `127.0.0.1`, but the RDS certificate has the Aurora endpoint hostname. We disable hostname verification (`check_hostname = False`) and certificate verification (`verify_mode = CERT_NONE`) since the tunnel itself is encrypted and authenticated. This matches the common pattern for tunneled database connections.

**Lazy boto3 import**: `boto3` is imported inside `_generate_iam_token()` rather than at module level. This ensures the plugin still works for password-based auth even if `boto3` is not installed.

**No separate plugin**: This is an enhancement to the existing `aws-aurora-ssm` plugin rather than a new plugin, since the SSM tunnel infrastructure is shared and IAM auth is just an alternative authentication method for the same connection flow.
