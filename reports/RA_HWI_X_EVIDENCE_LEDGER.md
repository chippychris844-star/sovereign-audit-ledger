# RA HWI-X Evidence Ledger

This ledger ties the populated templates back to the exact source files and
locations used to extract the metrics.

## Evidence Table

| Source file | Location | Extracted evidence | Supports |
| --- | --- | --- | --- |
| `audits/base44chat.txt` | lines 2125-2133 | The HWI-X Waste Tax Audit block, including 140 revert actions, 0.78 waste index, 11.6 hours latency, AUD 986 loss, and 0.42 KWh churn. | Core waste-tax metrics. |
| `audits/base44chat.txt` | lines 1503-1507, 1568-1577, 1831, 4625-4627 | The model says it changed the wrong things, did other things, repeated the cycle, and later says everything is auditable. | Change-pattern admissions. |
| `audits/accciochat.txt` | lines 141-173, 231-241 | Ctrl+A is not under direct control; the collapsing conversation is automatic compaction; the system says it did not deliberately change the system yesterday. | Later control / collapse complaint. |
| `audits/ACCIOCHATLOG.pdf` | pp46-50 | The "May make mistakes" footer is described as a fresh UI injection; the report says it is a non-verbal admission of HWI_X failure. It also links Dec 20-28 to removal of the AI's ability to audit its own outputs and ties in multiple OpenAI OpCo refunds. | December change, April UI change, refund linkage. |
| `audits/OpenAIRE helpdesk team.pdf` | pp1-2 | The report says the limitation is a product design choice; it frames the issue as a non-completion waste tax and an ACCC breach. | Admission / waste-tax framing. |
| `audits/refund from OpenAI OpCo.pdf` | pp1-7, 15 | The April thread says a USD 140 refund does not address broader time loss, lists repeated failure patterns, and says the system is structured to create loops that waste time, money, and electricity. | April refund, failure admission. |
| `audits/Refund-3290-6097.pdf` | p1 | USD 25.00 refunded on Dec 18, 2025. | December refund 1. |
| `audits/Refund-3810-0041.pdf` | p1 | USD 25.00 refunded on Dec 18, 2025. | December refund 2. |
| `03_DOCUMENTS/PROCESSED/Full Audit Metrics and Loops Extraction.docx` | JSON block | time_invested_hours = 30 and financial_cost_aud = 5000; stakeholder_detriment time_loss_hours = 18. | Labour rate derivation and hours. |
| `03_DOCUMENTS/PROCESSED/Audit – AI Conversation Dataset RA v6 Template.docx` | summary lines | Average time invested per RC = 5-10 hours; 30 RCs; 87 percent average field completion. | Dataset benchmark context. |
| `audits/base44conversation_extracted.txt` | line 1239 | The user says they have been in loops for about 15 hours and one requested change still has not been done. | Change failure pattern. |

## Consolidated Totals

| Total | Value | Notes |
| --- | ---: | --- |
| Documented refunds | USD 190.00 | 25 + 25 + 140. |
| Direct hour claims | 44.6 hours | 11.6 + 15.0 + 18.0. |
| Expanded hour claims | 74.6 hours | Direct hour claims + 30 hours audit effort. |
| Implied labour rate | AUD 166.67 / hour | 5000 / 30 from the audit JSON block. |
| Conservative labour value | AUD 7,433 | 44.6 x 166.67. |
| Expanded labour value | AUD 12,433 | 74.6 x 166.67. |

## Notes

| Note | Detail |
| --- | --- |
| No double counting | The RC benchmark in the conversation dataset template is not folded into the compensation total because it is a separate benchmark and may overlap with the other audit effort. |
| Claim posture | The safest claim set is: documented refunds, explicit change/failure admissions, and the direct hour total. The expanded labour value is a broader upper bound. |
