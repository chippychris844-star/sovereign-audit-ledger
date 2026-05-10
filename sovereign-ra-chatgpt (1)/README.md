# Resolution AI v5.1

Resolution AI is a local-first, verification-labelled assistant for Resolution Assurance.

## Start

Double-click:

- `CREATE DESKTOP ICON - RESOLUTION AI.cmd`

Then use the **Resolution AI** desktop icon.

Alternative:

- `START_RESOLUTION_AI.cmd`

## Defaults

- Private storage prefers `D:\SovereignRA`.
- Claude / Anthropic is the primary hosted provider when a valid key is found.
- Ollama local is the fallback.
- OpenAI is advanced/manual only.
- WordPress can read Resolution Assurance content through the REST API when configured.
- Attachments, microphone input, local file browser, code sandbox, graph anchoring, audit log, and legal pages are included.

## Verification

Answers behave like a normal chatbot, but the UI displays a status badge:

- Verified
- Partially Verified
- Not Verified
- Insufficient Evidence

High-impact claims such as valuations require stronger rooted evidence.
