import pytest

from jarvis_core.config.schema import JarvisConfig
from jarvis_core.permissions.store import PermissionStore
from jarvis_core.storage.db import get_connection


@pytest.fixture
def config(tmp_path) -> JarvisConfig:
    return JarvisConfig(data_dir=str(tmp_path))


@pytest.fixture
def db_conn(config):
    conn = get_connection(config.resolved_db_path())
    yield conn
    conn.close()


@pytest.fixture
def permission_store(db_conn) -> PermissionStore:
    return PermissionStore(db_conn)
