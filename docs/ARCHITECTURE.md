# Architecture decisions

## ADR 001 — Separate extraction from presentation

The UI imports pure domain functions. The Pydantic contracts are shared across extraction modes. Provider-specific behavior lives in one module. This keeps failure cases testable without a model request.

## ADR 002 — Start with an inspectable baseline

A keyword baseline supplies a free demonstration and a repeatable comparison. It does not understand all language. Preserve its limitations in tests and challenge cases rather than hiding them behind confident phrasing.

## ADR 003 — Verify quotations independently

After a live response is parsed, reject evidence absent from the input. This is a necessary but insufficient grounding check. A real quote can be paired with an incorrect skill or priority. The chapter teaches this explicitly.

## ADR 004 — Bounded optional live mode

Live AI is disabled by default. Configuration stays server-side; no client receives credentials. The adapter has a timeout and no retries. A public paid-inference service requires authentication, quotas, abuse controls, and stronger operational instrumentation beyond this chapter.

## ADR 005 — Shared content, two delivery modes

`content/chapter1.json` supplies both the Streamlit reader and generated HTML. The build script also derives the browser skill registry from the Python registry. The browser companion escapes user text before rendering. It checks short exercise answers rather than executing submitted code.

## Limits

No live job ingestion, freshness verification, salary extraction, applicant ranking, production authentication, persistent database, or verified credentialing is implemented. The synthetic sample describes no real employer vacancy. Practice progress is self-reported. The live adapter requires real-service verification before claims about provider behavior.
