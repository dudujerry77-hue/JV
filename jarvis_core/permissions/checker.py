"""Enforcement + audit trail for capability checks.

Every check is logged -- granted or denied -- so the owner can always
answer "what did Jarvis try to do, and under what permission?" per
.jarvis/observability_spec.md and .jarvis/permissions_model.md
"Auditability".
"""

import sqlite3
from datetime import UTC, datetime

from jarvis_core.observability.logging import get_logger
from jarvis_core.permissions.capabilities import Capability
from jarvis_core.permissions.store import PermissionStore

logger = get_logger("permissions")


class PermissionDenied(Exception):
    def __init__(self, capability: Capability):
        self.capability = capability
        super().__init__(f"Capability not granted: {capability.value}")


def _record_audit(conn: sqlite3.Connection, capability: Capability, granted: bool) -> None:
    conn.execute(
        "INSERT INTO audit_log (timestamp, event_type, detail) VALUES (?, ?, ?)",
        (
            datetime.now(UTC).isoformat(),
            "permission_check",
            f"capability={capability.value} granted={granted}",
        ),
    )
    conn.commit()


def require(
    store: PermissionStore,
    capability: Capability,
    conn: sqlite3.Connection | None = None,
) -> None:
    """Raise PermissionDenied if `capability` is not granted.

    Callers that want the check recorded in the durable audit log should
    pass the same sqlite connection the store is backed by.
    """
    granted = store.is_granted(capability)

    if conn is not None:
        _record_audit(conn, capability, granted)

    if granted:
        logger.debug("permission check passed: %s", capability.value)
    else:
        logger.warning("permission check denied: %s", capability.value)
        raise PermissionDenied(capability)
