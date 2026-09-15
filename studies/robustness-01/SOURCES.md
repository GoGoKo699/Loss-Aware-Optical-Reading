# Sources and attribution for the bounded robustness study

This is not a new novelty audit. Analytic results are written out in PROOFS.md;
finite-model claims rely on saved, checked witnesses. No third-party article or
code is redistributed. The following primary records were checked online during
this continuation; no theorem-level literature exclusion is inferred from their
abstracts.

1. **Project baseline.** `GoGoKo699/Loss-Aware-Optical-Reading` at
   `de73c9b094036b756d1ff008eaccbc52cec46207`: `proofs/THEORY.md`,
   `docs/CONTRIBUTIONS.md`, `docs/PHYSICAL_SETTING.md`, and the existing
   experiment and source records. The bounded work order is already committed
   as `ddb17c5040e17cb0078121081afe15de70158fe8` on `research/robustness-01`.
   Exact ideal-code optimality, the conservative map perturbation ceiling, and
   the credited all-classical source comparison are inherited baseline inputs.

2. **Yonina C. Eldar, Alexandre Megretski, George C. Verghese.**
   *Designing Optimal Quantum Detectors Via Semidefinite Programming*,
   [arXiv:quant-ph/0205178](https://arxiv.org/abs/quant-ph/0205178),
   DOI [10.1109/TIT.2003.809510](https://doi.org/10.1109/TIT.2003.809510).
   The primary record establishes the prior detector-SDP framework. This study
   derives its own restricted joint diagonal-channel formulation and explicit
   dual inequality; it does not claim to invent semidefinite detector design.
   Scope inspection here: primary abstract and bibliographic record, not a new
   full-text equation-by-equation comparison.

3. **Yonina C. Eldar.** *Mixed quantum state detection with inconclusive results*,
   [arXiv:quant-ph/0211121](https://arxiv.org/abs/quant-ph/0211121),
   PRA 67, 042309 (2003). Inconclusive measurement optimization is established.
   Primary abstract/record inspected. No new generic error/inconclusive principle
   or claim that this article proves the complete input-retuning extension.

4. **Ryan Hamerly, Saumil Bandyopadhyay, Dirk Englund.**
   *Accurate Self-Configuration of Rectangular Multiport Interferometers*,
   [arXiv:2106.03249v2](https://arxiv.org/abs/2106.03249v2),
   Phys. Rev. Applied 18, 024019 (2022). The primary record describes calibration
   in the presence of fabrication errors using external sources/detectors.
   Used only to credit calibration as an established engineering activity. It
   supplies no tolerance, inventory, or calibration guarantee for our laboratory.

The phase-noise and systematic-phase examples are explicitly defined models,
not measured facts taken from these sources. The exact dephasing result is a
short extension of the baseline positivity argument. The dual/LDL constructions
are standard optimization/certification techniques applied to this task.
No independent priority or publication-significance claim is made for these
supporting results. This stage does not reopen the completed S18/S20 audit.
