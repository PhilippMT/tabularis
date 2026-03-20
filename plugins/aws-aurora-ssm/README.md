# Aurora PostgreSQL (SSM) Tabularis Plugin

This plugin adds a custom Tabularis driver that connects to **AWS Aurora PostgreSQL** through an **AWS Systems Manager Session Manager port-forwarding tunnel** via a jump host (managed instance).

It uses the local AWS CLI credentials resolution by default (environment variables / default profile / EC2 role, etc.) and optionally supports a specific `--profile`.

## What it does

- Starts (and reuses) an SSM tunnel using:
  - `aws ssm start-session`
  - document `AWS-StartPortForwardingSessionToRemoteHost`
- Forwards a local port to your Aurora endpoint and port.
- Connects to PostgreSQL via `pg8000` over `127.0.0.1:<forwarded-port>`.
- Implements Tabularis JSON-RPC methods for schema exploration, query execution, CRUD, views, routines, and SQL generation.

## Prerequisites

On your workstation:

1. AWS CLI v2 installed and authenticated.
2. Session Manager plugin installed.
3. Python 3.9+.
4. Python dependency:

   ```bash
   pip install -r requirements.txt
   ```

On AWS side:

1. A jump host EC2 managed by SSM (SSM Agent online).
2. IAM permissions for starting SSM sessions (`ssm:StartSession` etc.).
3. Jump host network path to your Aurora endpoint.
4. Aurora PostgreSQL credentials (username/password).

## Settings (Tabularis → Settings → gear icon on plugin)

- **SSM Target (instance ID)**: managed jump host instance ID (required)
- **AWS Region**: optional; blank uses AWS CLI defaults
- **AWS Profile**: optional; blank uses default AWS credential chain
- **SSM document**: defaults to `AWS-StartPortForwardingSessionToRemoteHost`
- **Preferred local tunnel port**: `0` = auto
- **Tunnel startup timeout**: seconds to wait for local port to open

## Connection form values in Tabularis

- **Host**: Aurora cluster/instance endpoint (e.g. `mydb.cluster-xxxx.us-east-1.rds.amazonaws.com`)
- **Port**: Aurora port (`5432` by default)
- **Database**: target database name
- **Username/Password**: PostgreSQL credentials

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

## Local plugin installation layout

Put this folder into your Tabularis plugins path, e.g. on Linux:

`~/.local/share/tabularis/plugins/aws-aurora-ssm/`

Ensure the script is executable on Linux/macOS:

```bash
chmod +x aurora-ssm-plugin.py
```

Folder should contain:

- `manifest.json`
- `aurora-ssm-plugin.py`
- `requirements.txt`

## Troubleshooting

- If tunnel startup fails, check Tabularis logs (plugin writes diagnostics to `stderr`).
- Validate manually:

  ```bash
  aws ssm start-session \
    --target <instance-id> \
    --document-name AWS-StartPortForwardingSessionToRemoteHost \
    --parameters '{"host":["<aurora-endpoint>"],"portNumber":["5432"],"localPortNumber":["15432"]}'
  ```

- If you use a custom profile, ensure it has both SSM access and network reachability assumptions.
