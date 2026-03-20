#!/usr/bin/env python3
"""Tabularis plugin: AWS Aurora PostgreSQL over SSM jump-host port forwarding.

Protocol: JSON-RPC 2.0 over stdin/stdout (one JSON object per line).
"""

from __future__ import annotations

import atexit
import datetime as dt
import decimal
import json
import socket
import subprocess
import sys
import threading
import time
import traceback
import uuid
from collections import deque
from contextlib import closing
from dataclasses import dataclass, field
from typing import Any, Deque, Dict, List, Optional, Tuple

try:
    import pg8000.dbapi as pg_dbapi
except Exception as import_error:  # noqa: BLE001
    print(
        "[aurora-ssm] Missing Python dependency 'pg8000'. "
        "Install with: pip install -r requirements.txt",
        file=sys.stderr,
        flush=True,
    )
    raise import_error

JSONRPC = "2.0"


# -----------------------------
# Generic helpers
# -----------------------------

def eprint(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def quote_ident(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def normalize_database_selection(database: Any) -> str:
    if isinstance(database, list):
        return str(database[0]) if database else ""
    if database is None:
        return ""
    return str(database)


def strip_trailing_semicolon(sql: str) -> str:
    return sql.strip().rstrip(";").strip()


def is_select_like(sql: str) -> bool:
    upper = sql.lstrip().upper()
    return upper.startswith("SELECT") or upper.startswith("WITH")


def to_json_value(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool, dict, list)):
        return value
    if isinstance(value, decimal.Decimal):
        try:
            return int(value)
        except Exception:
            try:
                return float(value)
            except Exception:
                return str(value)
    if isinstance(value, (dt.date, dt.time, dt.datetime)):
        return value.isoformat()
    if isinstance(value, (bytes, bytearray, memoryview)):
        return "\\x" + bytes(value).hex()
    if isinstance(value, uuid.UUID):
        return str(value)
    return str(value)


# -----------------------------
# SSM tunnel handling
# -----------------------------

TunnelKey = Tuple[str, str, int, str, str, str]


@dataclass
class TunnelState:
    process: subprocess.Popen[str]
    local_port: int
    key: TunnelKey
    recent_output: Deque[str] = field(default_factory=lambda: deque(maxlen=40))
    stdout_thread: Optional[threading.Thread] = None
    stderr_thread: Optional[threading.Thread] = None

    def alive(self) -> bool:
        return self.process.poll() is None


class TunnelManager:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._tunnels: Dict[TunnelKey, TunnelState] = {}

    def shutdown_all(self) -> None:
        with self._lock:
            for state in list(self._tunnels.values()):
                self._terminate_tunnel(state)
            self._tunnels.clear()

    def ensure_tunnel(
        self,
        *,
        target: str,
        remote_host: str,
        remote_port: int,
        profile: str,
        region: str,
        document_name: str,
        preferred_local_port: int,
        timeout_seconds: int,
    ) -> int:
        key: TunnelKey = (
            target,
            remote_host,
            int(remote_port),
            profile or "",
            region or "",
            document_name,
        )

        with self._lock:
            existing = self._tunnels.get(key)
            if existing and existing.alive() and self._port_is_open(existing.local_port):
                return existing.local_port

            if existing:
                self._terminate_tunnel(existing)
                self._tunnels.pop(key, None)

            local_port = self._pick_local_port(preferred_local_port)
            state = self._start_tunnel(
                key=key,
                target=target,
                remote_host=remote_host,
                remote_port=remote_port,
                profile=profile,
                region=region,
                document_name=document_name,
                local_port=local_port,
            )

            try:
                self._wait_for_port(state, timeout_seconds)
            except Exception:
                self._terminate_tunnel(state)
                raise

            self._tunnels[key] = state
            return local_port

    def _start_tunnel(
        self,
        *,
        key: TunnelKey,
        target: str,
        remote_host: str,
        remote_port: int,
        profile: str,
        region: str,
        document_name: str,
        local_port: int,
    ) -> TunnelState:
        cmd = self._build_aws_command(
            target=target,
            remote_host=remote_host,
            remote_port=remote_port,
            local_port=local_port,
            profile=profile,
            region=region,
            document_name=document_name,
        )
        eprint(f"[aurora-ssm] Starting tunnel: {' '.join(cmd)}")

        process = subprocess.Popen(
            cmd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

        state = TunnelState(process=process, local_port=local_port, key=key)
        state.stdout_thread = self._spawn_pipe_reader(state, process.stdout, "stdout")
        state.stderr_thread = self._spawn_pipe_reader(state, process.stderr, "stderr")
        return state

    def _build_aws_command(
        self,
        *,
        target: str,
        remote_host: str,
        remote_port: int,
        local_port: int,
        profile: str,
        region: str,
        document_name: str,
    ) -> List[str]:
        params_json = json.dumps(
            {
                "host": [str(remote_host)],
                "portNumber": [str(remote_port)],
                "localPortNumber": [str(local_port)],
            }
        )

        cmd: List[str] = ["aws"]
        if profile:
            cmd.extend(["--profile", profile])
        if region:
            cmd.extend(["--region", region])
        cmd.extend(
            [
                "ssm",
                "start-session",
                "--target",
                target,
                "--document-name",
                document_name,
                "--parameters",
                params_json,
            ]
        )
        return cmd

    def _spawn_pipe_reader(
        self,
        state: TunnelState,
        pipe: Optional[Any],
        label: str,
    ) -> Optional[threading.Thread]:
        if pipe is None:
            return None

        def _read() -> None:
            try:
                for raw in iter(pipe.readline, ""):
                    line = raw.rstrip("\n")
                    if not line:
                        continue
                    msg = f"{label}: {line}"
                    state.recent_output.append(msg)
                    eprint(f"[aurora-ssm] {msg}")
            except Exception as exc:
                eprint(f"[aurora-ssm] Failed reading tunnel {label}: {exc}")
            finally:
                try:
                    pipe.close()
                except Exception:
                    pass

        t = threading.Thread(target=_read, daemon=True)
        t.start()
        return t

    def _pick_local_port(self, preferred: int) -> int:
        used_ports = {s.local_port for s in self._tunnels.values() if s.alive()}
        if preferred > 0 and preferred not in used_ports and self._port_bind_available(preferred):
            return preferred

        if preferred > 0:
            eprint(
                f"[aurora-ssm] Preferred local port {preferred} unavailable, using a random free port."
            )

        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            sock.bind(("127.0.0.1", 0))
            return int(sock.getsockname()[1])

    def _port_bind_available(self, port: int) -> bool:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(("127.0.0.1", int(port)))
                return True
            except OSError:
                return False

    def _port_is_open(self, port: int) -> bool:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            sock.settimeout(0.2)
            return sock.connect_ex(("127.0.0.1", int(port))) == 0

    def _wait_for_port(self, state: TunnelState, timeout_seconds: int) -> None:
        deadline = time.time() + max(2, timeout_seconds)
        while time.time() < deadline:
            if state.process.poll() is not None:
                logs = "\n".join(state.recent_output)
                raise RuntimeError(
                    "SSM tunnel process exited before forwarding became ready "
                    f"(exit={state.process.returncode}). Recent output:\n{logs}"
                )
            if self._port_is_open(state.local_port):
                eprint(f"[aurora-ssm] Tunnel ready on local port {state.local_port}.")
                return
            time.sleep(0.2)

        logs = "\n".join(state.recent_output)
        raise TimeoutError(
            f"Timed out waiting for local forwarded port {state.local_port} to open.\n{logs}"
        )

    def _terminate_tunnel(self, state: TunnelState) -> None:
        try:
            if state.process.poll() is None:
                state.process.terminate()
                try:
                    state.process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    state.process.kill()
        except Exception as exc:
            eprint(f"[aurora-ssm] Failed to terminate tunnel: {exc}")


# -----------------------------
# Plugin implementation
# -----------------------------


class AuroraSsmPlugin:
    def __init__(self) -> None:
        self.settings: Dict[str, Any] = {}
        self.tunnels = TunnelManager()
        atexit.register(self.shutdown)

    def shutdown(self) -> None:
        self.tunnels.shutdown_all()

    def initialize(self, settings: Optional[Dict[str, Any]]) -> None:
        self.settings = settings or {}
        masked = {
            k: ("***" if "password" in k.lower() or "secret" in k.lower() else v)
            for k, v in self.settings.items()
        }
        eprint(f"[aurora-ssm] initialize settings={masked}")

    # -------- settings helpers --------

    def _setting_str(self, key: str, default: str = "") -> str:
        value = self.settings.get(key, default)
        if value is None:
            return default
        return str(value).strip()

    def _setting_int(self, key: str, default: int) -> int:
        value = self.settings.get(key, default)
        try:
            return int(value)
        except Exception:
            return default

    def _resolve_tunnel_settings(self) -> Tuple[str, str, str, str, int, int]:
        target = self._setting_str("ssm_target", "")
        if not target:
            raise ValueError(
                "Plugin setting 'ssm_target' is required (jump host managed instance ID)."
            )

        region = self._setting_str("aws_region", "")
        profile = self._setting_str("aws_profile", "")
        document_name = self._setting_str(
            "ssm_document_name", "AWS-StartPortForwardingSessionToRemoteHost"
        )
        preferred_local_port = max(0, self._setting_int("local_port", 0))
        timeout_seconds = max(5, self._setting_int("connect_timeout_seconds", 20))

        return (
            target,
            region,
            profile,
            document_name,
            preferred_local_port,
            timeout_seconds,
        )

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

    # -------- DB connection helpers --------

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
            ctx.verify_mode = ssl.CERT_NONE

        # Through an SSM tunnel we connect to 127.0.0.1, so hostname
        # verification against the RDS certificate will always fail.
        ctx.check_hostname = False
        return ctx

    def _connect(
        self,
        conn_params: Dict[str, Any],
        database_override: Optional[str] = None,
    ) -> Any:
        remote_host = (conn_params.get("host") or "").strip()
        if not remote_host:
            raise ValueError("Connection host must be set to your Aurora endpoint.")

        username = (conn_params.get("username") or "").strip()
        if not username:
            raise ValueError("Connection username is required.")

        database = database_override or normalize_database_selection(conn_params.get("database"))
        if not database:
            raise ValueError("Connection database is required.")

        remote_port = int(conn_params.get("port") or 5432)

        (
            target,
            region,
            profile,
            document_name,
            preferred_local_port,
            timeout_seconds,
        ) = self._resolve_tunnel_settings()

        local_port = self.tunnels.ensure_tunnel(
            target=target,
            remote_host=remote_host,
            remote_port=remote_port,
            profile=profile,
            region=region,
            document_name=document_name,
            preferred_local_port=preferred_local_port,
            timeout_seconds=timeout_seconds,
        )

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

    def _connect_for_databases(self, conn_params: Dict[str, Any]) -> Any:
        candidates = [
            normalize_database_selection(conn_params.get("database")),
            "postgres",
            "template1",
        ]
        seen: set[str] = set()
        last_err: Optional[Exception] = None

        for db in candidates:
            if not db or db in seen:
                continue
            seen.add(db)
            try:
                return self._connect(conn_params, database_override=db)
            except Exception as exc:  # noqa: PERF203
                last_err = exc

        if last_err is not None:
            raise RuntimeError(f"Could not connect to list databases: {last_err}")
        raise RuntimeError("Could not connect to list databases.")

    @staticmethod
    def _apply_search_path(cur: Any, schema: Optional[str]) -> None:
        if schema:
            cur.execute(f"SET search_path TO {quote_ident(schema)}")

    # -------- introspection --------

    def test_connection(self, conn_params: Dict[str, Any]) -> Dict[str, bool]:
        with closing(self._connect(conn_params)):
            return {"success": True}

    def get_databases(self, conn_params: Dict[str, Any]) -> List[str]:
        with closing(self._connect_for_databases(conn_params)) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT datname FROM pg_database WHERE datistemplate = false ORDER BY datname"
                )
                return [str(row[0]) for row in cur.fetchall()]

    def get_schemas(self, conn_params: Dict[str, Any]) -> List[str]:
        with closing(self._connect(conn_params)) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT schema_name
                    FROM information_schema.schemata
                    WHERE schema_name NOT IN ('pg_catalog', 'information_schema', 'pg_toast')
                      AND schema_name NOT LIKE 'pg_temp_%'
                      AND schema_name NOT LIKE 'pg_toast_temp_%'
                    ORDER BY schema_name
                    """
                )
                return [str(row[0]) for row in cur.fetchall()]

    def get_tables(self, conn_params: Dict[str, Any], schema: Optional[str]) -> List[Dict[str, Any]]:
        schema_name = schema or "public"
        with closing(self._connect(conn_params)) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = %s AND table_type = 'BASE TABLE'
                    ORDER BY table_name
                    """,
                    (schema_name,),
                )
                return [{"name": str(row[0])} for row in cur.fetchall()]

    def get_columns(
        self,
        conn_params: Dict[str, Any],
        table_name: str,
        schema: Optional[str],
    ) -> List[Dict[str, Any]]:
        schema_name = schema or "public"
        query = """
            SELECT
                c.column_name,
                c.data_type,
                c.is_nullable,
                c.column_default,
                c.is_identity,
                c.character_maximum_length,
                (
                    SELECT COUNT(*)
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage kcu
                      ON tc.constraint_name = kcu.constraint_name
                     AND tc.table_schema = kcu.table_schema
                    WHERE tc.constraint_type = 'PRIMARY KEY'
                      AND tc.table_schema = c.table_schema
                      AND kcu.table_name = c.table_name
                      AND kcu.column_name = c.column_name
                ) > 0 AS is_pk
            FROM information_schema.columns c
            WHERE c.table_schema = %s AND c.table_name = %s
            ORDER BY c.ordinal_position
        """

        with closing(self._connect(conn_params)) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (schema_name, table_name))
                rows = cur.fetchall()

        result: List[Dict[str, Any]] = []
        for row in rows:
            (
                name,
                data_type,
                is_nullable,
                column_default,
                is_identity,
                char_len,
                is_pk,
            ) = row
            default_val = str(column_default) if column_default is not None else ""
            is_auto = str(is_identity).upper() == "YES" or "nextval" in default_val

            normalized_default: Optional[str] = None
            if (
                not is_auto
                and default_val
                and default_val.lower() != "null"
                and not default_val.startswith("NULL::")
            ):
                normalized_default = default_val

            result.append(
                {
                    "name": str(name),
                    "data_type": str(data_type),
                    "is_pk": bool(is_pk),
                    "is_nullable": str(is_nullable).upper() == "YES",
                    "is_auto_increment": is_auto,
                    "default_value": normalized_default,
                    "character_maximum_length": (
                        int(char_len) if char_len is not None else None
                    ),
                }
            )

        return result

    def get_foreign_keys(
        self,
        conn_params: Dict[str, Any],
        table_name: str,
        schema: Optional[str],
    ) -> List[Dict[str, Any]]:
        schema_name = schema or "public"
        query = """
            SELECT
                tc.constraint_name,
                kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name,
                rc.update_rule,
                rc.delete_rule
            FROM information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
             AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage AS ccu
              ON ccu.constraint_name = tc.constraint_name
             AND ccu.table_schema = tc.table_schema
            JOIN information_schema.referential_constraints AS rc
              ON rc.constraint_name = tc.constraint_name
             AND rc.constraint_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY'
              AND tc.table_schema = %s
              AND tc.table_name = %s
        """

        with closing(self._connect(conn_params)) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (schema_name, table_name))
                rows = cur.fetchall()

        return [
            {
                "name": str(r[0]),
                "column_name": str(r[1]),
                "ref_table": str(r[2]),
                "ref_column": str(r[3]),
                "on_update": str(r[4]) if r[4] is not None else None,
                "on_delete": str(r[5]) if r[5] is not None else None,
            }
            for r in rows
        ]

    def get_indexes(
        self,
        conn_params: Dict[str, Any],
        table_name: str,
        schema: Optional[str],
    ) -> List[Dict[str, Any]]:
        schema_name = schema or "public"
        query = """
            SELECT
                i.relname AS index_name,
                a.attname AS column_name,
                ix.indisunique AS is_unique,
                ix.indisprimary AS is_primary,
                array_position(ix.indkey, a.attnum) AS seq_in_index
            FROM pg_class t
            JOIN pg_namespace n ON t.relnamespace = n.oid
            JOIN pg_index ix ON t.oid = ix.indrelid
            JOIN pg_class i ON i.oid = ix.indexrelid
            JOIN pg_attribute a ON a.attrelid = t.oid AND a.attnum = ANY(ix.indkey)
            WHERE t.relkind = 'r'
              AND n.nspname = %s
              AND t.relname = %s
            ORDER BY t.relname, i.relname, seq_in_index
        """

        with closing(self._connect(conn_params)) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (schema_name, table_name))
                rows = cur.fetchall()

        return [
            {
                "name": str(r[0]),
                "column_name": str(r[1]),
                "is_unique": bool(r[2]),
                "is_primary": bool(r[3]),
                "seq_in_index": int(r[4] or 0),
            }
            for r in rows
        ]

    # -------- views --------

    def get_views(self, conn_params: Dict[str, Any], schema: Optional[str]) -> List[Dict[str, Any]]:
        schema_name = schema or "public"
        with closing(self._connect(conn_params)) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT viewname FROM pg_views WHERE schemaname = %s ORDER BY viewname",
                    (schema_name,),
                )
                return [{"name": str(r[0]), "definition": None} for r in cur.fetchall()]

    def get_view_definition(
        self,
        conn_params: Dict[str, Any],
        view_name: str,
        schema: Optional[str],
    ) -> str:
        schema_name = schema or "public"
        qualified = f"{quote_ident(schema_name)}.{quote_ident(view_name)}"

        with closing(self._connect(conn_params)) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT pg_get_viewdef(%s::regclass, true) AS definition",
                    (qualified,),
                )
                row = cur.fetchone()
                definition = str(row[0]) if row and row[0] is not None else ""

        return f"CREATE OR REPLACE VIEW {qualified} AS\n{definition}"

    def get_view_columns(
        self,
        conn_params: Dict[str, Any],
        view_name: str,
        schema: Optional[str],
    ) -> List[Dict[str, Any]]:
        return self.get_columns(conn_params, view_name, schema)

    def create_view(
        self,
        conn_params: Dict[str, Any],
        view_name: str,
        definition: str,
        schema: Optional[str],
    ) -> None:
        schema_name = schema or "public"
        sql = f"CREATE VIEW {quote_ident(schema_name)}.{quote_ident(view_name)} AS {definition}"
        with closing(self._connect(conn_params)) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)

    def alter_view(
        self,
        conn_params: Dict[str, Any],
        view_name: str,
        definition: str,
        schema: Optional[str],
    ) -> None:
        schema_name = schema or "public"
        sql = (
            f"CREATE OR REPLACE VIEW {quote_ident(schema_name)}.{quote_ident(view_name)} "
            f"AS {definition}"
        )
        with closing(self._connect(conn_params)) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)

    def drop_view(
        self,
        conn_params: Dict[str, Any],
        view_name: str,
        schema: Optional[str],
    ) -> None:
        schema_name = schema or "public"
        sql = f"DROP VIEW IF EXISTS {quote_ident(schema_name)}.{quote_ident(view_name)}"
        with closing(self._connect(conn_params)) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)

    # -------- routines --------

    def get_routines(
        self,
        conn_params: Dict[str, Any],
        schema: Optional[str],
    ) -> List[Dict[str, Any]]:
        schema_name = schema or "public"
        query = """
            SELECT proname, prokind
            FROM pg_proc
            WHERE pronamespace = (SELECT oid FROM pg_namespace WHERE nspname = %s)
              AND prokind IN ('f', 'p')
            ORDER BY proname
        """
        with closing(self._connect(conn_params)) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (schema_name,))
                rows = cur.fetchall()

        result: List[Dict[str, Any]] = []
        for name, prokind in rows:
            kind = "PROCEDURE" if str(prokind) == "p" else "FUNCTION"
            result.append({"name": str(name), "routine_type": kind, "definition": None})
        return result

    def get_routine_parameters(
        self,
        conn_params: Dict[str, Any],
        routine_name: str,
        schema: Optional[str],
    ) -> List[Dict[str, Any]]:
        schema_name = schema or "public"
        params_out: List[Dict[str, Any]] = []

        with closing(self._connect(conn_params)) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT data_type, routine_type
                    FROM information_schema.routines
                    WHERE routine_schema = %s AND routine_name = %s
                    LIMIT 1
                    """,
                    (schema_name, routine_name),
                )
                info = cur.fetchone()
                if info:
                    data_type, routine_type = info
                    if (
                        str(routine_type).upper() == "FUNCTION"
                        and str(data_type).lower() not in {"void", "trigger"}
                    ):
                        params_out.append(
                            {
                                "name": "",
                                "data_type": str(data_type),
                                "mode": "OUT",
                                "ordinal_position": 0,
                            }
                        )

                cur.execute(
                    """
                    SELECT p.parameter_name, p.data_type, p.parameter_mode, p.ordinal_position
                    FROM information_schema.parameters p
                    JOIN information_schema.routines r ON p.specific_name = r.specific_name
                    WHERE r.routine_schema = %s AND r.routine_name = %s
                    ORDER BY p.ordinal_position
                    """,
                    (schema_name, routine_name),
                )
                for row in cur.fetchall():
                    params_out.append(
                        {
                            "name": str(row[0] or ""),
                            "data_type": str(row[1] or ""),
                            "mode": str(row[2] or ""),
                            "ordinal_position": int(row[3] or 0),
                        }
                    )

        return params_out

    def get_routine_definition(
        self,
        conn_params: Dict[str, Any],
        routine_name: str,
        _routine_type: str,
        schema: Optional[str],
    ) -> str:
        schema_name = schema or "public"
        with closing(self._connect(conn_params)) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT pg_get_functiondef(p.oid) AS definition
                    FROM pg_proc p
                    JOIN pg_namespace n ON p.pronamespace = n.oid
                    WHERE n.nspname = %s AND p.proname = %s
                    LIMIT 1
                    """,
                    (schema_name, routine_name),
                )
                row = cur.fetchone()
                return str(row[0]) if row and row[0] is not None else ""

    # -------- query execution / CRUD --------

    def execute_query(
        self,
        conn_params: Dict[str, Any],
        query: str,
        limit: Optional[int],
        page: int,
        schema: Optional[str],
    ) -> Dict[str, Any]:
        sql = strip_trailing_semicolon(query)
        if not sql:
            return {
                "columns": [],
                "rows": [],
                "affected_rows": 0,
                "truncated": False,
                "pagination": None,
            }

        page = max(1, int(page or 1))
        limit_value = int(limit) if limit is not None else None
        if limit_value is not None and limit_value <= 0:
            limit_value = None

        is_select = is_select_like(sql)
        final_sql = sql
        if is_select and limit_value is not None:
            offset = (page - 1) * limit_value
            final_sql = (
                f"SELECT * FROM ({sql}) AS data_wrapper "
                f"LIMIT {limit_value + 1} OFFSET {offset}"
            )

        with closing(self._connect(conn_params)) as conn:
            with conn.cursor() as cur:
                self._apply_search_path(cur, schema)
                cur.execute(final_sql)

                # Statements that do not return rows
                if cur.description is None:
                    affected = int(cur.rowcount) if (cur.rowcount and cur.rowcount > 0) else 0
                    return {
                        "columns": [],
                        "rows": [],
                        "affected_rows": affected,
                        "truncated": False,
                        "pagination": None,
                    }

                columns = [str(d[0]) for d in cur.description]
                rows = [[to_json_value(v) for v in row] for row in cur.fetchall()]

                pagination: Optional[Dict[str, Any]] = None
                truncated = False
                affected_rows = 0

                if is_select and limit_value is not None:
                    has_more = len(rows) > limit_value
                    if has_more:
                        rows = rows[:limit_value]
                    truncated = has_more
                    pagination = {
                        "page": page,
                        "page_size": limit_value,
                        "total_rows": None,
                        "has_more": has_more,
                    }

                return {
                    "columns": columns,
                    "rows": rows,
                    "affected_rows": affected_rows,
                    "truncated": truncated,
                    "pagination": pagination,
                }

    def insert_record(
        self,
        conn_params: Dict[str, Any],
        table: str,
        data: Dict[str, Any],
        schema: Optional[str],
    ) -> int:
        schema_name = schema or "public"
        qualified = f"{quote_ident(schema_name)}.{quote_ident(table)}"

        with closing(self._connect(conn_params)) as conn:
            with conn.cursor() as cur:
                if not data:
                    cur.execute(f"INSERT INTO {qualified} DEFAULT VALUES")
                    return int(cur.rowcount or 0)

                columns = [quote_ident(str(col)) for col in data.keys()]
                placeholders = ", ".join(["%s"] * len(columns))
                values = [data[k] for k in data.keys()]

                sql = (
                    f"INSERT INTO {qualified} ({', '.join(columns)}) "
                    f"VALUES ({placeholders})"
                )
                cur.execute(sql, tuple(values))
                return int(cur.rowcount or 0)

    def update_record(
        self,
        conn_params: Dict[str, Any],
        table: str,
        pk_col: str,
        pk_val: Any,
        col_name: str,
        new_val: Any,
        schema: Optional[str],
    ) -> int:
        schema_name = schema or "public"
        qualified = f"{quote_ident(schema_name)}.{quote_ident(table)}"

        with closing(self._connect(conn_params)) as conn:
            with conn.cursor() as cur:
                if isinstance(new_val, str) and new_val == "__USE_DEFAULT__":
                    sql = (
                        f"UPDATE {qualified} SET {quote_ident(col_name)} = DEFAULT "
                        f"WHERE {quote_ident(pk_col)} = %s"
                    )
                    cur.execute(sql, (pk_val,))
                else:
                    sql = (
                        f"UPDATE {qualified} SET {quote_ident(col_name)} = %s "
                        f"WHERE {quote_ident(pk_col)} = %s"
                    )
                    cur.execute(sql, (new_val, pk_val))
                return int(cur.rowcount or 0)

    def delete_record(
        self,
        conn_params: Dict[str, Any],
        table: str,
        pk_col: str,
        pk_val: Any,
        schema: Optional[str],
    ) -> int:
        schema_name = schema or "public"
        qualified = f"{quote_ident(schema_name)}.{quote_ident(table)}"

        sql = f"DELETE FROM {qualified} WHERE {quote_ident(pk_col)} = %s"
        with closing(self._connect(conn_params)) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (pk_val,))
                return int(cur.rowcount or 0)

    # -------- SQL generation methods --------

    def get_create_table_sql(
        self,
        table_name: str,
        columns: List[Dict[str, Any]],
        schema: Optional[str],
    ) -> List[str]:
        schema_name = schema or "public"
        col_defs: List[str] = []
        pk_cols: List[str] = []

        for col in columns:
            col_name = str(col.get("name", "")).strip()
            if not col_name:
                continue

            data_type = str(col.get("data_type", "TEXT"))
            is_auto = bool(col.get("is_auto_increment", False))
            is_nullable = bool(col.get("is_nullable", True))
            is_pk = bool(col.get("is_pk", False))
            default_value = col.get("default_value")

            if is_auto:
                upper = data_type.upper()
                data_type = "BIGSERIAL" if "BIG" in upper else "SERIAL"

            clause = f"{quote_ident(col_name)} {data_type}"
            if not is_nullable and not is_auto:
                clause += " NOT NULL"
            if default_value not in (None, "") and not is_auto:
                clause += f" DEFAULT {default_value}"

            col_defs.append(clause)
            if is_pk:
                pk_cols.append(quote_ident(col_name))

        if pk_cols:
            col_defs.append(f"PRIMARY KEY ({', '.join(pk_cols)})")

        sql = (
            f"CREATE TABLE {quote_ident(schema_name)}.{quote_ident(table_name)} (\n"
            f"  {',\n  '.join(col_defs)}\n"
            ")"
        )
        return [sql]

    def get_add_column_sql(
        self,
        table: str,
        column: Dict[str, Any],
        schema: Optional[str],
    ) -> List[str]:
        schema_name = schema or "public"
        col_name = str(column.get("name", "")).strip()
        if not col_name:
            raise ValueError("Column name is required.")

        data_type = str(column.get("data_type", "TEXT"))
        is_auto = bool(column.get("is_auto_increment", False))
        is_nullable = bool(column.get("is_nullable", True))
        default_value = column.get("default_value")

        if is_auto:
            upper = data_type.upper()
            data_type = "BIGSERIAL" if "BIG" in upper else "SERIAL"

        sql = (
            f"ALTER TABLE {quote_ident(schema_name)}.{quote_ident(table)} "
            f"ADD COLUMN {quote_ident(col_name)} {data_type}"
        )
        if not is_nullable and not is_auto:
            sql += " NOT NULL"
        if default_value not in (None, "") and not is_auto:
            sql += f" DEFAULT {default_value}"

        return [sql]

    def get_alter_column_sql(
        self,
        table: str,
        old_column: Dict[str, Any],
        new_column: Dict[str, Any],
        schema: Optional[str],
    ) -> List[str]:
        schema_name = schema or "public"
        tbl = f"{quote_ident(schema_name)}.{quote_ident(table)}"

        old_name = str(old_column.get("name", ""))
        new_name = str(new_column.get("name", ""))

        stmts: List[str] = []

        if old_name and new_name and old_name != new_name:
            stmts.append(
                f"ALTER TABLE {tbl} RENAME COLUMN {quote_ident(old_name)} TO {quote_ident(new_name)}"
            )

        col_ref = quote_ident(new_name or old_name)

        old_type = str(old_column.get("data_type", ""))
        new_type = str(new_column.get("data_type", ""))
        if old_type and new_type and old_type != new_type:
            stmts.append(
                f"ALTER TABLE {tbl} ALTER COLUMN {col_ref} TYPE {new_type} USING {col_ref}::{new_type}"
            )

        if bool(old_column.get("is_nullable", True)) != bool(new_column.get("is_nullable", True)):
            if bool(new_column.get("is_nullable", True)):
                stmts.append(f"ALTER TABLE {tbl} ALTER COLUMN {col_ref} DROP NOT NULL")
            else:
                stmts.append(f"ALTER TABLE {tbl} ALTER COLUMN {col_ref} SET NOT NULL")

        old_default = old_column.get("default_value")
        new_default = new_column.get("default_value")
        if old_default != new_default:
            if new_default not in (None, ""):
                stmts.append(
                    f"ALTER TABLE {tbl} ALTER COLUMN {col_ref} SET DEFAULT {new_default}"
                )
            else:
                stmts.append(f"ALTER TABLE {tbl} ALTER COLUMN {col_ref} DROP DEFAULT")

        if not stmts:
            raise ValueError("No changes detected")

        return stmts

    def get_create_index_sql(
        self,
        table: str,
        index_name: str,
        columns: List[str],
        is_unique: bool,
        schema: Optional[str],
    ) -> List[str]:
        schema_name = schema or "public"
        unique = "UNIQUE " if is_unique else ""
        col_sql = ", ".join(quote_ident(c) for c in columns)
        sql = (
            f"CREATE {unique}INDEX {quote_ident(index_name)} "
            f"ON {quote_ident(schema_name)}.{quote_ident(table)} ({col_sql})"
        )
        return [sql]

    def get_create_foreign_key_sql(
        self,
        table: str,
        fk_name: str,
        column: str,
        ref_table: str,
        ref_column: str,
        on_delete: Optional[str],
        on_update: Optional[str],
        schema: Optional[str],
    ) -> List[str]:
        schema_name = schema or "public"
        sql = (
            f"ALTER TABLE {quote_ident(schema_name)}.{quote_ident(table)} "
            f"ADD CONSTRAINT {quote_ident(fk_name)} "
            f"FOREIGN KEY ({quote_ident(column)}) "
            f"REFERENCES {quote_ident(schema_name)}.{quote_ident(ref_table)} ({quote_ident(ref_column)})"
        )
        if on_delete:
            sql += f" ON DELETE {on_delete}"
        if on_update:
            sql += f" ON UPDATE {on_update}"
        return [sql]

    def drop_index(
        self,
        conn_params: Dict[str, Any],
        index_name: str,
        schema: Optional[str],
    ) -> None:
        schema_name = schema or "public"
        sql = f"DROP INDEX {quote_ident(schema_name)}.{quote_ident(index_name)}"
        with closing(self._connect(conn_params)) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)

    def drop_foreign_key(
        self,
        conn_params: Dict[str, Any],
        table: str,
        fk_name: str,
        schema: Optional[str],
    ) -> None:
        schema_name = schema or "public"
        sql = (
            f"ALTER TABLE {quote_ident(schema_name)}.{quote_ident(table)} "
            f"DROP CONSTRAINT {quote_ident(fk_name)}"
        )
        with closing(self._connect(conn_params)) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)

    # -------- batch methods --------

    def _get_all_columns_batch_with_conn(
        self,
        cur: Any,
        schema_name: str,
    ) -> Dict[str, List[Dict[str, Any]]]:
        query = """
            SELECT
                c.table_name,
                c.column_name,
                c.data_type,
                c.is_nullable,
                c.column_default,
                c.is_identity,
                c.character_maximum_length,
                (
                    SELECT COUNT(*)
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage kcu
                      ON tc.constraint_name = kcu.constraint_name
                     AND tc.table_schema = kcu.table_schema
                    WHERE tc.constraint_type = 'PRIMARY KEY'
                      AND tc.table_schema = c.table_schema
                      AND kcu.table_name = c.table_name
                      AND kcu.column_name = c.column_name
                ) > 0 AS is_pk
            FROM information_schema.columns c
            WHERE c.table_schema = %s
            ORDER BY c.table_name, c.ordinal_position
        """
        cur.execute(query, (schema_name,))

        out: Dict[str, List[Dict[str, Any]]] = {}
        for row in cur.fetchall():
            (
                table_name,
                column_name,
                data_type,
                is_nullable,
                column_default,
                is_identity,
                char_len,
                is_pk,
            ) = row
            default_val = str(column_default) if column_default is not None else ""
            is_auto = str(is_identity).upper() == "YES" or "nextval" in default_val

            normalized_default: Optional[str] = None
            if (
                not is_auto
                and default_val
                and default_val.lower() != "null"
                and not default_val.startswith("NULL::")
            ):
                normalized_default = default_val

            out.setdefault(str(table_name), []).append(
                {
                    "name": str(column_name),
                    "data_type": str(data_type),
                    "is_pk": bool(is_pk),
                    "is_nullable": str(is_nullable).upper() == "YES",
                    "is_auto_increment": is_auto,
                    "default_value": normalized_default,
                    "character_maximum_length": (
                        int(char_len) if char_len is not None else None
                    ),
                }
            )
        return out

    def _get_all_foreign_keys_batch_with_conn(
        self,
        cur: Any,
        schema_name: str,
    ) -> Dict[str, List[Dict[str, Any]]]:
        query = """
            SELECT
                tc.table_name,
                tc.constraint_name,
                kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name,
                rc.update_rule,
                rc.delete_rule
            FROM information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
             AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage AS ccu
              ON ccu.constraint_name = tc.constraint_name
             AND ccu.table_schema = tc.table_schema
            JOIN information_schema.referential_constraints AS rc
              ON rc.constraint_name = tc.constraint_name
             AND rc.constraint_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY'
              AND tc.table_schema = %s
        """
        cur.execute(query, (schema_name,))

        out: Dict[str, List[Dict[str, Any]]] = {}
        for row in cur.fetchall():
            table_name, constraint_name, column_name, ref_table, ref_column, on_update, on_delete = (
                row
            )
            out.setdefault(str(table_name), []).append(
                {
                    "name": str(constraint_name),
                    "column_name": str(column_name),
                    "ref_table": str(ref_table),
                    "ref_column": str(ref_column),
                    "on_update": str(on_update) if on_update is not None else None,
                    "on_delete": str(on_delete) if on_delete is not None else None,
                }
            )
        return out

    def get_all_columns_batch(
        self,
        conn_params: Dict[str, Any],
        schema: Optional[str],
    ) -> Dict[str, List[Dict[str, Any]]]:
        schema_name = schema or "public"
        with closing(self._connect(conn_params)) as conn:
            with conn.cursor() as cur:
                return self._get_all_columns_batch_with_conn(cur, schema_name)

    def get_all_foreign_keys_batch(
        self,
        conn_params: Dict[str, Any],
        schema: Optional[str],
    ) -> Dict[str, List[Dict[str, Any]]]:
        schema_name = schema or "public"
        with closing(self._connect(conn_params)) as conn:
            with conn.cursor() as cur:
                return self._get_all_foreign_keys_batch_with_conn(cur, schema_name)

    def get_schema_snapshot(
        self,
        conn_params: Dict[str, Any],
        schema: Optional[str],
    ) -> List[Dict[str, Any]]:
        schema_name = schema or "public"
        with closing(self._connect(conn_params)) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = %s AND table_type = 'BASE TABLE'
                    ORDER BY table_name
                    """,
                    (schema_name,),
                )
                table_names = [str(r[0]) for r in cur.fetchall()]

                columns_map = self._get_all_columns_batch_with_conn(cur, schema_name)
                fks_map = self._get_all_foreign_keys_batch_with_conn(cur, schema_name)

        return [
            {
                "name": table,
                "columns": columns_map.get(table, []),
                "foreign_keys": fks_map.get(table, []),
            }
            for table in table_names
        ]

    # -------- dispatch --------

    def handle(self, method: str, params: Dict[str, Any]) -> Any:
        if method == "initialize":
            self.initialize(params.get("settings", {}))
            return None

        conn_params = params.get("params") or {}

        if method == "test_connection":
            return self.test_connection(conn_params)
        if method == "get_databases":
            return self.get_databases(conn_params)
        if method == "get_schemas":
            return self.get_schemas(conn_params)
        if method == "get_tables":
            return self.get_tables(conn_params, params.get("schema"))
        if method == "get_columns":
            return self.get_columns(conn_params, params["table"], params.get("schema"))
        if method == "get_foreign_keys":
            return self.get_foreign_keys(conn_params, params["table"], params.get("schema"))
        if method == "get_indexes":
            return self.get_indexes(conn_params, params["table"], params.get("schema"))

        if method == "get_views":
            return self.get_views(conn_params, params.get("schema"))
        if method == "get_view_definition":
            return self.get_view_definition(conn_params, params["view_name"], params.get("schema"))
        if method == "get_view_columns":
            return self.get_view_columns(conn_params, params["view_name"], params.get("schema"))
        if method == "create_view":
            self.create_view(
                conn_params,
                params["view_name"],
                params["definition"],
                params.get("schema"),
            )
            return None
        if method == "alter_view":
            self.alter_view(
                conn_params,
                params["view_name"],
                params["definition"],
                params.get("schema"),
            )
            return None
        if method == "drop_view":
            self.drop_view(conn_params, params["view_name"], params.get("schema"))
            return None

        if method == "get_routines":
            return self.get_routines(conn_params, params.get("schema"))
        if method == "get_routine_parameters":
            return self.get_routine_parameters(
                conn_params,
                params["routine_name"],
                params.get("schema"),
            )
        if method == "get_routine_definition":
            return self.get_routine_definition(
                conn_params,
                params["routine_name"],
                params.get("routine_type", ""),
                params.get("schema"),
            )

        if method == "execute_query":
            return self.execute_query(
                conn_params,
                params.get("query", ""),
                params.get("limit"),
                int(params.get("page", 1)),
                params.get("schema"),
            )
        if method == "insert_record":
            return self.insert_record(
                conn_params,
                params["table"],
                params.get("data", {}),
                params.get("schema"),
            )
        if method == "update_record":
            return self.update_record(
                conn_params,
                params["table"],
                params["pk_col"],
                params.get("pk_val"),
                params["col_name"],
                params.get("new_val"),
                params.get("schema"),
            )
        if method == "delete_record":
            return self.delete_record(
                conn_params,
                params["table"],
                params["pk_col"],
                params.get("pk_val"),
                params.get("schema"),
            )

        if method == "get_create_table_sql":
            return self.get_create_table_sql(
                params["table_name"],
                params.get("columns", []),
                params.get("schema"),
            )
        if method == "get_add_column_sql":
            return self.get_add_column_sql(
                params["table"],
                params["column"],
                params.get("schema"),
            )
        if method == "get_alter_column_sql":
            return self.get_alter_column_sql(
                params["table"],
                params["old_column"],
                params["new_column"],
                params.get("schema"),
            )
        if method == "get_create_index_sql":
            return self.get_create_index_sql(
                params["table"],
                params["index_name"],
                params.get("columns", []),
                bool(params.get("is_unique", False)),
                params.get("schema"),
            )
        if method == "get_create_foreign_key_sql":
            return self.get_create_foreign_key_sql(
                params["table"],
                params["fk_name"],
                params["column"],
                params["ref_table"],
                params["ref_column"],
                params.get("on_delete"),
                params.get("on_update"),
                params.get("schema"),
            )
        if method == "drop_index":
            self.drop_index(conn_params, params["index_name"], params.get("schema"))
            return None
        if method == "drop_foreign_key":
            self.drop_foreign_key(
                conn_params,
                params["table"],
                params["fk_name"],
                params.get("schema"),
            )
            return None

        if method == "get_all_columns_batch":
            return self.get_all_columns_batch(conn_params, params.get("schema"))
        if method == "get_all_foreign_keys_batch":
            return self.get_all_foreign_keys_batch(conn_params, params.get("schema"))
        if method == "get_schema_snapshot":
            return self.get_schema_snapshot(conn_params, params.get("schema"))

        raise NotImplementedError(f"Method '{method}' not implemented")


# -----------------------------
# JSON-RPC loop
# -----------------------------

def send_response(req_id: Any, result: Any = None) -> None:
    payload = {"jsonrpc": JSONRPC, "id": req_id, "result": result}
    sys.stdout.write(json.dumps(payload, default=to_json_value) + "\n")
    sys.stdout.flush()


def send_error(req_id: Any, code: int, message: str) -> None:
    payload = {
        "jsonrpc": JSONRPC,
        "id": req_id,
        "error": {
            "code": code,
            "message": message,
        },
    }
    sys.stdout.write(json.dumps(payload) + "\n")
    sys.stdout.flush()


def main() -> None:
    plugin = AuroraSsmPlugin()

    for raw in sys.stdin:
        line = raw.strip()
        if not line:
            continue

        try:
            req = json.loads(line)
        except Exception as exc:
            send_error(None, -32700, f"Parse error: {exc}")
            continue

        req_id = req.get("id")

        try:
            method = req.get("method")
            if not isinstance(method, str) or not method:
                raise ValueError("Missing or invalid 'method'")

            params = req.get("params") or {}
            if not isinstance(params, dict):
                raise ValueError("'params' must be an object")

            result = plugin.handle(method, params)
            send_response(req_id, result)

        except NotImplementedError as exc:
            send_error(req_id, -32601, str(exc))
        except (KeyError, TypeError, ValueError) as exc:
            send_error(req_id, -32602, f"Invalid params: {exc}")
        except Exception as exc:  # noqa: BLE001
            traceback.print_exc(file=sys.stderr)
            send_error(req_id, -32603, f"Internal error: {exc}")


if __name__ == "__main__":
    main()
