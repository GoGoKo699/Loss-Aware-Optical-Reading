# Current source map and contribution boundaries

The completed [predecessor comparison](audits/novelty-01/REPORT.md) is now integrated
into the main reading path. The [source inventory](audits/novelty-01/SOURCES.md)
records 21 primary references, inspected passages and retrieval limitations.
The [equation reductions](audits/novelty-01/REDUCTIONS.md) and
[claim map](audits/novelty-01/CLAIM_MAP.md) are preserved without modification.
This is a bounded literature comparison, not a worldwide priority certificate.

## Direct reductions that determine the framing

| Repository statement | Primary predecessor and locator | Use in this project |
|---|---|---|
| Single-photon phase-code reading | [Guha and Shapiro, 1207.6435v3](https://arxiv.org/abs/1207.6435), Eqs. (7)-(8) and loss discussion | Inherited mechanism. Keep the total-signal and per-pixel budget conventions distinct. |
| Fixed code decoder for a supplied input | [Eldar and Forney, quant-ph/0005132](https://arxiv.org/abs/quant-ph/0005132), Sec. 8.3 | Constant-diagonal Gram square-root criterion gives the decoder; R1 makes the substitution. |
| Error-free minimum-coefficient endpoint | [Chefles and Barnett, quant-ph/9807023](https://arxiv.org/abs/quant-ph/9807023), Eq. (3.15) | Direct Fourier-code specialization, Gram extension and input normalization; R2. |
| General input/measurement error-margin task | [Hashimoto and colleagues, 0912.2610](https://arxiv.org/abs/0912.2610), Sec. II | The general task is inherited. R3 isolates the additional normalized-input reduction for this loss/code model. |
| Uniform coherent fixed-alphabet curve | [Herzog, 1206.4412](https://arxiv.org/abs/1206.4412), Eq. (4.18) | Exact specialization with N=4, overlap exp(-t mu), and failure F; R4. |
| Filter followed by minimum-error discrimination | [Bagan and colleagues, 1206.4145](https://arxiv.org/abs/1206.4145), Eqs. (6)-(8) | Existing receiver method; the input-only result must additionally account for pre-device normalization and loss. |
| Binary spectral contrast | [Bouchet and colleagues, 2108.03755](https://arxiv.org/abs/2108.03755), Eqs. (1)-(3) | Our binary contrast is one half of their operator; R6. No general multiclass eigenmode optimum is inferred. |
| Nulling/displacement and click receivers | [Sidhu and colleagues, 2109.00008](https://arxiv.org/abs/2109.00008), Secs. 5.1-5.2 and Appendix B | Established receiver ingredients. R5/R7 distinguish their optimization from the all-source bound. |

The candidate contributions are the complete joint input-only retuning statement
and the multiclass optical source-class converse. The known uniform curve is
credited separately from the proof that changing the transmitter or intensity
mixture cannot improve it at the stated mean budget. Standard inequality and
statistical components are not separate novelty claims. [Contribution note](docs/CONTRIBUTIONS.md).

## Other relevant scope comparisons

[Nair and Yen, 1107.1190](https://arxiv.org/abs/1107.1190) already study optical
probe optimization in loss with a larger signal-idler class. That class is not
silently imported into our restricted photon theorem.
[Primaatmaja, Ho and Scarani, 2012.11104](https://arxiv.org/abs/2012.11104) include
a losses coda, Sec. V, and phase-reference distinctions. Their work must not be
characterized as purely lossless. Transmission amplitudes and probabilities
must be converted before comparing formulas.

[Melo and colleagues, 2411.14537v1](https://arxiv.org/abs/2411.14537) already scan
error/inconclusive tradeoffs using path-optical emulation with laser light and
cameras. That is not a measured signal-photon advantage over the allowed classical
source class, and it is not presented by us as one. Its declared emulation goal
is distinct from our proposed experiment.

Gram feasibility, pairwise overlap bounds, approximate unambiguous discrimination,
perturbation continuity and concentration also have predecessors. See S10,
S13-S14 and S19-S21 in the [full inventory](audits/novelty-01/SOURCES.md).
The bounded fixed-N test imports no optional-stopping guarantee from a time-uniform
reference and is not a new concentration theorem.

## Coverage and unresolved work

Relevant full-text passages were inspected for 18 of the 21 records; two recent
full texts were used only for formal scope screening. S18 and S21 were
abstract/bibliographic screens; S20 was checked indirectly through the explicit
attribution and equation in primary source S19. Those limited readings cannot
establish that the complete texts contain no related theorem.

Herzog, Bagan and Primaatmaja full PDFs were recovered after the earlier HTML
retrieval failures. The original source-audit text remains in the immutable
checkpoint-07 archive; its old retrieval gaps are not the current status.

Remaining concrete gaps are S18, *Efficiently Computable Strategies and Limits
for Bosonic Channel Discrimination*, full theorem/appendix comparison; S20,
*Upper bound for the success probability of unambiguous discrimination among
quantum states*, original full text; and possible equivalent multiclass
error/failure overlap bounds. The [next work order](work_orders/CURRENT.md)
sets a bounded follow-up. No absence claim is inferred from search failures.

## Hardware sources and evidence status

The project hardware documents ask about balanced path preparation, phase control,
separated optical sections, calibration, native conventions and simultaneous
readout. They are laboratory-review questions, not a confirmed inventory.
No cited paper's source or detector specifications are assigned to the intended
installation. [Lab brief](experiment/LAB_REVIEW.md).

The integrated comparison changes attribution and reader-facing framing, not
canonical proofs, numerical routines, the acquisition protocol or archived
results. Mathematical audit, predecessor coverage, external peer review, actual
calibration and experimental data remain separate. No release or license decision
is made by this source map.
