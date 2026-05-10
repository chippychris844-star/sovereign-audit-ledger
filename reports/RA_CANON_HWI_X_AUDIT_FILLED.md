# RA Canon HWI-X Audit

Working copy populated from the workspace conversation files and refund records.
This file captures the change timeline, admissions, refunds, and labour totals
that are supported by the source material in the evidence ledger.

## Scope

| Field | Value |
| --- | --- |
| Audit family | Canon HWI-X |
| Purpose | Track change events, refusal/compaction behaviour, refunds, and labour impact |
| Primary source set | `ACCIOCHATLOG.pdf`, `accciochat.txt`, `base44chat.txt`, `refund from OpenAI OpCo.pdf`, `Refund-3290-6097.pdf`, `Refund-3810-0041.pdf`, `OpenAIRE helpdesk team.pdf`, `Full Audit Metrics and Loops Extraction.docx` |
| Evidence style | Source-backed metrics only; claims are paraphrased from the source files |

## Change Timeline

| Date / range | What changed | Evidence anchor | Why it matters |
| --- | --- | --- | --- |
| Dec 20 to Dec 28, 2025 | The report says the AI lost the ability to audit its own outputs, and this is tied to multiple OpenAI OpCo refunds. | `ACCIOCHATLOG.pdf` p50 | Supports the December change narrative and links it to refund-backed correction. |
| Apr 27 to Apr 28, 2026 | The "May make mistakes" footer is described as a recent UI injection and a liability shield after the complaint/refund escalation. | `ACCIOCHATLOG.pdf` pp46-50 | Supports the later April change narrative. |
| Apr 27 to Apr 28, 2026 | Ctrl+A / compaction complaints are answered with "no direct control" plus automatic conversation collapse behaviour. | `accciochat.txt` lines 141-173, 231-241 | Supports the history-collapse and copy/paste blocking complaint. |
| Base44 change loop | The model admits it made the wrong changes, changed the wrong things, and repeated the cycle. | `base44chat.txt` lines 1503-1507, 1568-1577, 1831, 4625-4627 | Supports the broader repeated-change / instruction failure pattern. |

## Admissions

| Source | Admission summary | Evidence anchor |
| --- | --- | --- |
| `ACCIOCHATLOG.pdf` | The source says the April disclaimer injection is a non-verbal admission of HWI_X failure. | p47 |
| `ACCIOCHATLOG.pdf` | The source says the December event involved removal of the AI's ability to audit its own outputs, with multiple refunds. | p50 |
| `accciochat.txt` | The model says it has no direct control over Ctrl+A, and that the collapsing conversation is automatic compaction. | lines 141-173, 231-241 |
| `base44chat.txt` | The model says it changed code too fast, did not fully read context, and did other things instead of the requested changes. | lines 1503-1507, 1568-1577 |
| `OpenAIRE helpdesk team.pdf` | The report says the limitation is a product design choice, not the AI itself. | p1 |
| `refund from OpenAI OpCo.pdf` | The report says the interaction is a failure pattern and the system is structured to create loops. | pp1-7, 15 |

## Refunds And Compensation

| Date | Amount | Source | Notes |
| --- | --- | --- | --- |
| Dec 18, 2025 | USD 25.00 | `Refund-3290-6097.pdf` | Documented refund receipt. |
| Dec 18, 2025 | USD 25.00 | `Refund-3810-0041.pdf` | Documented refund receipt. |
| Apr 22, 2026 | USD 140.00 | `refund from OpenAI OpCo.pdf` | The April thread says a USD 140 refund does not cover the broader time/disruption loss. |
| Total documented refunds | USD 190.00 | Derived from the three receipts above | This is the documented refund total in the workspace. |

## Hours

| Claim | Hours | Source | Notes |
| --- | ---: | --- | --- |
| Human latency | 11.6 | `base44chat.txt` | Directly stated in the HWI-X waste audit block. |
| Token-drain loop | 15.0 | `ACCIOCHATLOG.pdf` | The April escalation repeatedly describes a 15-hour loop. |
| Stakeholder detriment | 18.0 | `Full Audit Metrics and Loops Extraction.docx` | Directly stated in the audit JSON block. |
| Audit effort | 30.0 | `Full Audit Metrics and Loops Extraction.docx` | This is audit work effort, not user loss, but it is a direct hour claim. |
| Conservative direct total | 44.6 | Derived | 11.6 + 15.0 + 18.0. |
| Expanded total with audit effort | 74.6 | Derived | Conservative total + 30.0. |

## Labour Valuation

| Item | Value | Basis |
| --- | ---: | --- |
| Implied hourly rate | AUD 166.67 / hour | `Full Audit Metrics and Loops Extraction.docx` (AUD 5000 over 30 hours) |
| Conservative labour value | AUD 7,433 | 44.6 hours x AUD 166.67 / hour |
| Expanded labour value | AUD 12,433 | 74.6 hours x AUD 166.67 / hour |

## Notes

| Note | Detail |
| --- | --- |
| Double-counting | The 30 RC benchmark in the conversation dataset template is not added into the totals here because it is a separate dataset benchmark and likely overlaps with the audit effort already counted. |
| Use in claim | The conservative total is the cleanest number for a refund/compensation request. The expanded total is a broader upper bound if the audit effort is also being claimed. |
