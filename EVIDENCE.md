# Network evidence

Stable Studionet · chain 61999 · [contract 0xc4b68c5c24a96Eca51FB43E981ccA27d88A50EcA](https://explorer-studio.genlayer.com/address/0xc4b68c5c24a96Eca51FB43E981ccA27d88A50EcA)

Deployed source SHA256: `bbf9a61b1abc4feed131e8b6092e5ad5bb4ffb3945f3f7cb32c25481fef2b3fa`. Deployment code was read back and compared byte for byte before use.

The lamp fixture is authored. Two distinct temporary zero-balance accounts were controlled by one test operator; this does not demonstrate independent human inspections. Full consensus was requested for each call.

| Call | Transaction | Final execution |
| --- | --- | --- |
| 01-deploy | [0xc54bbccec8…](https://explorer-studio.genlayer.com/tx/0xc54bbccec86ba53933d98dfff6b61577c115fe2e89457b48983e720bc5815375) | FINALIZED / SUCCESS |
| 02-dispatch | [0x71fe588411…](https://explorer-studio.genlayer.com/tx/0x71fe588411bf8e315dc0d86a3fcf5648638221fef221d5a681c6fa12e585437b) | FINALIZED / SUCCESS |
| 03-receive | [0xa3f8a2fe65…](https://explorer-studio.genlayer.com/tx/0xa3f8a2fe6596a0fd0fa213a1bf72cf77426f11ea34fd00d9aef305db5b597452) | FINALIZED / SUCCESS |
| 04-compare | [0x59c7db12c7…](https://explorer-studio.genlayer.com/tx/0x59c7db12c73ba5e5782c634be9687a4f8089ae6674f9cb4f9683f9ad48f49e85) | FINALIZED / SUCCESS |
| 05-stale-digest-denied | [0x88af7caa42…](https://explorer-studio.genlayer.com/tx/0x88af7caa4218a3907d016f03189e2d43bd1de5c49c233de4b99793867c5e51a6) | FINALIZED / ERROR |
| 06-owner-acknowledges | [0x1e5bc3c153…](https://explorer-studio.genlayer.com/tx/0x1e5bc3c153051797c336bb1322d68648fa41e134fa0cdf4cc0f696f1a5d80226) | FINALIZED / SUCCESS |
| 07-receiver-acknowledges | [0x8ed63bbc15…](https://explorer-studio.genlayer.com/tx/0x8ed63bbc1561c0ac457a81d3aee25fbc3e3c36fdb31eb6a9234e50c162ba07b5) | FINALIZED / SUCCESS |
| 08-incomplete-dispatch | [0x11ec0b462f…](https://explorer-studio.genlayer.com/tx/0x11ec0b462f5814efcbf05aec060e1f855c3a7cbb4b4597eb8f332a64bd4084a3) | FINALIZED / SUCCESS |
| 09-incomplete-receive | [0x5ea642950d…](https://explorer-studio.genlayer.com/tx/0x5ea642950defe222fb3635a1be5cf47522e453352840c167d9fe61fce21e701d) | FINALIZED / SUCCESS |
| 10-incomplete-compare | [0x523cb20bb7…](https://explorer-studio.genlayer.com/tx/0x523cb20bb78002cdb4814ab14f903bfc436392f40578a6eac2b8790943ac5ba1) | FINALIZED / SUCCESS |
| 11-review-ack-denied | [0xb456abd593…](https://explorer-studio.genlayer.com/tx/0xb456abd5934e8302369092c0db630600548d45fb9f499b102e8a79e096d048fe) | FINALIZED / ERROR |

Main record: `ACKNOWLEDGED`, identity `SAME`, labels `UNCHANGED / NEW_DAMAGE / UNCHANGED`, two approvals.

Incomplete record: `REVIEW`; the uninspected stem is `UNCLEAR`. Acknowledgement is rejected. The deliberately stale-digest call is also rejected. Failed calls are retained as negative evidence.

[Raw network receipts and saved state](evidence/studionet.json.gz) · [Compact index](evidence/summary.json) · [Deployment configuration](public/deployment.json).

Offline validation: 14 mocked-host contract tests, 3 JavaScript helper tests and a production build passed. These checks do not prove remote model accuracy or prompt-injection immunity. Browser practice and finalized public-record readback were exercised separately.

Raw receipts use lossless gzip compression. Inspect with `gzip -dc evidence/studionet.json.gz`.
