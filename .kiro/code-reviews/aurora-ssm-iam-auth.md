# Code Review: Aurora SSM IAM Auth

**Date**: 2026-03-20
**Scope**: `plugins/aws-aurora-ssm/` (4 new files)

**Stats:**

- Files Modified: 0 (tracked)
- Files Added: 4 (untracked — new plugin)
- Files Deleted: 0
- New lines: ~50 (IAM auth additions to existing plugin code)

---

## Issues

```
severity: medium
file: plugins/aws-aurora-ssm/aurora-ssm-plugin.py
line: 434-440
issue: ssl_ca_bundle setting is a no-op — CERT_NONE overrides CA verification
detail: When a user provides a CA bundle path, the code loads it via
  ssl.create_default_context(cafile=ca_bundle) but then unconditionally sets
  ctx.verify_mode = ssl.CERT_NONE, which disables all certificate verification.
  The CA bundle is loaded into memory but never used. A user who downloads the
  RDS global-bundle.pem and configures it expects certificate verification to
  actually happen (minus hostname checking, since we tunnel to 127.0.0.1).
suggestion: Only set CERT_NONE when no CA bundle is provided. When a CA bundle
  IS provided, keep verify_mode = CERT_REQUIRED (the default from
  create_default_context) so the server certificate is validated against the
  bundle. check_hostname = False is correct in both cases (tunnel scenario).

  Fixed _build_ssl_context:

    def _build_ssl_context(self, ssl_mode, *, force=False):
        mode = (ssl_mode or "").strip().lower()
        if not force and mode in ("", "disable", "disabled", "off", "false"):
            return None
        import ssl

        ca_bundle = self._setting_str("ssl_ca_bundle", "")
        if ca_bundle:
            ctx = ssl.create_default_context(cafile=ca_bundle)
        else:
            ctx = ssl.create_default_context()
            ctx.verify_mode = ssl.CERT_NONE

        # Through an SSM tunnel we connect to 127.0.0.1, so hostname
        # verification against the RDS certificate will always fail.
        ctx.check_hostname = False
        return ctx
```

---

No other issues found. Logic, security, naming, patterns, and documentation are all clean.
