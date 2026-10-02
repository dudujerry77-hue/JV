"""Grant (or revoke) a capability against Jarvis Core's permission store.

There is no admin UI yet (Mission Control is Phase 11) -- this is a
stopgap until one exists. It operates on the same SQLite database the
running service uses (resolved the same way jarvis_core.service.main
does, via load_config()), so it's safe to run against a live Core: the
running process will see the change on its next permission check.

Usage:
    python scripts/grant_permission.py AI_PROVIDER
    python scripts/grant_permission.py AI_PROVIDER --revoke
    python scripts/grant_permission.py --list
"""

import argparse
import sys

from jarvis_core.config.loader import load_config
from jarvis_core.permissions.capabilities import Capability
from jarvis_core.permissions.store import PermissionStore
from jarvis_core.storage.db import get_connection


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "capability", nargs="?", help="Capability name, e.g. AI_PROVIDER (see --list for all)"
    )
    parser.add_argument("--revoke", action="store_true", help="Revoke instead of grant")
    parser.add_argument(
        "--list", action="store_true", help="List all capabilities and their current state"
    )
    args = parser.parse_args()

    config = load_config()
    conn = get_connection(config.resolved_db_path())
    store = PermissionStore(conn)

    if args.list:
        for grant in store.list_grants():
            state = "GRANTED" if grant["granted"] else "denied"
            print(f"{grant['capability']:<20} {state:<10} tier={grant['tier']}")
        return 0

    if not args.capability:
        parser.print_usage()
        return 1

    try:
        capability = Capability(args.capability.upper())
    except ValueError:
        valid = ", ".join(c.value for c in Capability)
        print(f"Unknown capability {args.capability!r}. Valid: {valid}", file=sys.stderr)
        return 1

    if args.revoke:
        store.revoke(capability)
        print(f"Revoked {capability.value}")
    else:
        store.grant(capability)
        print(f"Granted {capability.value}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
