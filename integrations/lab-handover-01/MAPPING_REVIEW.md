# Independent mapping and record-adapter review

Date: 2026-09-15. Scope: new `scripts/lab_reference.py`,
`scripts/lab_records.py`, `tests/test_lab_reference.py`, `experiment/SU4.md`,
`experiment/SU8.md`, and `docs/THEORY_ROUTE.md`. Supporting inspection included
the canonical theory/protocol and existing four-label analyzer. No repository
files were edited by this review. This is an implementation/interpretation
review, not a calibration, theorem-extension study, or GitHub visual check.

## Findings and disposition

1. **Exact preparation-matrix convention mismatch, corrected during review.**
   The initial code changed the sign of the last Householder column, while
   SU4.md specified the correction on column 1. On embedded SU8 the initial
   generated preparation consequently differed from the stated `Uprep4 ⊕ I4`
   on unoccupied columns. The occupied first column and photon predictions were
   correct, but the exact target conventions disagreed. Root independently
   identified the same problem. The code agent changed the correction to
   column 1 and added an exact preparation embedding regression. Reinspection
   confirmed the full block matrix agreement, with maximum residual 0.0 for
   `p=(.1,.2,.3,.4)`, `eta=(.8,.7,.6,.2)`.

2. **Minor timestamp schema clarification, outstanding at this snapshot.**
   `SCHEMA['times']` says timestamps can be blank only for synthetic rows.
   Clock-defined real trials legitimately have no source-herald timestamp.
   Runtime validation already requires only real gate-open/gate-close fields,
   which is appropriate. Suggested wording: require gate timestamps on real
   records; source-herald time is optional when a clock defines the trial.
   This is a schema explanation issue, not a scored-trial accounting defect.

No other substantive mapping error was found in the reviewed slice.

## Checks actually executed

- `python -m unittest discover -s tests -p test_lab_reference.py -v`: **13 tests
  passed**, Python 3.12.14. This includes CLI generation/analysis, generated
  example manifests, all 256 embedded click masks, malformed record rejection,
  and refusal of native eight-label certification plans.
- Separate direct algebra checked each physical four-path hidden operation
  equals `I4−2|j><j|`, `D4=J4/2−I4`, and `D4 O_j (1,1,1,1)/2=e_j`.
- Unequal-loss four-path outputs matched the active SU8 block exactly; spare
  output amplitudes were zero in the ideal target and the corrected full
  preparation was `Uprep4 ⊕ I4`.
- Independently calculated coherent contrast: canonical operations give
  kappa=1; multiplying all operations by `exp(i*pi/4)` leaves kappa=1;
  flipping only one label's phase gives kappa=4/3. This checks the stated
  shared-phase warning quantitatively.
- Built Walsh8 independently as `H2 ⊗ H2 ⊗ H2`. It exactly matches the
  bit-parity code and satisfies integer `Z8.T Z8=8 I8`. Uniform input routes
  amplitudes to the declared integer labels 0–7; decoder determinant was
  0.9999999999999998 at floating precision.
- For both SU4 and embedded SU8 P2 targets, direct evaluation of
  `T O_j^SU alpha − c T alpha` left only the marked mode, with amplitude
  `−2 c sqrt(eta_j) alpha_j`. The displacement is independent of j and
  includes the common hidden compiler phase c. P2 has identity path routing
  after displacement, not the photon D4 receiver.

## Interpretation checks

- Native Walsh8 uses actual orthogonal phase codewords, not eight path flips.
  The photon rule is limited to its exact assumptions. The no-click failure
  branch has lambda at least 1/7; lower-penalty optima require vacuum guesses.
- Both chip pages distinguish compiled transfer verification from independent
  source/hidden-operation/receiver roles. T is stated to be attenuation, not a
  programmed phase unitary. Processor availability is confirmed; missing
  source/detector/interface information is not invented.
- The four-label SU8 adapter retains raw masks and diagnoses leakage before
  mapping affected attempts to failure. Native8 has separate descriptive
  accounting and cannot enter the four-label certificate path.
- Native8 makes no exact eight-label classical frontier or source-class
  advantage claim. The four-mode robustness results are not automatically
  extended to an imperfect eight-mode device.
- THEORY_ROUTE introduces full returned states including vacuum and C/E/F
  before optimization, distinguishes receiver optimality from source-class
  advantage, and preserves the candidate-A/derived-B hierarchy.

## Reviewed snapshot hashes

| File | SHA-256 |
|---|---|
| scripts/lab_reference.py | af9e99af8ce0f610606853c7681b81b303645ddd2e2faac1ae4513951b7e14da |
| scripts/lab_records.py | bf156123759b0ae17eb2c8f35805610d5bc28dca61e26527d3a85f73c5f4f70b |
| tests/test_lab_reference.py | 31ec6a31cc0aa9346c234ba947b0c42ff22c790d43d3e02fc93f699ba96fd50e |
| experiment/SU4.md | 2357cc9550d53cd3c953da2e36ea67399840b307cb6128522cc638f796aeca2d |
| experiment/SU8.md | 16f64f021804332731ae5a5536e287e3e8bca039e74a48627b4122c362b9dca9 |
| docs/THEORY_ROUTE.md | 23782cf35b99a9183258c2f4f3deb44e1d720a64580d9f87171461b866434612 |

These identify this read-only review snapshot, not a claim that subsequent
parallel edits or the final merge have been checked. Root's final-tree checks
and remote workflow verification remain separate.
