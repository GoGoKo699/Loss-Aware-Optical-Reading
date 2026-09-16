# Laboratory recipe review

Reviewed commit `ba00d9ce64333ad08ef3b61108aa6df959cc5fc7`, tree
`605719db8b64ec45d75454dbe4338d56140d8593`, on branch
`audit/final-handover-01`. The initial worktree was clean. Review date:
2026-09-16. No pre-existing repository file was modified by this review.

**Result: the documented reference calculations and teaching-record adapters
pass this bounded review. No release-blocking recipe or matrix defect was
found. This is readiness for software reference use and laboratory planning,
not a finding of readiness for certified acquisition.** No instruments,
acquisition interfaces, vendor drivers, or network services were invoked.

## Scope and exact execution record

Read `AGENTS.md`, `experiment/INDEX.md`, `SU4.md`, `SU8.md`,
`COMMISSIONING.md`, `M1.md`, `P1.md`, `P2.md`, `INTERFACES.md`,
`UNCERTAINTY.md`, and `examples/lab/README.md`, together with
`scripts/lab_reference.py`, `scripts/lab_records.py`, their laboratory unit
tests, the delegated four-label analyzer, the two example plans, and relevant
reproduction/protocol sections. The full unit suite and main scientific and
robustness reproductions belong to the coordinating review and were not
duplicated here.

All **32 literal reference/analyzer commands** in those reader pages were
executed successfully. Both documented P1/P2 SU8 prose substitutions were also
generated and analyzed, adding four successful commands. The exact original
line, source page and line number, actual argument vector, exit code, stdout,
stderr and elapsed time are preserved in [RECIPE_COMMANDS.json](RECIPE_COMMANDS.json).

Only these path/interpreter substitutions were made:

| Literal component | Executed component |
|---|---|
| `python` | `/workspace/scratch/d29a6922cf06/ci-env/bin/python` |
| `results/runs/` prefix in output and dependent trial paths | `/workspace/scratch/d29a6922cf06/final-handover-01-runs/recipes/` |
| Working directory | `/workspace/scratch/d29a6922cf06/repo` |

Committed example input paths were retained verbatim. Every normal destination
was fresh. The interpreter is the recorded Python 3.13.5 environment with NumPy
2.3.5, SciPy 1.17.0 and mpmath 1.3.0.

| Source | Literal commands | Result |
|---|---:|---|
| `experiment/INDEX.md` | 3 | 3 exit 0 |
| `experiment/SU4.md` | 3 | 3 exit 0 |
| `experiment/SU8.md` | 5 | 5 exit 0 |
| `experiment/COMMISSIONING.md` | 4 | 4 exit 0 |
| `experiment/M1.md` | 4 | 4 exit 0 |
| `experiment/P1.md` | 2 | 2 exit 0 |
| `experiment/P2.md` | 2 | 2 exit 0 |
| `examples/lab/README.md` | 9 | 9 exit 0 |
| P1/P2 explicit SU8 prose variants | 4 additional | 4 exit 0 |

The default sample has 256 attempts. Generated forecasts retain
`HYPOTHETICAL_MODEL_NOT_LAB_DATA`, rows retain
`SYNTHETIC_NOT_AN_EXPERIMENT`, and the documented analysis commands return
`DESCRIPTIVE_ONLY`. They do not accidentally produce a source-class certificate.

## Independent mathematical and record checks

[RECIPE_CHECKS.json](RECIPE_CHECKS.json) records **193 checks, all passing**.
These were direct checks of generated objects, independent calculations, and
explicit adversarial adapter calls; they were not a second execution of the
repository unit suite. The largest observed matrix/numeric residual was
`4.440892098500626e-16`, against the review's `8e-14` floating-point comparison
threshold. This comparison does not change any repository scientific tolerance
or establish an interval certificate.

- Reconstructed `D4 = J4/2 - I4` and the four individual marked-path operations
  independently. Checked the preparation's first column, unitarity,
  determinant-one compiler representatives, shared hidden phase and ideal
  label-to-port routing.
- Reconstructed Walsh8 by integer Sylvester recursion, independently of the
  implementation's bit-parity construction. Integer orthogonality is exact.
  Checked all eight physical operations, the decoder, port order, preparation,
  determinant-one targets and native label routing. This is the Walsh code,
  not eight individual flips.
- Compared generated SU4 and embedded SU8 M1/P1/P2 targets. Active blocks agree;
  preparations are `Uprep,4` plus a spare identity block; spare incident and
  output amplitudes are zero in the ideal target. Loss is retained as a
  nonunitary device contraction. The spare identity is a reference convention,
  not a calibration claim.
- Checked every commissioning transfer CSV entry against independently
  composed `D T O_j Uprep`, including output-row/input-column conventions.
  There are 64, 256 and 512 entries for SU4, embedded SU8 and Walsh8 respectively.
  All are marked `TARGET_NOT_A_MEASUREMENT`.
- Checked P2 identity routing and matched common-SU-phase displacement directly:
  every unmarked output is nulled. P2 does not use `D4` as its nulling receiver.
- Independently solved the native-eight documented nonuniform eigenproblem.
  At `eta=(.7,.7,.7,.7,.7,.7,.7,.14)` and penalty 5, the result is
  `p_strong=0.1090574612051167`, `p_weak=0.23659777156418352`,
  `C=0.5597246158740043`, `E=0.007780632050053082`,
  `F=0.43249475207594257`, and score `0.5208214556237387`.
  These agree with the exported specialization and rounded page values.
- Recomputed all generated manifest hashes and independently counted every
  generated default record. Counts, N, full-width mask histogram and synthetic
  status agree with the generated summaries.

| Exhaustive fixture: hidden label 0, one row per mask | N | Correct | Wrong | Inconclusive |
|---|---:|---:|---:|---:|
| SU4, all 16 masks | 16 | 1 | 3 | 12 |
| SU8 embedding, all 256 masks | 256 | 1 | 3 | 252 |
| Native Walsh8, all 256 masks | 256 | 1 | 7 | 248 |

The embedding maps masks 16, 17 and 128 to failure while preserving their raw
values and full histogram; upper bits cannot turn into an active success.
A separate five-row fixture retained no-click, multiple-click, spare-click
and integrity-rejected events, yielding `N=5` and counts `1/0/4`.

Malformed in-process records were refused for out-of-range and negative masks,
noninteger masks, invalid labels/mode count, unknown quality flags, empty and
duplicate IDs, missing required fields, empty input and real records with
missing gate timestamps. Both generator and analyzer were also invoked against
existing output directories: they refused with nonzero exit and every existing
file remained byte-identical.

The unchanged P1/P2 plans were invoked on 256-attempt samples for both SU4 and
embedded SU8. All four calls refused the short sample before creating output,
requiring exactly 500,000 or 50,000 attempts as appropriate. Walsh8 refused a
four-label certification plan. No provisional cap or confidence allocation was
changed. These seven expected-failure CLI calls are included in
`RECIPE_CHECKS.json` with actual commands and refusal messages.

The default SU4 and SU8 embedded samples agree exactly by recipe:

| Recipe | Correct | Wrong | Inconclusive | N |
|---|---:|---:|---:|---:|
| M1 penalty-5 teaching sample | 97 | 1 | 158 | 256 |
| P1 teaching sample | 139 | 0 | 117 | 256 |
| P2 teaching sample | 92 | 0 | 164 | 256 |

M1's forecast compares all four preparations, while its compact trial file
samples the identified penalty-5 condition. The page explicitly explains this
boundary; the single teaching sample is not evidence for a multi-condition
mechanism experiment.

## Compact example regeneration

Regenerated **all six committed examples** with the documented seed 20260915
and 64 attempts, then analyzed every regenerated sample: 12 further commands,
all exit 0. [RECIPE_COMPACT_REGEN.json](RECIPE_COMPACT_REGEN.json) preserves
their exact argument vectors, results, old/new file hashes and comparisons.

`target_matrices.json`, `synthetic_trials.csv`, `synthetic_summary.json`,
`RECORD_SCHEMA.json`, and all applicable commissioning transfer CSV files are
byte-identical to the committed examples. Each `forecast.json` differs only in
its recorded Python version, 3.12.14 versus 3.13.5. After removing the environment
object, forecasts are identical with zero numeric difference. Consequently a
new manifest has a different forecast hash; no historical example or manifest
was rewritten.

Overall, this sub-review executed 48 successful recipe/analyzer commands and
seven deliberately refused CLI commands.

## Findings and readiness boundaries

**Blocking defect: none found within this review scope.** No arithmetic,
port-order, embedding, native-code, sample-accounting, plan-routing or
overwrite-protection failure was observed.

**Nonblocking interface limitation:** `scripts/lab_records.py:84` checks that
real gate timestamps are present, without parsing their format or ordering.
The explicit fixture `record_status=REAL`, `gate_open_time=not-a-time`,
`gate_close_time=not-a-time` is accepted as `DESCRIPTIVE_ONLY`. The generic
schema intentionally supplies no laboratory clock unit. Thus a successful
descriptive parse must not be treated as timing validation. The eventual lab
adapter must define the clock format, gate ordering, settling and exposure
rules and validate them against acquisition evidence. This does not change
the observed counts or the documented external-calibration boundary.

The following are missing laboratory prerequisites, not newly discovered
software defects and not evidence that the two chips are unavailable:

| Activity | Inputs still required from the laboratory |
|---|---|
| Physical commissioning | Logical/physical connector and detector maps, matrix/compiler convention, control access, compatible wavelength/polarization/illumination, calibrated readout; shared phase reference for complex transfer |
| M1 or genuine hidden-label interrogation | Independently controlled preparation, hidden phase/loss and receiver roles; fresh isolated label controller; source/clock or pre-exposure herald definition; complete output, timing and failed-attempt records |
| P1/P2 certification | P0 incident mean and source/tail bounds; simultaneous phase-referenced P0-to-P1 maps and uncertainty coverage; drift and accessible-mode/leakage treatment; blinded fixed-N held-out plan, frozen settings and confidence allocation |
| P2 implementation | Coherent reference/couplers, stable label-independent displacement matched to the actual common hidden phase, and its configuration/readout calibration |
| Either SU8 scientific route | Complete eight-output recording or separately justified bounded leakage treatment; distinct native-eight records and no transfer of four-mode robustness/source-class certificates |

The exported matrices are logical targets, not voltages. No result verifies
physical calibration coverage, high-number energy tails, hidden-label
isolation, absence of optional stopping, or acquisition readiness. Native-eight
Walsh references supply an ideal photon-theorem specialization and descriptive
records; they supply neither an eight-label classical frontier nor a registered
source-class experiment. No experimental advantage, computing speedup, or new
hardware capability follows from these software passes.
