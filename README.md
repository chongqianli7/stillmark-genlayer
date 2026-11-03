# STILLMARK

A record between hands.

Stillmark is a small loan-handover desk for tagged objects. A lender fixes an outgoing condition note and the parts to inspect. The named receiver signs an arrival note from their own wallet. GenLayer compares each part; both parties may acknowledge only the exact accepted comparison.

The lamp example preserves an old base scratch, detects a newly reported stem dent, and leaves the unchanged shade alone. A second record omits the stem inspection and blocks acknowledgement.

## Open the desk

[Application](https://chongqianli7.github.io/stillmark-genlayer/) · [Contract](contracts/stillmark.py) · [Protocol](PROTOCOL.md) · [Network evidence](EVIDENCE.md)

1. Start with **Offline practice**. Compare the authored notes, then try missing information. These fixtures use no wallet, model call or network transaction.
2. Choose **Read finalized example** to inspect the deployed record without signing.
3. For a new handover, switch to **On chain**, connect a wallet on Stable Studionet 61999, and enter a distinct receiver, tagged item and up to five parts. Sign the dispatch note once.
4. The named receiver reads that owner-qualified record and signs their own arrival note. Either party requests comparison.
5. Inspect every part, the identity finding and source quotations. REVIEW blocks acknowledgement. CONSISTENT or EXCEPTIONS permits each party to acknowledge the same digest. Two signatures close the record; either party may instead decline before completion.
6. Export the readback and the current session's last receipt as JSON. Existing receipt hashes remain available in the evidence directory.

Temporary sessions are optional, memory-only zero-balance test signers. Create two to explore both roles; they do not establish independent people. Never fund them. Reload loses their signing keys, while public records remain readable.

## Why consensus matters

Different wording can describe the same scratch. Missing information must not become evidence of an undamaged object. The leader and validators independently classify object identity and every part's before/after condition. The complete ordered label vector and identity finding must agree; agreement on the overall status is insufficient. Quotes are checked against the exact signed notes but their wording is not required to match across validators.

Deterministic code derives the status, hashes the full comparison with both reports and party identities, and enforces two distinct acknowledgements on that digest. An application operator cannot submit the receiver's note or supply an unvalidated result through the public API.

## Run

Node 22+ and Python 3.11+:

```sh
npm ci
npm test
npm run test:contract
npm run build
npm run dev
```

The production output is static `dist/`. Dependencies are pinned; no paid API, database or server is needed. The GitHub Pages workflow builds and publishes the default branch. Tests use mocked GenLayer hosts and model responses; real network evidence is documented separately.

## Boundaries

The reports are public, user-supplied observations. Stillmark does not inspect the object, authenticate photos or identity, determine damage causation, certify insurance coverage, move funds, or transfer custody. Consensus can be wrong. Wallet distinction is not proof of independent people. Acknowledgement accepts the record, not legal liability or the physical truth of either report. Corrections require a new ID; records are immutable after their respective signatures.

Stable Studionet only: chain `61999`, RPC `https://studio.genlayer.com/api`. Writes use zero value and full consensus, and stop if the gas price is nonzero. MIT licensed. The lamp illustration is an original code-drawn SVG.
