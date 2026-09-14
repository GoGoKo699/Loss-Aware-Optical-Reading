# First experiment: test the boundary, not only a favorable interference pattern

Status: a self-contained design for initial laboratory review. No experiment has
been executed. All numeric device/source values below are hypothetical planning
inputs. The actual installation has not supplied the required calibration data.

## 1. Scientific question and completion standard

For a single-use four-symbol optical phase code, test whether changing only the
input amplitudes allows one fixed single-photon receiver to follow the predicted
reliability/loss tradeoff. At a preselected favorable point, certify a score that
no classical coherent-state mixture can match under the same incident signal
budget. At a separate severe-imbalance point, try to demonstrate an implemented
classical strategy above the upper bound for the entire specified four-path
single-photon architecture.

The primary result is not a VQA, a new learning paradigm, a speedup, or a claim
that a single photon always outperforms classical light. It is a decision-resource
comparison. The overall program may later extend to eight-mode codes and
multi-query tasks, but those are not assumed by this first experiment.

Positive result: a finite-data classical-probe exclusion with its assumptions
and confidence recorded. Reverse result: a finite-data exclusion of the ideal
one-photon/four-path class by a measured coherent receiver. Failure to certify
one does not establish the other. An unresolved interval remains unresolved.

## 2. Hardware baseline and the physical interface

Use the project's single-photon global-path setting. Four optical paths carry
one computational photon; the detector herald, if used, is outside the
computation. No synchronized multiphoton probe, auxiliary interacting photon,
quantum memory, recirculation, or adaptive optical quantum gate is required.

Physical order:

    source / preparation -> P0 -> hidden phase-and-loss section -> P1
                        -> fixed four-mode decoder -> four click detectors

P0 is the incident signal-energy accounting plane. P1 is the end of the declared
unknown device, before the optimized receiver. The ideal classical competitor
is granted any measurement from P1 onward. Do not reduce its allowed performance
by attributing losses in our chosen decoder/detectors to the unknown device.

The phase code consists of four actual physical operations:

    O_j=I-2|j><j|, j=0,1,2,3.

Exactly one pi flip is promised. There is no healthy fifth hypothesis. Call the
experiment four-symbol phase reading, not general optical fault diagnosis.

The fixed photon decoder is D=J/2-I. Preparation is a normalized amplitude vector
specified before the hidden label is selected. Its four path probabilities are
set by the theorem or a previously fixed calibration-based robust design.

The present project documents ask, but do not confirm, whether preparation and
receiver can occupy separate/cascaded sections. An arbitrary SU(4)/SU(8) compiler
alone does not supply this oracle interface. An answer-dependent compiled
end-to-end matrix is not an acceptable substitute.

An external bank of standard phase modulators/attenuators between a preparation
network and an existing four-mode receiver is eligible hardware. This is an
option for the lab to evaluate, not a claim that it is already assembled.

## 3. Two primary tests and one mechanism test

### P1. Certified nonclassical reading in moderate imbalance

Illustrative target: eta=(.7,.7,.7,.56), penalty lambda=5. Positive score means
C-5E. Compute the preparation from calibration before the test; for the nominal
ideal maps it is approximately

    p=(.24058994,.24058994,.24058994,.27823018).

The decoder remains D. One click means its port label; zero and multiple clicks
mean inconclusive. Keep all attempted gates in N.

The null is every nonnegative Glauber-Sudarshan mixture of coherent signal
states, any mixture label/phase reference, and any receiver, at the calibrated
mean signal budget. A measured weak coherent control is not the definition of
the null. Use the general transfer-map score upper bound from THEORY.md, not a
fit to the control's performance.

### P2. A genuine reverse comparison in severe imbalance

Illustrative target: eta=.7*(1,1,1,.05), lambda=5. Build the coherent nulling
receiver: select a known coherent illumination, displace the known unflipped
background after P1, and use one-click port identification. Never supply j to
the displacement controller.

This uses ordinary coherent reference light and couplers, not an extra quantum
probe photon. It is an additional classical receiver capability requiring lab
confirmation. Count reference power separately even though the theorem charges
only illumination crossing P0. Receiver coupling attenuation and imperfect
nulling remain in the measured probabilities.

For this point the ideal pure one-photon score ceiling is .1860224979. With the
illustrative simultaneous map error radius .003, a conservative upper ceiling
is .2220224979. An implemented coherent receiver exceeding that ceiling would
beat every allowed single-photon probe/measurement, not just our tested input.
It would not beat every possible quantum architecture.

If optical displacement is unavailable, do not replace P2 by direct laser
intensity measurements and call that the same comparison. P2 then remains a
theoretical negative region; the experiment's claim must be narrowed accordingly.

### M1. Input-only retuning with a fixed receiver

Use a medium-imbalance point, for example eta=.7*(1,1,1,.2). Compare the
unambiguous input p proportional to 1/eta, a uniform input, and the theorem's
inputs for lambda=1 and lambda=5, with the same D throughout. The weak-path
probability changes from .625 in the zero-error limit to approximately .193814
at lambda=1 and .457125 at lambda=5.

Test predicted C,E,F directly. Do not train the receiver on the held-out records.
This test exposes the new design rule even in regimes where classical probes
are competitive. It is not an independent quantum-advantage assertion unless
separately preregistered and corrected for multiplicity.

## 4. The first data set should support the larger scientific argument

Use a modest predeclared grid such as r in {1,.8,.5,.2,.05} at one attainable
good-path transmission t. Recalibrate the actual values; the numbers above are
not imposed hardware specifications. Include at least one favorable point, one
strongly unfavorable point, and an intermediate point where the preparation
changes substantially with the error penalty.

At each point retain the whole confusion matrix, all 16 click-mask frequencies,
and the unconditional C,E,F. Plot the exact photon frontier, exact classical
results where known, and certified upper/lower brackets elsewhere. Never plot
the general classical upper bound as if it were an attained exact frontier.

For uniform loss the entire theoretical classical and photon frontiers are
exact. The minimum-error classical point is an abstract achievable POVM; it is
not automatically implemented by the four click detectors. Label an unperformed
receiver comparison as theoretical.

A later eight-mode transfer experiment should use an actual orthogonal phase
code, not eight single-path flips. The proof extends to flat orthogonal codes,
but the calibration and classical bound must use their actual physical phases.
Do not enlarge the first apparatus merely to claim a mode-count extension.

## 5. Acquisition protocol and blinding

1. Prepare/calibrate without using test labels. Separate calibration, pilot,
   and held-out test records. Archive code, parameter files, and their hashes.
2. Independently sample the hidden label uniformly for EACH attempted
   interrogation. Do not reuse one fixed label for a long train of test photons
   and count those as independent single-use decisions.
3. Keep the label/controller record unavailable to source preparation and
   decision logic until the optical records are sealed. Save it separately for
   offline scoring. Do not allow the label to leak through timing/control logs
   received by the reader or an accessible optical side channel.
4. Wait for independently specified phase settling before opening the input
   gate. Accept a fixed, label-independent acquisition window. Define trials
   from an upstream clock/herald, never from successful output coincidences.
5. Record every counted attempt, including zero clicks, multiple clicks,
   missed photons, and predeclared integrity flags. Zero/multiple-click masks
   are failures, not removed rows. Record pre-exposure aborted cycles in a
   separate ledger and ensure they send no uncounted light into P0.
6. Close the exposure window and independently draw the next hidden label before
   another counted probe enters. The fresh draw may equal the previous label. A slow thermal phase bank may allow only one gated interrogation
   per setting. Determine the attainable rate from the lab, not the MZI update
   time alone. More than one uncounted probe at the same hidden setting invalidates
   both the dose accounting and potentially the single-use comparison.
7. Acquire exactly the preregistered N. Do not stop on first apparent significance.
   If a run is aborted for an independently defined hardware problem, preserve
   it and apply the predeclared whole-run rule. Do not remove unfavorable trials.
8. Unseal labels, apply the frozen decoder, and compute the registered scores.
   Configuration/model changes require a new held-out run and error allocation.

Exact balancing of label counts in short announced blocks is not the same as
independent uniform sampling. It can make later labels predictable. Use iid
uniform labels for the stated proof, or derive a valid alternate randomization
analysis before acquisition.

## 6. Calibration that the theory actually requires

### Signal energy and source

Measure or justify an upper bound on incident mean photon number at P0 per
counted attempt, including preparation losses, vacuum components, and high-number
tails. An output herald/coincidence cannot set this normalization.

Supply source P0/P1/multiphoton bounds, a mean-energy upper bound, the method and
uncertainty, and a stability/tail contract. A bound on g^(2)(0) or on the
probability of n>=2 alone does not bound its energy. Finite click samples cannot
rule out an arbitrary unbounded rare bright tail without additional metering or
source assumptions. Do not truncate a source tail and renormalize it away.

The theoretical classical null allows unbounded bright-pulse mixtures. A
physical energy-calibration model must have a justified coverage statement,
not an assumption silently borrowed from that theorem. Source acquisition rate,
herald photons, pump energy, and reference power are separate reporting columns.

### Phase-referenced channel maps

Characterize the complex maps A_j from P0 to P1 with a common optical phase
reference across labels. Fit residuals alone are not operator-norm confidence
radii. Supply a simultaneous calibration envelope that covers test-time drift.

Do not independently choose a convenient global phase for each fitted A_j.
Such phases are irrelevant to a lone photon's density operator but observable
to a coherent probe with a phase reference. One such phase change leaves the
quantum task unchanged but increases the ideal contrast bound from 1 to 4/3.

Compute kappa_U from the maps and their interval radii. A common calibrated
post-encoding noise channel is allowed, but averaging fluctuating amplitude
matrices and pretending the average is the complete channel can give a false
benchmark. Missing modes, spectral changes, and control side channels need bounds.

### Readout

Measure per-port efficiencies, dark probabilities per FIXED gate, dead time,
wrong-port leakage, stability, and exposure-independent setting behavior. Use
these to predict performance, not to subtract detector-caused wrong answers
from the certified empirical score. Multiple/no-click masks remain observable
failures. Record the detector model separately from the unrestricted classical
receiver bound at P1.

## 7. Preregistered statistics and run size

For the primary positive score, use lambda=5 unless pilot calibration supplies
a compelling reason to choose another value before the held-out test. The
conservative fixed-N lower bound is

    mean(score) - 6 sqrt(log(1/alpha_stat)/(2N)).

The upper classical score is

    (15/14)[1-exp(-kappa_U mu_U)],

capped at one. A chosen further subtraction for multiphoton contamination or a
separately certified model-error term is recorded, not fitted afterward.

Illustrative program-wide false-certification allocation:

- simultaneous energy/source and channel calibration failures: at most .0005;
- primary positive test: alpha_stat=.00025;
- primary reverse test: alpha_stat=.00025.

The two primary conclusions together then have a union-bound error at most .001
under their declared calibration/independence assumptions. These calibration
probabilities are design requirements, not properties supplied by the simulation.
Secondary plots receive descriptive intervals or a separate multiplicity plan.

Let g be the pretest conservative anticipated score gap. A minimal sizing rule
for a desired statistical radius <=g/2 is

    N >= 2(1+lambda)^2 log(1/alpha_stat)/g^2.

This is deliberately conservative and does not itself set the final N without
calibration. It is not a power guarantee if the predicted gap is wrong. The
laboratory pilot supplies the attainable operating region and rate.

Provisional example caps: 500,000 attempts for P1; 50,000 for P2; approximately
20,000 per non-primary characterization condition. Freeze revised counts after
pilot calibration and before examining held-out outcomes. If the apparatus cannot
reach the needed region/rate, narrow the experiment rather than secretly condition
on surviving photons. Time estimates require the lab's gated-trial rate.

## 8. Worked feasibility calculation, explicitly not data

For P1, use the following hypothetical inputs:

    nominal eta = (.7,.7,.7,.56)
    P_n = (.029,.97,.001) for n=0,1,2, no higher tail in this toy model
    incident mean = .972; conservative mean upper = .98
    combined post-device transmission and detector efficiency = .92 at all ports
    dark probability = 1e-6 per detector per gate
    common-distribution independent Gaussian path phases: sigma=.035 rad
    simultaneous per-map operator radius = .003
    lambda = 5, N=500,000

The exact finite-source counting model gives approximately

    C=.59005719, E=.000707285, F=.40923552,
    C-5E=.58652077.

The robust classical score ceiling is .53562201. The statistical radius for
alpha_stat=.00025 is .01727964. An additional .002 source-tail score subtraction
would still leave an anticipated gap of about .03162. This shows a nonempty
design region; it is not evidence that the lab can attain it or that an observed
run will certify an advantage.

For the illustrative P2 maps, a displaced coherent control with nominal mean incident
energy .99 and a calibrated upper bound of one, .92 combined post-device survival
and detection, residual Poisson background intensity 1e-4 per output, the same
sigma=.035 path phase noise, and the same dark probability has the score recorded
in results/hypothetical_design_forecast.csv (approximately .42648719). The conservative
photon ceiling is .22202250 before its own statistical allowance. This large
separation makes the negative test less fragile than trying to measure a crossing
at arbitrarily small error.

Vacuum dilution is a real readiness condition. With the positive-point optics
above but a simple vacuum/one-photon source, the expected score gap becomes
positive only near one-photon presence .695 under the illustrative energy
uncertainty; including the 500,000-trial statistical radius requires roughly .803.
These thresholds are model-specific, not source specifications. No-click
postselection is not a remedy when the source fails the readiness test.

## 9. Go/no-go before consuming a large test budget

Proceed to the held-out acquisition only when all of the following are resolved:

- a physical source -> hidden section -> fixed receiver interface exists;
- exactly charged, independently labelled one-use trial gates can be generated;
- calibrated maps retain a COMMON coherent optical phase convention;
- the source mean/tail bound and channel interval have defensible coverage;
- pilot data plus worst-case calibration permit a positive registered margin;
- P2 displacement hardware is feasible, or the scope explicitly drops its
  experimental comparison rather than replacing it with a weaker laser control;
- raw records, code hashes, trial masks, N, lambda, and stopping rules are frozen.

A full best-classical finite-error solution for arbitrary unequal loss is not a
prerequisite: a proved upper bound suffices for P1. Its exact frontier must not be
claimed. Likewise no adaptive multi-query theorem is needed for independent
single-use gates, and none is assumed.

## 10. What the lab should return at initial review

Return a block diagram with P0/P1 marked; preparation and decoder interfaces;
phase-setting and exposure-gating timings; whether all four outputs are recorded
simultaneously; source presence/mean/tail characterization and its uncertainty;
readout performance; a phase-referenced channel-calibration route; and whether a
four-output coherent displacement control can be assembled with existing
components. The lab need not execute a full experiment before commenting.

This document defines the scientific task and success criterion. It does not
substitute for the laboratory's detailed optical engineering, safety review,
calibration campaign, or confirmation of equipment availability.

## 11. File-level analysis contract

`templates/primary_plan.example.json` and `templates/reverse_plan.example.json`
are provisional, explicitly synthetic plan templates. The first excludes
classical probes; the second excludes the specified ideal single-photon class.
The CSV schema is in `templates/trials.csv`. Both tests use `src/analyze_trials.py`.
The program refuses unapproved real-data plans, missing trials, duplicated IDs,
and undeclared receiver or calibration changes. It cannot verify physical
calibration, hidden-label isolation, energy tails, or preregistration merely
because a JSON field says they were completed.
