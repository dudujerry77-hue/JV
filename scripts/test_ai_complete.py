"""Send one test prompt to a running Jarvis Core's POST /ai/complete.

Requires: Core already running (python -m jarvis_core.service.main),
AI_PROVIDER permission already granted (see scripts/grant_permission.py),
and an Anthropic API key already stored in the OS keyring under
service "jarvis", key "anthropic_api_key" (see jarvis_core/secrets.py).

Usage:
    python scripts/test_ai_complete.py "Say hello in five words."
"""

import json
import sys
import urllib.request

from jarvis_core.config.loader import load_config


def main() -> int:
    prompt = " ".join(sys.argv[1:]) or "Say hello in exactly five words."
    config = load_config()
    url = f"http://{config.service.host}:{config.service.port}/ai/complete"

    body = json.dumps({"prompt": prompt}).encode("utf-8")
    request = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/json"}, method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        print(f"HTTP {exc.code}: {detail}", file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"Could not reach {url}: {exc}. Is Core running?", file=sys.stderr)
        return 1

    print(f"Model: {result['model']}")
    print(f"Usage: {result['usage']}")
    print(f"Response: {result['text']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
