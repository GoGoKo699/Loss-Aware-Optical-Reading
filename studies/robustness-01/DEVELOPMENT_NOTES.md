# Execution and bounded limitations

The continuation resumed an existing work-order commit, not a new scientific
branch. Main and that branch were read through the authenticated connector.
Container Git access was attempted and failed at DNS resolution. Current tool
discovery exposes read operations only; `create` discovery returned no tool, a
complete GitHub listing contained no write action, and a plugin-directory search
found the already installed GitHub plugin, not an additional connected writer.
Consequently this delivery is a local, repository-relative packet and patch.
It is not a claimed remote commit, CI run, or merged result.

No authenticated local checkout is claimed. The numerical work is newly written
and imports no canonical module. A prior repair archive was extracted into a
separate temporary working area for inspection but was not used as executable
input to the final study. The original uploaded archives are not overwritten.

## Exploratory numerical issue and response

An initial cutting-plane prototype requested a tighter 2e-9 spectral tolerance.
SciPy HiGHS returned `HiGHS Status 0: Not Set` on one imbalanced phase case. This
was not accepted as a bound or as evidence of failure of a physical strategy.
The final proposal search uses a 2e-8 stopping target and an explicit alternative
HiGHS IPM proposal if the first method fails. Two final cases record such a
proposal failure/retry in their `solver_events`. A stalled search may still
produce a usable bound, but only if its stored exact rational witness passes.

All reported upper bounds are checked after the numerical search with strict
exact rational Hermitian LDL. Each joint lower bound comes from a separately
constructed positive POVM with an exact checked completeness allowance, and an
exact rational score. The fixed-optics phase bounds check all 625 classical
assignments. Numerical solver tolerances are not the certification criterion.
No existing scientific tolerance was changed: the new search is independent
code with a separate contract and no modification to canonical tests.

During construction, the optional all-abstention strategy was made explicit in
standard-decoder screens. This avoids presenting a negative score as an optimized
choice when the zero-score answer is allowed. Early local runs remain in the
working area; the final reproducibility pair is identified by result hashes.
No old result is relabelled as a fresh final run.

The complete 41-case final calculation was executed twice into different new
directories. Its RESULTS.json bytes matched. The separate witness verifier does
not call any optimizer; its exact matrix and rational payoff checks supplement
independent direct optical propagation and uniform-loss closed-form checks.

The broadest common-downstream-loss bounds are intentionally not tight. The
phase-error bounds solve the finite rational diagonal-channel instances, not
arbitrary unknown physical maps. The analytic dephasing theorem and the generic
continuity bound have their stated continuous domains. Source imperfections,
calibration confidence sets, unequal dark-count/readout channels, and adaptive
interrogation of the same hidden setting are not silently absorbed into these
results. No laboratory or source-quality claim follows from their software PASS.
