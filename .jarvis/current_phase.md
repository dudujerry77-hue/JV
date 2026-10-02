# Current Phase

Phase: **Phase 3 — Multi-AI Brain**
Status: `in_progress`
Last updated: 2026-10-02

Phase 1 — Foundation is `complete` (see
`phase_completion_records/P001-completion.md`). Per `roadmap.md`'s "Notes"
(phases are a planning sequence, not a strict waterfall), the owner chose
to move to Phase 3 next rather than Phase 2 (Voice), so Jarvis has a real
capability to exercise the Foundation layer against before building a
voice interface on top of it.

## Decided for This Phase

- First concrete AI provider: **Anthropic** (D-0015).
- Monthly AI cost ceiling: **$20 USD**, configurable, enforced by the
  router rather than advisory (D-0016).
- Default model: `claude-sonnet-5-5`, configurable via `ai.model`.

## What Exists So Far (first increment, implemented 2026-10-02)

`jarvis_core/ai/` — provider abstraction, `AnthropicProvider`, cost
tracking against the configured ceiling, and `AIRouter.complete(prompt)`
enforcing the `AI_PROVIDER` permission gate + ceiling + audit logging
(metadata only, never prompt/response content). Exposed via
`POST /ai/complete` on Core's local HTTP API. Credentials come from the
OS keyring (D-0012), looked up lazily — Core starts fine with no API key
configured; the endpoint simply isn't usable until one is set. See
`ai_provider_spec.md`'s "Phase 3 First Increment" section for the full
list of what this does and does not cover yet.

12 new tests added (`tests/test_ai.py`, plus new cases in
`tests/test_service.py`); full suite verified passing, 36/36, this
session.

## Explicitly Not Yet Done (this phase is not complete)

- Intent analysis, task classification, and real model/tool selection —
  the router currently always uses the one configured model.
- A second concrete provider / real fallback between providers (D-0007's
  abstraction supports this; nothing beyond Anthropic has been built).
- Local models (D-0006's local tier — wake word, STT, embeddings — is
  Phase 2/5 territory, not this increment).
- A formal security review of this increment specifically (Phase 1's
  review in `phase_completion_records/P001-completion.md` predates this
  code).
- A `phase_completion_records/P003-completion.md` — not created yet;
  `roadmap.md`'s completion bar (Implementation + Tests + Integration +
  Documentation + Security review + Verification) is not fully met until
  the above are addressed.
- No real end-to-end call to the Anthropic API has been made in this
  environment (no API key configured here, and none should be added to
  this repo or committed) — verification so far is unit-level with an
  injected fake client (`tests/test_ai.py`) plus a build-and-boot smoke
  test confirming the service wires up correctly with no key present.

## Hardening Done After Real-Server Testing (2026-10-02)

Running the actual service end-to-end (not just unit tests) surfaced a
real bug: a keyring backend failure (no backend installed, or a locked
vault) raised an uncaught `keyring.errors.KeyringError` straight through
`AnthropicProvider`, past the `AIProviderError` handling in
`service/app.py`, producing a raw HTTP 500 with a stack trace instead of
the intended clean 502. Fixed by wrapping all `keyring` calls in
`jarvis_core/secrets.py` and translating the failure into
`AIProviderError` in `anthropic_provider.py`. Regression tests added
(`tests/test_secrets.py`, plus new cases in `tests/test_ai.py` and
`tests/test_service.py` using a real `AnthropicProvider` + real
`AIRouter` through the actual FastAPI app, not just fakes). Full suite:
40 passed.

Also added, since there's no admin UI yet (Mission Control is Phase 11):
- `scripts/grant_permission.py` — grant/revoke/list capabilities against
  a running (or stopped) Core's permission store.
- `scripts/test_ai_complete.py` — send one test prompt to a running
  Core's `/ai/complete` and print the result.

Both were smoke-tested against a real running `jarvis_core.service.main`
instance in this session (confirmed `/health`, `/status`, and
`/ai/complete`'s error path all behave correctly).

## Next Action

Owner-supplied Anthropic API key (via the OS keyring, never a config file
or env var) to validate a real end-to-end call against the live API, then:
a second provider or broader router capability (model/task routing), or
move toward a plugin that actually calls `/ai/complete` — whichever the
owner prioritizes.
