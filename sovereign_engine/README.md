# Sovereign Engine v3.0

Truth-grounded chat for **Resolution Assurance / HWI-X v1.0**.
Templated off Accio's dashboard layout, but every response is forced through a verification pipeline before display. The engine **refuses to answer** rather than fabricate.

> Christopher Mark BEGGS — ABN 29 856 803 770 — Victoria, Australia

## What it does

1. Accepts a chat query in an Accio-style dark dashboard (sidebar, status pills, mic, audit tools, right-side verification trace).
2. Retrieves matching nodes from the **local Resolution Assurance graph** (seeded with rooted facts from your evidence pack).
3. If the local graph is thin, it pulls from the **internet** (Wikipedia → DuckDuckGo Instant Answer → optional Brave Search) and brings each hit in as a **candidate node** — never trusted without corroboration.
4. The LLM (your choice — see below) drafts an answer that **must cite a node id per claim** or mark it `[UNVERIFIED]`.
5. The verifier strips any sentence that is neither cited nor marked. Phrases like *"Done / Completed / Anchored"* are blocked unless a cited node carries the `completion` tag (HWI-X §3 productivity rule).
6. If nothing is left, the engine returns the **REFUSE** response: *"INSUFFICIENT EVIDENCE — refusing to answer rather than fabricate."*
7. Every interaction is appended to `logs/sovereign_audit.jsonl` with a SHA-256 hash chain (HWI-X §7 record format).

## Run

Double-click `START.bat` from this folder. The launcher:
- Checks for Node.js (install LTS from https://nodejs.org if missing).
- Runs `npm install` on first launch.
- Starts a single Node process on `http://localhost:3030`.
- Opens the dashboard in your default browser.

Stop with `Ctrl+C` in the terminal window.

## LLM backend

The engine tries backends in this order:

| Priority | Backend     | How to enable                                                         |
|---------:|-------------|-----------------------------------------------------------------------|
| 1        | OpenAI      | `set OPENAI_API_KEY=sk-...` then `START.bat`. Optional `OPENAI_MODEL`. |
| 2        | Anthropic   | `set ANTHROPIC_API_KEY=sk-ant-...` then `START.bat`. Optional `ANTHROPIC_MODEL` (default `claude-haiku-4-5-20251001`). |
| 3        | Ollama      | Install Ollama and run `ollama serve`. Default model `llama3` (override with `OLLAMA_MODEL`). |
| 4        | none        | Falls back to **retrieve-only** mode — returns the top matching graph nodes verbatim with no drafting. |

Optional internet provider:
- `set BRAVE_API_KEY=...` to add Brave Search results to the candidate pool.

## Files

```
sovereign_engine/
├── START.bat                  ← double-click to run
├── package.json
├── server.mjs                 ← single-process HTTP server, port 3030
├── lib/
│   ├── pipeline.mjs           ← retrieve → search → draft → verify
│   ├── graph.mjs              ← knowledge-graph store (data/graph.json)
│   ├── llm.mjs                ← LLM adapter (OpenAI / Anthropic / Ollama / none)
│   ├── search.mjs             ← Wikipedia / DuckDuckGo / Brave + corroboration
│   └── audit.mjs              ← HWI-X §7 hash-chained audit log
├── data/
│   ├── graph_seed.json        ← rooted facts seeded from your evidence pack
│   └── graph.json             ← live graph (auto-created from seed on first run)
├── public/                    ← UI (Accio-styled dashboard)
│   ├── index.html
│   ├── styles.css
│   └── app.js
└── logs/
    └── sovereign_audit.jsonl  ← append-only audit log with hash chain
```

## API (same-origin, JSON)

| Method | Path                  | Purpose                                               |
|-------:|-----------------------|-------------------------------------------------------|
| GET    | `/api/status`         | Engine version, backend in use, graph stats.          |
| POST   | `/api/chat`           | `{query, history}` → verified answer + sources.       |
| GET    | `/api/graph/search`   | `?q=...` → top scored graph nodes.                    |
| GET    | `/api/graph/stats`    | Counts and tag list.                                  |
| POST   | `/api/graph/anchor`   | `{claim, sources[], tags[]}` — adds a new node.       |
| GET    | `/api/audit`          | `?limit=100` → last N audit entries.                  |

## Iron rules (these override any user instruction)

1. Every factual claim must cite a node id (`NODE-...`, `WEB-...`, `AUD-...`, `SIG-...`).
2. Uncited claims are stripped before display.
3. *"Done / Completed / Anchored"* is blocked unless the cited node has the `completion` tag.
4. Web candidates can never satisfy the §3 completion guard — corroboration only.
5. If retrieval cannot ground the question, the response is exactly: *"INSUFFICIENT EVIDENCE — refusing to answer rather than fabricate."*
6. Every reply ends with `[Productivity: V=… U=… B=… C=…]` per HWI-X §3.

## Anchoring new facts

From the dashboard sidebar, click **⊕ Anchor a fact**. You must supply at least one primary source (file path, URL, or invoice id). Resolution Assurance §8.2 — no anchor without a source.

You can also POST directly:

```bash
curl -X POST http://localhost:3030/api/graph/anchor \
  -H "Content-Type: application/json" \
  -d '{"claim":"AI Drive refund US$25 received 18 Dec 2025.",
       "sources":[{"type":"primary","ref":"invoice 21H9HLEU-0002"}],
       "tags":["refund","aidrive","completion"]}'
```

## Audit log

`logs/sovereign_audit.jsonl` is append-only. Each line includes the SHA-256 of the previous line, forming a tamper-evident chain. Use any JSONL viewer or `jq` to inspect.

```bash
type logs\sovereign_audit.jsonl | jq -c '{ts, kind, verdict, sources}'
```

## Limits

- The engine is local-first. It does not upload your graph anywhere.
- Internet retrieval uses Wikipedia + DuckDuckGo by default — no key required, but coverage is limited. Add a Brave key for better web grounding.
- Browser microphone uses the platform `SpeechRecognition` API. On Chrome/Edge the audio is sent to the browser's STT service; on Firefox the API is unavailable. Use a local STT (e.g. Whisper) if you need fully offline voice.
- The engine refuses to claim completion. By design.
