"""Deny-by-default permission store, backed by SQLite.

Enforcement authority lives here, not with whoever is asking -- see
.jarvis/security_policy.md "Safe plugin loading": a plugin or agent
declaring it wants a capability does not mean it has it.
"""

import sqlite3
from datetime import UTC, datetime

from jarvis_core.permissions.capabilities import Capability, tier_of


class PermissionStore:
    def __init__(self, conn: sqlite3.Connection):
        self._conn = conn
        self._seed_defaults()

    def _seed_defaults(self) -> None:
        now = datetime.now(UTC).isoformat()
        for capability in Capability:
            self._conn.execute(
                """
                INSERT OR IGNORE INTO permission_grants
                    (capability, granted, tier, updated_at)
                VALUES (?, 0, ?, ?)
                """,
                (capability.value, tier_of(capability).value, now),
            )
        self._conn.commit()

    def is_granted(self, capability: Capability) -> bool:
        row = self._conn.execute(
            "SELECT granted FROM permission_grants WHERE capability = ?",
            (capability.value,),
        ).fetchone()
        return bool(row and row["granted"])

    def grant(self, capability: Capability) -> None:
        self._set(capability, granted=True)

    def revoke(self, capability: Capability) -> None:
        self._set(capability, granted=False)

    def _set(self, capability: Capability, *, granted: bool) -> None:
        now = datetime.now(UTC).isoformat()
        self._conn.execute(
            """
            UPDATE permission_grants
            SET granted = ?, updated_at = ?
            WHERE capability = ?
            """,
            (int(granted), now, capability.value),
        )
        self._conn.commit()

    def list_grants(self) -> list[dict]:
        rows = self._conn.execute(
            "SELECT capability, granted, tier, updated_at FROM permission_grants"
        ).fetchall()
        return [dict(row) for row in rows]
