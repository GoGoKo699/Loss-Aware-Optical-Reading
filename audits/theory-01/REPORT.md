# Independent theory and certificate audit

**Disposition: the core mathematical claims support the planned experiment under
their stated assumptions. Three limited corrections are required. The audit is
complete; the corrections have not been applied to canonical files.**

Target: `d07e4e2180992ab52ee08d0a0cad689154d2e9bd`.
Branch: `audit/theory-01`. Authority: the bounded `work_orders/CURRENT.md` at that
target and the user's instruction to proceed. No merge, research extension,
publication, novelty clearance or laboratory execution is included.

## What was checked

| Claim | Audit conclusion | Main reason |
|---|---|---|
| Global photon support bound for arbitrary positive diagonal loss and a flat orthogonal code | Supported | A measurement-independent upper argument and an attaining input/decoder; a second full Hermitian dual check |
| Complete photon error/inconclusive frontier | Supported | Vacuum decision segment, strict monotonicity of the unequal-loss curved branch, and the zero-error limit |
| Classical finite-error bound for calibrated passive maps | Supported | Coherent overlaps, POVM Cauchy-Schwarz, and explicit input/output normalization |
| Extension to arbitrary labelled coherent mixtures at a mean budget | Supported | Concavity/Jensen without a peak-energy or photon-number cutoff |
| Exact uniform four-symbol classical frontier | Supported | Matching general upper bound and a constructive Gram-matrix POVM, including the zero-energy limit |
| Operator-norm calibration bound and phase-reference requirement | Supported | Stacked-map norm bound; independent gauge-change check |
| Reverse comparison against the specified one-photon class | Supported in the declared model | Trace-distance perturbation plus score range; numerical domain caveat F02 below |
| Fixed-N score certificate and conditional-energy version | Supported with the stated conditions | Independent bounded-mgf derivation and a negative control showing why grand-average energy is insufficient |
| Source/detector forecast and trial accounting | Consistent in the tested model | Independent multinomial/Gaussian quadrature calculation; all click masks and malformed-record controls |
| Exact arbitrary-loss classical finite-error optimum, multi-query advantage, hardware feasibility or novelty | Not evaluated as established results | These remain outside the proved/authorized scope |

See [INDEPENDENT_DERIVATIONS.md](INDEPENDENT_DERIVATIONS.md) for the actual
reconstruction. This audit is not merely a rerun of the inherited validator.
It is also not an outside specialist's peer review or a formal proof-assistant
certificate.

## Findings requiring separate correction

### F01. The displayed score cap is a false chained inequality

**Severity: low; affects the written universal statement, not the implemented
primary-test formula.**

`proofs/THEORY.md`, section 4, currently writes

$$
S_\lambda\le K_\lambda[1-e^{-\kappa\mu}]\le1.
$$

The last inequality is false in general. At m=4, lambda=5 and kappa mu=3, its
middle expression is `1.0180852838915744`. The correct combined bound is

$$
S_\lambda\le\min\{1,K_\lambda[1-e^{-\kappa\mu}]\}.
$$

`classical_score_upper` already implements that minimum. The planned primary
positive ceiling and its recorded synthetic score do not change. Correct the
written statement in a separate patch; do not describe the middle expression
as itself bounded by one.

### F02. The photon support routine accepts numerically unsafe penalties

**Severity: medium for a reusable certificate library. No failure found at the
planned lambda=5 operating points.**

`src/theory.py:photon_score` accepts every finite nonnegative penalty. It computes
E by subtracting C from the survival probability, then forms C-lambda E. For
large penalties, cancellation can invalidate the returned optimal-support value.

An explicit input in this audit environment is

```
eta = [0.2, 0.4, 0.8, 0.9]
lambda = 1e15
returned score = 0.35012265158564393
80-digit independently reconstructed optimum = 0.4056338028169016
feasible zero-error score = 0.4056338028169014
```

A purported upper value below an explicitly feasible score cannot be used as a
certificate. The separately returned double-precision eigenvalue is also
inaccurate here (`0.47463959682499995`), so replacing the subtraction by that
number alone does not solve the general issue. Stress cases through lambda=1e18
are preserved; exact failing values can vary with numerical environment.

This is a numerical implementation defect, not a counterexample to the photon
theorem. A repair should either reject unsupported numerical regimes or use a
stable calculation with an outward-safe error allowance. A useful stable identity
for the error is

$$
E=\frac1m\sum_{i<k}(\sqrt{\eta_i p_i}-\sqrt{\eta_k p_k})^2,
$$

but that identity by itself is not a complete certified-rounding policy. Merely
flooring the answer at the harmonic mean would not certify the true optimum at
finite lambda. Add independent high-precision regression cases and an explicit
accepted-domain rule. No such repair was performed during the audit.

### F03. One code docstring uses the wrong classicality shorthand

**Severity: low; terminology inconsistency, no change to the proved benchmark.**

`src/theory.py:classical_uniform_frontier` says 'Includes positive-P mixtures'.
The scope section correctly distinguishes a nonnegative diagonal
Glauber-Sudarshan distribution from the doubled-phase-space positive-P
representation. The latter is not the intended restriction to classical optical
states. Use the explicit source-class name in the docstring as well. The formulas
and the main proof already use the correct class.

## Operational assumptions verified, not removed

The positive comparison allows arbitrary receivers, phase references and rare
bright coherent pulses. It does not become a comparison with the laboratory's
particular weak-laser receiver. The negative comparison excludes only one photon
in the tested paths; no occupied bypass, idler or additional interrogation was
silently added to that class.

Every attempted interrogation receives a fresh hidden uniform label. Its source
and receiver must not obtain that label. Every failed, no-click and multiple-click
attempt remains in the denominator. The same fixed decoder is used independently
of the answer. The signal budget is at P0, and our downstream receiver loss does
not reduce the competitor's allowed performance at P1.

The fixed-N guarantee requires an iid source null or the declared conditional
predictable-energy contract. A run-level mean alone is insufficient. The audit
constructs an excluded non-iid source with 90% vacuum runs and 10% bright runs:
a misapplied 1% test would falsely reject with probability at least 9.556% in the
example. That is a boundary stress test, not a contradiction of the correctly
stated theorem.

The proposed Gaussian phase noise is safe to treat as a common post-encoding
channel only if its law really is independent of the hidden label. The separate
small map-radius example is not a deterministic envelope for unbounded Gaussian
phase draws. The laboratory must identify which uncertainty model its calibration
supports. An approval field in a JSON file cannot supply that evidence.

No plot or simulation can establish a mean-energy bound against arbitrary source
tails. That bound still needs independent metering or a validated source model.
The all-energy theoretical classical benchmark assumes the declared passive map
model on the permitted pulses; extrapolating a finite-power calibration to every
pulse energy is an external physical assumption.

## Independent computations

The audit's separate diagnostics passed **998 checks**, with the complete results
and numerical certificates preserved in the evidence archive. They include:

- 75 photon input/score cases across dimensions 2, 3, 4, 5 and 8, with complex
  Fourier codes, arbitrary nonoptimal POVMs and all frontier branches;
- seven full-Hermitian discrimination-dual calculations, using spectral cutting
  planes and linear programs, followed by explicit positive-semidefinite repair;
- 80-digit scalar solutions independent of the canonical eigensolver;
- constructive uniform-loss classical POVMs and random complex passive-map tests;
- labelled intensity mixtures and flash-pulse energies up to 1e16 at a fixed mean budget;
- calibration and trace-distance tests; exact finite score convolutions; all
  16 detector-mask accounting checks and eight malformed-plan/record cases;
- independent quadrature, multinomial occupation and dark-mask enumeration for
  a nonuniform source/detector case.

The largest primal/dual gap was `1.1606256511420554e-08`, below the declared
`3e-6` diagnostic tolerance. Every repaired dual matrix was explicitly checked
against every payoff operator; minimum constraint eigenvalues were about `1e-10`.
The largest other algebraic/probability residual was `1.7928372785222699e-12`.
These are floating-point certificates, not interval-arithmetic proof objects.
There was no dedicated SDP package: the independent search used SciPy HiGHS LPs
with full Hermitian spectral constraints. None of the analytic claims rests on
this finite search.

A second new-directory run reproduced the complete independent check ledger and
diagnostic data byte for byte. Runtime metadata was not required to match.

The normal, unmodified safe reproduction wrapper also passed all **5,261 inherited
checks** and the frozen-reference comparison. Its largest table difference was
`4.720057678042622e-12` within the declared `1e-8` tolerance. This regression is
kept separate from the independent evidence. Checkpoint-06's archived proofs and
original regression evidence were preserved; its entire separate theorem package
was not newly re-audited here.

## Access, preservation and numerical-development record

GitHub connector reads established the exact main commit and created the audit
branch. Container Git access failed at DNS resolution, so no authenticated local
clone or clean Git worktree is claimed. Numerical work used a new disposable
snapshot reconstructed from the supplied checkpoint archive and the exact remote
I/O perimeter. The source manifest and both reproduction scripts were matched
byte-for-byte to their remote Git blob IDs. All 39 protected source members were
verified before and after execution. The baseline archive SHA-256 remained
`e2bd57686376549342881a5d0348b16820ebbdab094b8d72df05a6836dbad016`.

Development of the independent diagnostic had three unsuccessful preliminary
runs, preserved in the evidence. The first hit an LP numerical stop; the second
produced a valid but insufficiently tight repaired dual; the third exposed
ill-conditioning in the audit's weak-energy Gram square root. The final method
uses justified photon/vacuum pinching, an alternate LP method on failure, and a
stable symmetric Gram square root. No canonical scientific file or diagnostic
tolerance was loosened to absorb those failures. The final two runs passed.

The audit's new output is confined to `audits/theory-01/`. Canonical proofs, source,
experiment protocol, archive manifests, frozen results and the READY work order
are unchanged. Branch CI checks the existing baseline regression; it does not
by itself certify that these independent diagnostics ran remotely. The archived
independent runs were performed in the stated local runtime.

## Decision and next boundary

The audit supports continuing the project with the stated four-path physical
model and lambda=5 first-experiment design. It does not support calling the
software an unrestricted, numerically certified implementation for every finite
penalty until F02 is repaired. Fix F01 and F03 alongside that bounded repair,
then rerun both the old regression and the independent cases. Preserve the old
source and numerical evidence.

Calibration, optical-interface feasibility, independent outside peer review and
theorem-level novelty remain separate tasks. The source check recovered one
previously inaccessible full text but did not perform the authorized-next novelty
study. No release, license change, experiment or manuscript was produced.

**Stop condition reached: audit packet committed for review; no merge and no
canonical repair.**
