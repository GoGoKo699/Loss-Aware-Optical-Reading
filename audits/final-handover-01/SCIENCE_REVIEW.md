# Final scientific and laboratory-handover review

Reviewed commit `ba00d9ce64333ad08ef3b61108aa6df959cc5fc7`, tree
`605719db8b64ec45d75454dbe4338d56140d8593`, on `audit/final-handover-01`.
The initial working tree was clean. This bounded review read the current
scientific/protocol documents, their canonical proof contracts, plan templates,
and matrix/displacement construction in `scripts/lab_reference.py`. It makes
no science changes, performs no new literature campaign, and does not claim
fresh numerical regeneration or CI results; those have separate audit records.

**Decision: no scientific blocker found to releasing these reference materials
for initial laboratory review. They are not ready for certified acquisition.**
Both processors are confirmed available; the missing acquisition inputs are
explicitly disclosed, rather than supplied by the synthetic examples.

## Checked contracts

| Area | Finding and evidence |
|---|---|
| SU4 conventions | Column amplitudes, output rows/input columns, the single-path pi flip `O_j`, and `D4=J/2-I` agree. The lossless equal input gives `D4 O_j a=e_j`; uniform transmission gives unconditional `(C,E,F)=(t,0,1-t)`. Both operations have determinant −1; their common `exp(i*pi/4)` multipliers give determinant one. The two-reflection preparation has determinant one and the required first column. [SU4](../../experiment/SU4.md), [construction](../../scripts/lab_reference.py). |
| SU8 routes | The four-label route is the direct-sum embedding, with spare inputs in vacuum and all spare-output outcomes retained as failures. Its shared SU phase is `exp(i*pi/8)`. Native8 uses the binary-dot Walsh code, whose columns are orthogonal; its hidden operations and normalized decoder have determinant one. It is not eight single-path flips. Separate eight-label records prevent importing the four-label certificate. [SU8](../../experiment/SU8.md), [Theorems 1–2](../../proofs/THEORY.md). |
| Physical phases and loss | The canonical maps retain a shared optical phase. Label-dependent global phase changes are correctly forbidden; common SU phases must be tracked and matched by P2 displacement. `T` is physical attenuation, not a unitary compiler setting. A known answer-dependent combined matrix establishes only transfer, not unknown-operation reading. [Interfaces](../../experiment/INTERFACES.md), [commissioning](../../experiment/COMMISSIONING.md). |
| A and B | A remains the candidate complete joint input/measurement reduction under the flat-code, uniform-label, positive diagonal-loss contract. Known fixed-input decoding and harmonic-mean ingredients are credited. B remains a derived optical all-classical-source benchmark; neither independent generic novelty nor a tight arbitrary-loss frontier is asserted. [Contributions](../../docs/CONTRIBUTIONS.md), [source audit](../../SOURCE_AUDIT.md), [claim ledger](../../CLAIM_STATUS.md). |
| M1 | Uniform, inverse-loss and finite-penalty preparations use the same decoder. A finite scan tests the mechanism; it establishes neither global optimality nor source-class advantage. [M1](../../experiment/M1.md), [protocol §3](../../experiment/FIRST_EXPERIMENT.md#3-two-primary-tests-and-one-mechanism-test). |
| P1 | The comparison remains an unconditional photon score against all permitted classical mixtures and receivers, including receiver-known preparation labels, phase references and rare bright pulses at the same P0 mean signal budget. The four-label `lambda=5` ceiling is `min(1,(15/14)(1-exp(-kappa_U mu_U)))`; the general bound is not represented as attained. [P1](../../experiment/P1.md), [canonical proof §§2,4](../../proofs/THEORY.md). |
| P2 | The coherent receiver uses label-blind displacement `-T alpha` (or `-c T alpha` for a physical common phase), identity routing and direct clicks. It must beat the entire declared four-path one-photon upper bound, not one tested input. Displacement requires actual reference/coupling hardware. [P2](../../experiment/P2.md), [canonical proof §5](../../proofs/THEORY.md), [construction](../../scripts/lab_reference.py). |
| Planes and attempts | P0 charges incident signal after preparation; P1 ends the declared device before the unrestricted receiver. Downstream receiver/detector loss reduces the achieved score without silently reducing the competitor ceiling. All exposed attempts, no-click, multiple-click, leakage and rejected records remain in the denominator. Fresh independent hidden labels, blinding, separate pilot/test records and fixed N are preserved. [Physical setting](../../docs/PHYSICAL_SETTING.md), [protocol §§5–7](../../experiment/FIRST_EXPERIMENT.md). |
| Statistical contract | Recipes and provisional templates retain `lambda=5`, P1 `N=500000`, P2 `N=50000`, each `alpha_stat=.00025`, and shared simultaneous calibration failure allocation `.0005`; combined error is at most `.001` only under the declared assumptions. The radius is `6 sqrt(log(1/alpha_stat)/(2N))`. Conditional use needs the predictable-energy contract; a run-wide expected-energy average alone is insufficient. [Protocol](../../experiment/FIRST_EXPERIMENT.md), [primary plan](../../templates/primary_plan.example.json), [reverse plan](../../templates/reverse_plan.example.json), [finite-N proof](../../proofs/THEORY.md#finite-n-test-not-optional-stopping). |
| Robustness | Common-basis corrections, exact specified symmetric dephasing, finite marked-phase-bias counterexamples and conservative general-map bounds remain distinct. The guide's dephasing formula and `v>7/9` positive-score threshold match the study's four-mode `C-5E` proof. No universal noise tolerance, hardware calibration, native8 robustness or fully interval-certified pipeline is claimed. [Guide](../../docs/ROBUSTNESS_GUIDE.md), [study proofs](../../studies/robustness-01/PROOFS.md), [numerical contract](../../docs/NUMERICAL_CONTRACT.md). |

## Release nonblockers and interpretation

- The [README](../../README.md) makes publication significance conditional on
  successful measurements, complete calibration/comparisons and current novelty
  assessment. A remains a candidate; B supplies a credited comparison. No measured
  advantage or worldwide priority is reported.
- The new [computing relevance section](../../experiment/INDEX.md#relevance-to-photonic-quantum-computing)
  appropriately concerns measurement, control and signal-photon efficiency. It
  explicitly excludes computational speedup, universal computing, entangling-gate,
  error-correction, fault-tolerance, total-energy and wall-clock claims. Potential
  receiver reconfiguration savings still require measurement. Applying retuning
  to a computing subroutine requires a separate input/operation/objective mapping.
- The preserved first protocol's “later” eight-mode scope is explained by the
  current index/README: native Walsh8 reference commissioning now exists, while
  the registered four-label acquisition and certification scope is unchanged.
- Lack of an exact arbitrary-unequal-loss classical frontier is not a P1 blocker:
  a valid upper bound suffices. Lack of a native8 source-class plan does not block
  its separately labelled teaching/commissioning route. Hypothetical numbers,
  provisional plans and exact finite-model witnesses do not certify the apparatus.

## Acquisition blockers: laboratory inputs still required

Before a certified held-out run, obtain the inputs listed in
[the readiness worksheet](../../experiment/UNCERTAINTY.md) and
[protocol §§9–10](../../experiment/FIRST_EXPERIMENT.md):

1. A block diagram marking P0/P1, independently accessible preparation/hidden
   phase-and-loss/receiver roles, actual port and compiler conventions, compatible
   optical modes/readout, and any inter-chip coupling and leakage treatment.
2. A pre-exposure trial clock/herald, settling and gating timings, one exposure per
   fresh independent hidden draw, reader isolation and sealed-label joining.
3. Source vacuum/one-/multiphoton characterization and defensible P0 mean/tail
   energy bounds with test-time coverage. Multiphoton probability or `g^(2)` alone
   does not establish tail energy.
4. Actual common-phase P0-to-P1 maps, simultaneous uncertainty/drift coverage,
   accessible-mode accounting and the justified channel/noise model. Intensity
   fits and averaged amplitude matrices alone do not supply this certificate.
5. Complete detector/mask/time-tag records, receiver losses and nulling errors,
   with every exposed attempt retained; a frozen, pilot-informed plan and
   conservative anticipated margin before consuming the held-out trial budget.
6. For P2, a feasible and implemented stable coherent displacement receiver. If
   unavailable, its experimental comparison must be explicitly dropped; M1/P1
   review can proceed and the reverse region remains theoretical.

These are blockers to certified acquisition, not to sharing the present package
for initial technical feedback. Physical commissioning additionally needs the
lab's compatible illumination/readout and control interface; software reference
calculations alone do not establish that physical readiness. No release,
correspondence, hardware action or visibility change was performed by this review.

## Follow-up: presentation repair and preserved mathematics

The root reviewer subsequently found three live GitHub rendering errors in
`REPORT.md` section 3. This is a presentation defect, recorded separately from
the scientific assessment above. I independently inspected the final working
diff for [REPORT.md](../../REPORT.md) and complete source-to-reader diffs for
the three new reading copies; I did not edit those documents.

| Reviewed document | Scientific preservation finding |
|---|---|
| [Main report](../../REPORT.md) | Dollar-display to math-fence conversion, explicit fraction arguments, the equivalent less-than spelling, and protected inline norm/set transport retain the photon support equation, pairwise contrast normalization, operator norm, classical upper-C branches, simultaneous calibration bound, registered score ceiling, trial radius and all grid values. The processor-availability prose now agrees with the current physical setting; interfaces and calibration remain unsupplied. |
| [Robustness report](../../docs/ROBUSTNESS_REPORT.md) versus [preserved source](../../studies/robustness-01/REPORT.md) | All scientific statements, quantitative examples, boundaries and evidence claims are retained. Changes comprise math transport, rebased links, a source footer and omission of two obsolete delivery-status paragraphs from the reading copy. Those paragraphs remain in the original, and the footer points to the actual integration record. |
| [Robustness proofs](../../docs/ROBUSTNESS_PROOFS.md) versus [preserved source](../../studies/robustness-01/PROOFS.md) | All proof assumptions and equations are retained. In particular the dephasing matrix keeps coefficients 3/2 and 7/2, the fixed-receiver phase-bias score keeps 9/2, and the perturbation/regret bounds retain 12 and 24. The channel, semidefinite constraints, phase-bias receiver and rotated-loss map are unchanged. Only math transport, rebased links and the source footer differ. |
| [Numerical proof](../../docs/NUMERICAL_PROOF.md) versus [preserved source](../../repairs/theory-01/NUMERICAL_PROOF.md) | The positive-root equation, exact-rational endpoint argument, low-penalty affine branch, stable nominal-rate formulas and outward-rounded reverse ceiling are unchanged. Only display delimiters and the source footer differ. |

**Follow-up decision: no mathematical or scientific regression found in these
presentation repairs.** This review checks meaning and source differences;
the root's rendering and executable validation have separate evidence.

I also replaced the raw ket/bra pipe expression in this review's SU4 table with
plain wording, because GFM interprets literal pipes as table separators even
inside inline code. The repository's `verify_documents` check was run on this
complete report, including its local links and anchors, and passed. This static
check does not claim visual rendering or numerical/theorem validation.
