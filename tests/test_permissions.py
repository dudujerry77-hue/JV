import pytest

from jarvis_core.permissions.capabilities import Capability, Tier, tier_of
from jarvis_core.permissions.checker import PermissionDenied, require


def test_deny_by_default(permission_store):
    assert permission_store.is_granted(Capability.CAMERA) is False


def test_grant_and_revoke(permission_store):
    permission_store.grant(Capability.NETWORK)
    assert permission_store.is_granted(Capability.NETWORK) is True

    permission_store.revoke(Capability.NETWORK)
    assert permission_store.is_granted(Capability.NETWORK) is False


def test_list_grants_covers_full_catalog(permission_store):
    grants = permission_store.list_grants()
    capability_names = {g["capability"] for g in grants}

    assert capability_names == {c.value for c in Capability}


def test_financial_action_is_financial_tier():
    assert tier_of(Capability.FINANCIAL_ACTION) == Tier.FINANCIAL


def test_network_is_standard_tier():
    assert tier_of(Capability.NETWORK) == Tier.STANDARD


def test_require_raises_when_not_granted(permission_store):
    with pytest.raises(PermissionDenied):
        require(permission_store, Capability.RUN_COMMAND)


def test_require_passes_when_granted(permission_store):
    permission_store.grant(Capability.RUN_COMMAND)
    require(permission_store, Capability.RUN_COMMAND)  # should not raise


def test_require_writes_audit_log_entry(permission_store, db_conn):
    permission_store.grant(Capability.NETWORK)
    require(permission_store, Capability.NETWORK, conn=db_conn)

    rows = db_conn.execute("SELECT * FROM audit_log").fetchall()
    assert len(rows) == 1
    assert rows[0]["event_type"] == "permission_check"
    assert "NETWORK" in rows[0]["detail"]
