import pytest

from jarvis_core.permissions.capabilities import Capability
from jarvis_core.permissions.checker import PermissionDenied
from jarvis_core.voice.factory import build_listen_loop
from jarvis_core.voice.pipeline import ListenLoop


def test_build_listen_loop_denied_without_microphone_permission(config, permission_store, db_conn):
    with pytest.raises(PermissionDenied):
        build_listen_loop(config, permission_store, db_conn)


def test_build_listen_loop_denial_is_audited(config, permission_store, db_conn):
    with pytest.raises(PermissionDenied):
        build_listen_loop(config, permission_store, db_conn)

    rows = db_conn.execute(
        "SELECT * FROM audit_log WHERE detail LIKE '%MICROPHONE%'"
    ).fetchall()
    assert len(rows) == 1
    assert "granted=False" in rows[0]["detail"]


def test_build_listen_loop_succeeds_when_microphone_granted(config, permission_store, db_conn):
    permission_store.grant(Capability.MICROPHONE)

    loop = build_listen_loop(config, permission_store, db_conn)

    assert isinstance(loop, ListenLoop)
