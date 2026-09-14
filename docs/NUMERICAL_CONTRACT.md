# Numerical contract after theory audit 01

The analytic photon theorem has not been narrowed. Its reusable implementation
now declares a numeric domain instead of accepting every finite penalty.

## Accepted inputs

For `photon_score`, `photon_secular`, `photon_frontier`, `support_interval`, and
the reverse-test photon bound:

- 2 through 64 modes;
- each binary64 transmission in [1e-12, 1];
- each binary64 penalty in [0, 1e18].

The reference environment uses IEEE-754 binary64 Python floats. Unsupported
inputs raise `PhotonNumericalDomainError` (a `ValueError` subclass), not a clipped
answer. These are conservative implementation limits, not experimental
thresholds or counterexamples outside the analytic theorem. Frontier points
requiring a larger penalty are rejected; the explicitly requested zero-error
endpoint remains available. This does not change the physical access model.

## Estimates and upper bounds are different outputs

`photon_score` returns nominal `C`, `E`, `F`, and an approximately attaining
preparation `p`. These are evaluated with 90-digit decimal arithmetic and then
converted to binary64. They are not individually outward-certified intervals.
The returned `matrix` is a compatibility/diagnostic field, not a stable way to
recover an eigenvalue at enormous penalties.

`score` and `eigenvalue` are stable point estimates. Do not use them as rigorous
upper bounds. `score_lower` and `score_upper` enclose the mathematical optimum
for the supplied binary64 inputs. The endpoints come from exact rational signs
of a monotone scalar equation, not a finite high-precision agreement test.
The lower endpoint bounds the optimum; it does not certify the rate of the
rounded preparation actually sent to hardware.

At the floating representation of lambda=1/(m-1), the nominal API retains the
inconclusive-vacuum recipe, as before. The bound calculation uses the exact
rational threshold. Thus the boundary's nominal score can differ from the
exact binary-input optimum at rounding scale; the certified endpoints still
cover the latter. This convention preserves the intended frontier bookkeeping.

`certify_reverse_counts` uses `score_upper` and outward-rounds the sum of that
bound with 2(1+lambda) times the supplied operator radius. It does not derive an
upper bound from rounded C-lambda E or a cancellation-prone matrix eigenvalue.
The documented radius must already cover physical uncertainty; this numerical
step does not estimate calibration error from data.

## Stable error and support calculations

The error is evaluated as a sum of squared amplitude differences, not by
subtracting two nearly equal probabilities. This prevents small subtraction
noise from becoming a large score error when multiplied by lambda.

The separate float secular routine is only a diagnostic; the certificate does
not rely on it. Exact-rational endpoint signs and direction-checked float
conversion establish the support enclosure. See
[the numerical proof](../repairs/theory-01/NUMERICAL_PROOF.md).

## What is not machine-certified by this change

This is not a formal verification of Python, the complete statistical pipeline,
or the optical apparatus. The classical exponential ceiling, Hoeffding logarithm,
reported p-values/confidence quantities, and nominal optical forecasts retain their
existing floating-point implementation. Their analytic assumptions still apply.
Only the photon-support bound and the indicated additive perturbation step acquire
exact-rational/outward rounding in this repair. Decisions with margins comparable
to numerical rounding should not be treated as experimentally established facts.

## Preservation

Original source bytes are still in the original ZIP and `IMPORT_MANIFEST.json`
is unchanged. A separate old/new hash record authorizes the canonical repairs.
Old result files remain unchanged. New runs retain the same 5,261 check identities
and tolerances; method metadata now discloses the rational enclosures. The original
998-check audit is rerun on historical source, while its scientific cases and new
fix regressions are run on repaired source. Historical defect assertions are not
silently rewritten in the preserved audit.
