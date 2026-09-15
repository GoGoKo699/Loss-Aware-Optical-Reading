# Uncertainty and readiness worksheet

**Both the SU(4) and SU(8) chips are available.** This page lists the supporting
interface and calibration inputs still needed. Blank entries mean unsupplied
information; they do not negate processor availability or prevent running the
self-contained reference calculations and planning commissioning.

Use this worksheet with [interfaces](INTERFACES.md). The completed robustness
study's more detailed [calibration worksheet](../studies/robustness-01/CALIBRATION_WORKSHEET.md)
and [local guide](../docs/ROBUSTNESS_GUIDE.md) explain which model each uncertainty
can support. Its examples are not measurements of either laboratory chip.

## Fill these fields for each proposed arrangement

| Input to supply | Required detail and boundary | Needed for |
|---|---|---|
| Logical/physical mode map | Actual input/output connector and detector ordering; matrix direction and units | All physical commissioning and tests |
| Compiler convention | Transpose/conjugate rules, phase gauge, determinant handling and independently accessible sections | All routes; common hidden phase is essential for source comparison |
| Wavelength/polarization | Operating wavelength, bandwidth, polarization and defined temporal/spectral modes | Transfer calibration and all subsequent claims |
| Independent roles | Physical preparation, hidden phase/loss, receiver and readout blocks; isolation of the current label | M1/P1/P2 and genuine native-eight interrogation |
| Connections | Inter-chip port map if used, path/phase stability, coupling loss, crosstalk and accessible extra modes | Any proposed two-chip arrangement |
| P0 source law | Vacuum/one-/multi-photon contributions per charged attempt; herald/clock definition | Photon mechanism and resource comparison |
| P0 energy guarantee | Upper mean including unbounded-tail treatment, method, uncertainty coverage and test-time stability | P1/P2 certification |
| P0-to-P1 maps | Complex maps for all physical labels in one optical phase convention; accessible outputs explicitly defined | Benchmarks for the actual task |
| Map uncertainty | Simultaneous norm/channel envelope and coverage over held-out trials; drift and missing modes addressed | Certified P1/P2; model comparison in M1 |
| Receiver and readout | Actual target, per-port efficiency, dark probability per fixed gate, dead time, leakage and nulling error where applicable | Forecasts and complete empirical scores |
| All-attempt data | Unique IDs, raw masks/time tags, integrity flags, no-exposure abort ledger and sealed label join | Every scientific run |
| Timing and randomization | Phase settling, one gated exposure per fresh independent hidden draw, source/reader isolation | Single-use interpretation and statistics |
| Pretest plan | Pilot/test separation, fixed N, penalty, confidence allocation, calibration hashes and whole-run abort rule | Certified acquisition |

Do not infer those entries from SU(4)/SU(8). A measured `g^(2)(0)` or a bound
on multiphoton probability alone does not bound high-number tail energy.
Finite click samples cannot rule out arbitrarily rare sufficiently bright
pulses without an independently justified energy/tail model. The allowed
classical comparator still includes such mixtures under its declared mean
signal budget.

## Which error changes which conclusion?

| Observation or model | Correct use | What it does not establish |
|---|---|---|
| A common, known calibratable basis change | Identify whether it can be absorbed into preparation and receiver under the study's assumptions | That every unknown basis drift is harmless, or that the original receiver is automatically still optimal |
| The specified symmetric dephasing model | Use only its defined channel, parameter regime and proved bounds | A result for arbitrary phase noise, correlated drift or every eight-mode chip |
| Systematic marked-phase bias | Use the study's four-mode physical operation and fixed phase convention | Permission to erase label-dependent global phase or replace a biased phase by an ideal pi flip |
| General map deviations | Apply only the norm/channel envelope that was actually justified | A confidence interval derived merely from fit residuals |
| Distributed-loss examples | Diagnose why a single ideal diagonal `T` may fail to describe the actual device | Four independently adjustable loss knobs, or an automatically tight noisy-channel optimum |
| Noisy measured fixed-receiver score | Achieved performance with every attempt included | The globally optimal receiver score or information irretrievably lost by the channel |

Keep three quantities separate: loss of distinguishability in the returned
ensemble, regret from retaining a particular receiver, and failure to implement
its programmed target. Optimizing a simulated receiver may expose regret, but
does not recover information lost to an inaccessible environment. An exact
finite-model certificate is exact for that declared model; a numerical proposal
is not a universal proof, and neither is a physical calibration certificate.

The four-mode study does not by itself certify native eight-mode Walsh noise
or leakage from the embedded four modes into other accessible outputs. Use
the ideal code theorem where its assumptions hold, and a separately justified
actual-map uncertainty treatment where they do not. Do not transfer a
four-mode numerical tolerance into an eight-mode apparatus specification.

## Planes, phase and score accounting

Mark P0 immediately before the hidden device and P1 immediately after it,
before the receiver. Downstream chip/decoder/detector loss lowers our achieved
score; it cannot silently lower a competitor allowed a different receiver.
Preparation losses affect the signal actually arriving at P0. Record signal
illumination, herald photons, pump energy, reference power, apparatus energy
and wall-clock time separately.

Calibrate all physical hidden maps with a shared phase reference. Independent
global phases for different fitted maps can change the coherent discrimination
problem. Even one common SU phase must be matched by the P2 nulling reference
or explicitly compensated. Intensity-only agreement is insufficient.

Report `C,E,F` per attempted interrogation, with `C+E+F=1`. No-click,
multiple-click, spare-port leakage and predeclared rejected exposed records are
failures, not rows removed from N. For SU8 embedding preserve all 256 masks
before the four-label adaptation; native8 uses a distinct eight-label record.
Do not let an output coincidence create the trial denominator retrospectively.

## Readiness without invented hardware values

The lab can begin an applicable [classical-light setup check](COMMISSIONING.md)
once it identifies compatible illumination/readout and its existing chip's
control/port interface. Reference calculations already run without hardware.
This establishes targets and diagnostic measurements, not certified readiness.

Before consuming a held-out P1/P2 trial budget, resolve the independent hidden
section, valid P0 source/energy and P0-to-P1 map envelopes, blinding/timing,
complete records, conservative anticipated gap and fixed statistical plan.
The P2 receiver must actually implement displacement. Keep the preserved
provisional caps and confidence allocation until a pilot-based plan is frozen
before test outcomes; do not use the illustrative values as calibration.

The controlling [first-experiment protocol](FIRST_EXPERIMENT.md),
[canonical proofs](../proofs/THEORY.md), and
[numerical contract](../docs/NUMERICAL_CONTRACT.md) state the statistical and
arithmetic boundaries. A software pass checks supplied records and calculations;
it does not establish external calibration coverage, label isolation,
source-tail bounds, or a valid no-optional-stopping acquisition.
