# Signed condition protocol

Records are addressed by lowercase dispatch owner and a 1–40 character lowercase alphanumeric/hyphen ID. The receiver must be a distinct nonzero address. Object identity is 5–180 characters; there are 1–5 unique named parts of 2–60 characters; each signed report is 30–3,000 characters.

| Call | Who can write | Effect |
| --- | --- | --- |
| `dispatch(id, receiver, item, parts_json, before)` | Any sender | Fix sender, receiver, tagged object, parts and outgoing report |
| `receive(owner, id, after)` | Named receiver | Fix incoming report once |
| `compare(owner, id)` | Either party | Independently interpret immutable reports once |
| `acknowledge(owner, id, expected_digest)` | Either party, once each | Accept exact result; second approval closes record |
| `decline(owner, id)` | Either party before terminal state | Close without acknowledgement |
| `get_record(owner, id)` | Read only | Exact JSON record or empty string |
| `get_protocol()` | Read only | `stillmark-1` |

`DISPATCHED → RECEIVED → CONSISTENT / EXCEPTIONS / REVIEW`. Two exact-digest approvals produce `ACKNOWLEDGED`. Either party can produce `DECLINED` before completion. REVIEW cannot be acknowledged. No report edit or reassessment is exposed; a correction needs a new record. Distinct IDs intentionally create distinct records; do not resubmit an ambiguous write.

## Classification

- Identity `SAME`: both reports explicitly identify the tagged item. Otherwise `UNCLEAR`.
- `UNCHANGED`: explicit equivalent condition, including unchanged pre-existing damage.
- `NEW_DAMAGE`: arrival explicitly reports deterioration relative to an explicitly better outgoing state. This does not locate the cause or timing.
- `IMPROVED`: explicit improvement relative to departure.
- `UNCLEAR`: missing, ambiguous, incompatible or incomparable observations.

Each part has grounded before/after quotes. Missing parts use another real passage as context and must remain UNCLEAR. A substring check establishes quote provenance, not semantic correctness.

The leader and validators use the same fixed prompt and original data independently. The custom validator parses both results, checks quote grounding, then compares identity and every ordered label exactly. Invalid output or non-return values cannot approve. Explanatory prose is not generated or stored.

Any unknown identity or part derives REVIEW. Otherwise any changed part derives EXCEPTIONS; all unchanged derives CONSISTENT. An exception can be acknowledged explicitly by both parties. Uncertainty cannot.

The SHA256 digest includes protocol, namespace, both parties, object, parts, exact reports and accepted findings. All acknowledgements carry this exact digest. No timestamp, off-chain URL authenticity, photo evaluation, payment, escrow, deadline or legal certificate is implied.

## Client lifecycle

Before writing, check chain 61999, selected account, zero gas and deployed source byte identity. Store an intent before sending and its returned hash immediately. Pending intent survives refresh. Poll that same hash, bind sender/contract/method/arguments, require FINALIZED, MAJORITY_AGREE and successful execution, then read `latest-final` and check the method's persisted effect. A readback failure retains tracking. Timeouts do not permit automatic resubmission. An unknown send outcome requires manual investigation; it is intentionally not silently cleared.
