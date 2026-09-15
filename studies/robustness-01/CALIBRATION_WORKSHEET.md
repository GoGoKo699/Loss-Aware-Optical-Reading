# Initial laboratory tolerance worksheet

**This is a discussion and pilot-analysis worksheet, not authorization for a main
acquisition. No field below has been supplied by a laboratory.** The parent
`experiment/FIRST_EXPERIMENT.md` and its original five review questions remain
unchanged. Do not use the hypothetical screens in this study as device specs.

## First distinguish what needs correction from what needs a bound

| Observed deviation | Treatment | Evidence needed |
|---|---|---|
| Extra known diagonal path loss | Already in A; retune the input using the measured losses | Hypothesis independence, port convention, confidence/stability bounds |
| One common input/output unitary offset | Calibrate the same basis/target once | Same offset for all hidden labels and all points claimed to share a fixed receiver |
| Symmetric label-independent random phase noise | Use the exact dephasing preparation rule in this study | All pairwise coherence factors consistent with one v, phase means corrected, residual/model uncertainty bounded |
| Systematic error of the marked phase | Do not replace it by a visibility reduction | Actual phase-referenced maps for all four labels; quantify fixed-receiver regret or correct the phase bank |
| Distributed or rotated loss | Treat as a new map structure, not four fitted efficiencies | Location of the attenuation relative to encoding, calibrated complex maps, common-channel justification if used |
| Preparation or readout error | Charge it as implementation loss | State-preparation accuracy, complete click/erasure response, source and detector uncertainties |

Calibrating controls to implement the same intended decoder is allowed. Choosing
a genuinely different target receiver for each loss/error-penalty point must be
reported as receiver retuning. Label-dependent corrections cannot be applied
using the hidden answer. A basis correction common to a whole scan is a
cleaner comparison than a new correction fitted separately at each test point.

## Pilot inputs required before numbers become acceptance conditions

**Physical task.** Mark P0 (incident signal energy) and P1 (accessible unknown-device
output before our receiver). Identify which component produces each loss and
phase error. Confirm fresh uniform hidden labels, one charged use, no hidden-label
leakage, and storage of every gate's record.

**Calibration.** Supply all four complex maps against one common phase reference,
with a simultaneous test-time uncertainty model. State whether errors are static,
common random channels, slowly drifting, or label dependent. An averaged
amplitude matrix is not a substitute for a random channel. Photon-only freedom
to discard global phases must not be used to weaken the coherent-source ceiling.

**Preparation/readout.** Supply vacuum/one-photon/multiphoton statistics and an
incident mean-energy upper bound with a justified tail model; preparation phase
and amplitude errors; downstream efficiency, dark/multiple clicks, and stability.
Pump, herald and reference costs are separate. This study's numerical source is
a perfect one photon; it does not supersede the parent's imperfect-source model.

**Decision requirements.** Choose an acceptable absolute score-regret allowance
only after discussing scientific resolution. The example 0.01 in the report
means 0.01 units of C-5E per attempted interrogation, not one percent relative
error and not one percentage point of success probability. Choose independent
pilot/test separation and the existing predeclared statistical protocol.

## Two different pass conditions

### Mechanism / near-optimality

For the same calibrated device and allowed input class, obtain an upper bound U_J
on all joint strategies and a lower bound L_D on a feasible fixed strategy. With
simultaneous calibration and implementation allowances included, require

$$
U_J-L_D\le\Delta_{\mathrm{allowed}}.
$$

If the model exactly matches symmetric dephasing, the optimized ideal fixed
receiver is optimal, but source preparation and detector defects still reduce
the achieved score. A trace-distance preparation allowance delta_p contributes
at most 6 delta_p score error after any physical channel. A justified per-trial
record total-variation allowance delta_r contributes at most 6 delta_r.
Do not count the same attenuation or error in multiple allowances.

For an arbitrary small coherent-map residual of operator radius epsilon, the
conservative fallback is 24 epsilon for regret. Use the sharper structure or
measured-score upper/lower bounds when available. A failed loose upper bound
means insufficient certification, not necessarily physical failure.

An M1 scan can test a predicted input effect but cannot experimentally prove
optimality over all quantum measurements. That universal component comes from
a valid theorem or certificate.

### Nonclassical-source advantage

Independently require an unconditional observed lower score above the credited
classical ceiling with calibrated map and signal-budget bounds. Use the existing
finite-N procedure and source-tail accounting. Being optimal among one-photon
strategies does not imply exceeding the classical-source bound. Conversely, a
nonoptimal photon receiver can still exceed that bound.

The numerical `P1_illustrative` fields in RESULTS.json are only an ideal-source
screen (mean signal energy 1, uniform downstream survival 0.92, no dark counts).
They do not include realistic source or calibration allowances and use ordinary
floating-point exponentials. They are NOT acceptance certificates or replacement
plans. In particular they are not the old P1 forecast with mean upper budget 0.98.

## Decision record

| Decision | Criterion | Current status |
|---|---|---|
| Initial review | Existing physical interface can be meaningfully assessed | Documents ready; no lab response supplied |
| Pilot | Independently characterized source/maps/readout, without using main-test records | Not performed |
| Retain fixed target decoder | Near-optimality or adequate-task-performance allowance satisfied | No device-specific determination yet |
| Main P1 acquisition | Conservative predicted positive margin and predeclared test | Not approved by this study |
| Main M1 acquisition | Preparation-dependent effect resolvable above calibration/drift | Not determined |
| Redesign phase bank / receiver | A meaningful lower regret exceeds the selected allowance, or a correctable model error is identified | No hardware decision made |

The next useful input is one laboratory block diagram with the five original
answers and preliminary source/map/readout data. Do not start another broad
noise survey merely because those data have not arrived.
