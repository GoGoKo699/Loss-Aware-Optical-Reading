# Independent review of supplied robustness delivery

Review date: 2026-09-15. Scope: inspect and reproduce the supplied bounded four-mode study; no science extension, repository edit, branch mutation, remote commit, or CI claim by this reviewer.

## Decision

**PASS for unchanged evidence import with a separate current-status integration wrapper.** No scientific or file-integrity blocker was identified. The original delivery explicitly records that it was pending a remote commit when created; preserve that text and its hashes as historical evidence. The current integration wrapper should report the actual resulting commit and CI separately.

The parent verified the original archive SHA-256 `ee21bb13afbd913779b5d2eae7b4f15a58d919500a7ed38b09deafb7e929c81b` and reported that remote `research/robustness-01` remained at `ddb17c5040e17cb0078121081afe15de70158fe8`. This reviewer did not independently inspect the remote branch; the parent must retain its live remote verification record.

## Inspection and preservation

Read `APPLY.md`, `DELIVERY.json`, all 15 supplied study files, the patch inventory and full study/proof/verifier code, manifests, original execution notes, and archived certificates. Also inspected repository `AGENTS.md`, `README.md`, `CLAIM_STATUS.md`, `SOURCE_AUDIT.md`, `docs/PHYSICAL_SETTING.md`, `docs/CONTRIBUTIONS.md`, `work_orders/CURRENT.md`, first-experiment protocol, reproduction guide, and numerical contract from the materialized source tree. This reviewer did not call that materialized tree an authenticated checkout.

Verified every hash listed by the supplied `MANIFEST.json`; verified the patch SHA-256 `1e1fe5bd4f2154c6dad00aac3dc090a790ca4a6089a96741a64f807c26955c6b`; verified `EVIDENCE.tar.xz` SHA-256 `b65074d1733bc648d5f0ac20a6dd6b1eea3334317fb73261ef8aff0573188f8b` and every archive member hash and inventory entry. The patch adds exactly 15 files under `studies/robustness-01/`, with no existing work order or canonical file replaced. A patch round-trip in an empty disposable scratch directory produced all 15 files byte-for-byte identical to the supplied study. No repository or branch was changed by that round-trip.

## Checks actually executed

Environment: Python 3.12.14; NumPy 2.3.5; SciPy 1.17.0. The original execution used Python 3.13.5; the two numerical package versions match. No dependency installation or network call was needed for the local checks.

| Check | Result |
|---|---|
| Supplied `test_local.py` | PASS, 8 unit-test groups |
| Fresh `study.py` regeneration | PASS, 41 scenarios and 381 diagnostics |
| Regenerated `RESULTS.json` comparison | Byte-identical to supplied results; SHA-256 `74c0b5ca9f114be36501426f28dc012fcfdb6b872ed6bb8533d463b6cddd14db` |
| Supplied optimizer-free certificate verification | PASS, 11,161 checks including 10,828 exact positive-matrix checks |
| Fresh regenerated certificate verification | Same PASS counts; `scipy.optimize.linprog` was patched to raise on any call and had zero calls |
| Existing-output refusal | Both scripts refused existing output directories; checked result hashes were unchanged |
| Manifest, evidence inventory, patch round-trip | PASS |

All regeneration and verification outputs were created in new directories. These counts identify separate check inventories and must not be added together as a proof count. Logs and JSON records are under the sibling scratch directory `robustness-review-runs/` and can be archived by the integrating workspace. This reviewer did not run inherited repository regressions or remote CI; those belong to the parent's final-tree integration checks.

## Scientific assessment and exact assumptions

The study is restricted to four active paths, uniform fresh hidden labels, a single incident photon in those paths, inaccessible loss modes, no retained idler or occupied bypass, one call, and score `C - 5 E` per attempted interrogation. Source impurity, detectors, real calibration uncertainty and trial-rate feasibility are separate inputs. No SU8 extension is proved by this study.

1. **Common calibratable basis change.** For maps `A_j = V T O_j W`, common known unitary matrices V and W can be absorbed into preparation and a single calibrated receiver. They must be the same for every hidden label and every loss/penalty point claimed to share that receiver. A label-dependent correction would require the hidden answer. A point-dependent V changes the physical receiver across the scan and must be reported. The six finite examples exercise the common output-unitary case; the general common input/output statement has the short algebraic proof in the supplied file.

2. **Specified symmetric dephasing.** The channel multiplies every pairwise off-diagonal coherence by the same real `v` in `[0,1]`, independently of the hidden label, after the diagonal-loss orthogonal four-symbol code. The jointly optimal score is the positive part of the top eigenvalue of `B_v = (3 v / 2) a a^T - (7/2 + 3 v/2) diag(eta)`. A positive top eigenvector supplies the input, and the same D4 receiver attains the bound; always inconclusive attains zero. I independently checked the payoff algebra: the coherent contribution gives `(3v/2)(sum sqrt(eta_i) z_i)^2` and the diagonal term gives `-(7/2+3v/2) sum eta_i z_i^2`. The visibility threshold `v > 7/9` concerns positivity of this particular penalized score, not existence of all information. A single measured fringe visibility does not by itself establish this channel; unequal coherence factors, deterministic bias and averaged-amplitude substitutions are excluded.

3. **Systematic marked-phase bias.** The marked phase is `pi + delta`, with an exact rational unit-circle parameter `delta = 2 atan(q)`; nominal transmission values are displayed approximations to the exact rational squares of recorded binary64 amplitudes. The fixed receiver class includes all complex normalized inputs and all 625 deterministic label/failure assignments to its four click outputs; the common vacuum is inconclusive. The joint class includes arbitrary POVMs in the specified no-idler model. Exact positive rational factors/completeness and payoffs prove feasible lower scores; exact Hermitian dual inequalities prove upper scores. Positive lower regret is therefore established for the listed finite instances, rather than inferred from a failed local search. The alternative polar-factor receiver is a feasible four-mode construction. The small-error order comparison does not constitute a universal phase tolerance.

4. **General map deviations.** The channel trace-distance argument including the vacuum block gives at most `12 epsilon` score perturbation for contractions separated by operator norm epsilon, hence receiver regret at most `min(1,24 epsilon)`. The declared radius must cover the actual test-time map. This conservative continuous statement is distinct from numerical examples and is often loose.

5. **Common downstream rotated loss.** The specified downstream contraction permits a data-processing joint ceiling. Its feasible fixed score gives a conservative regret upper bound. The reported gap can include actual information loss as well as receiver suboptimality and is not a tight achieved regret. Inserting uncharacterized chip or detector losses into T would not be justified by these examples.

The numerical optimizer proposes witnesses; it is not trusted as the proof. Exact rational LDL checks are sufficient strict-positivity checks and do not claim a complete semidefinite decision procedure. The verifier rebuilds optical payoffs and independently checks direct propagation and uniform-loss receiver formulas, but shares the exact arithmetic and model constructor with the study; this is not formal verification of all code or of hardware.

The `P1_illustrative` fields are ordinary floating-point sensitivity forecasts for an ideal one-photon source with mean budget 1, uniform downstream survival 0.92, and no dark counts or source impurity. They are not the parent's imperfect-source forecast (mean upper budget 0.98), not rounded-safe whole-pipeline confidence certificates, and not an acquisition plan. They must not replace registered M1/P1/P2 meanings, penalties, confidence allocations or raw-record rules.

## Integration instructions and remaining laboratory inputs

Preserve the supplied files, original archive, `APPLY.md`, `DELIVERY.json`, manifests, original evidence, and existing work-order history. Add an integration wrapper linking this verification, the current commit and actual CI. Do not rewrite the supplied pending-status paragraphs or refresh their hashes. The user has separately authorized reviewed handover integration, so the original packet's no-main-merge boundary documents its delivery stage and does not negate the current instruction.

The lab worksheet is suitable for recipe links. It correctly separates near-optimality from nonclassical-source advantage. All hardware values remain blank: common phase-referenced maps and simultaneous test-time envelopes; decomposition of static offsets, random dephasing, marked-phase bias and distributed loss; incident source probabilities and a justified energy/tail bound at P0; preparation error; per-port complete readout/erasure response; held-out drift; and a predeclared statistical plan. Both chips are confirmed by the owner in the current handover; the original study does not establish their supporting interface.

No visual GitHub rendering check, external source-access re-audit, physical calibration, apparatus execution, remote merge or remote CI is claimed here.
