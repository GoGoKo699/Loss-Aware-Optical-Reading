# SU8: two immediate routes

**Your SU(8) chip is available.** Route A uses four active paths for the existing
four-label experiment. Route B uses all eight paths for a native orthogonal
phase-code teaching and commissioning example. Both use one photon at a time
in global path encoding. Eight modes do not mean eight photons or eight
independently carried qubits.

Start with [classical-light commissioning](COMMISSIONING.md). Both routes have
runnable target matrices and synthetic records. Chip availability is confirmed;
physical port order, compiler phase convention, source/readout compatibility,
and the independent hidden phase/loss interface remain lab inputs in
[INTERFACES.md](INTERFACES.md).

## Route A: four active modes

Use logical input/output ports **0, 1, 2, 3** as the active block, in that order.
Inputs **4, 5, 6, 7 are vacuum**. Record the actual connector and detector map.
Vectors are columns; matrix rows are outputs and columns are inputs.

```math
a^{(8)}=(\sqrt{p_0},\sqrt{p_1},\sqrt{p_2},\sqrt{p_3},0,0,0,0)^T,
```

```math
O_j^{(8)}=(I_4-2|j\rangle\langle j|)\oplus I_4,
\quad j=0,1,2,3,
```

```math
T^{(8)}=\mathrm{diag}(\sqrt{\eta_0},\ldots,\sqrt{\eta_3})\oplus I_4,
\qquad D^{(8)}=(J_4/2-I_4)\oplus I_4.
```

`I4` on the spare block is the ideal reference target, not a measured claim
about spare-path loss. `T` is physical attenuation, not a unitary setting.
Use `Uprep,4 ⊕ I4` with the explicit preparation completion on the
[SU4 page](SU4.md); only input port 0 is populated before preparation.
The four losses and retuning rule are exactly those on that page. This is
**the same four-label task on an eight-mode processor**, not an eight-label result.

The hidden matrix and receiver above each have determinant minus one.
`exp(i*pi/8) O_j^(8)` and `exp(i*pi/8) D^(8)` are consistent SU(8)
representatives. The common hidden multiplier must be the same for all four
labels. Calibrate the actual shared optical phase; do not permit the compiler
to discard different label-dependent phases.

For equal input and uniform active transmission `t`, output `j` has ideal
probability `t` and the other outputs have zero probability. The input on each
spare rail remains vacuum. The theorem's illumination class is restricted to
the four tested input modes; extra occupied bypass inputs are not added to it.

### Spare outputs are recorded

An eight-detector record has a mask from **0 to 255**, with bit `k` for logical
output `k`. A single click on an active port reports that label. A spare-port
click, a mixed active/spare mask, any multiple-click mask, no click, or a
predeclared rejected record is inconclusive. Keep every row and every raw mask.
For example, mask `16` is a spare-port detection and mask `17` contains active
port 0 plus spare port 4; both fail. They must never become a successful active
click by dropping the upper bits.

Monitor all outputs or provide an independently justified treatment of
unmonitored leakage before claiming a complete acquisition. The reference
adapter preserves the 256-mask histogram and marks spare leakage as failure
before any four-label scoring. A different accessible-output geometry also
requires a phase-referenced map and a photon/classical bound appropriate to
that geometry; empty inputs do not prove that the real device has no leakage.

```bash
python scripts/lab_reference.py --recipe commission-su8-embed --output results/runs/su8-four-commission
python scripts/lab_reference.py --recipe m1 --chip su8-embed --output results/runs/su8-four-m1
python scripts/lab_records.py --route su8-embed --trials results/runs/su8-four-m1/synthetic_trials.csv --output results/runs/su8-four-m1-analysis
```

The [M1](M1.md), [P1](P1.md), and [P2](P2.md) pages identify their four-label
claims and extra requirements. Four-path ideal predictions carry over to this
embedding; four-mode robustness certificates do not automatically cover an
imperfect eight-mode channel with extra accessible outputs.

## Route B: native eight-mode Walsh code

Use ports and labels **0–7**, each written as three-bit binary strings
`000, 001, 010, 011, 100, 101, 110, 111`. The parity of the bitwise product
defines the physical phase code:

```math
Z_8[i,j]=(-1)^{\sum_{b=0}^{2}i_bj_b},\qquad
O_j=\mathrm{diag}(Z_8[:,j]),\qquad D_8=Z_8^\dagger/\sqrt{8}.
```

The exponent is evaluated modulo two. Rows below are **input paths**; columns
are **hidden labels**. A minus sign means a pi phase relative to the common
reference, and a plus sign means zero phase.

| Path / label | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| 0: 000 | + | + | + | + | + | + | + | + |
| 1: 001 | + | − | + | − | + | − | + | − |
| 2: 010 | + | + | − | − | + | + | − | − |
| 3: 011 | + | − | − | + | + | − | − | + |
| 4: 100 | + | + | + | + | − | − | − | − |
| 5: 101 | + | − | + | − | − | + | − | + |
| 6: 110 | + | + | − | − | − | − | + | + |
| 7: 111 | + | − | − | + | − | + | + | − |

Every column has norm `sqrt(8)`. For distinct columns `j,k`, the nonzero bit
string `j XOR k` pairs the paths into opposite contributions, giving zero inner
product. Thus `Z8† Z8 = 8 I8`, `D8† D8 = I8`, and

```math
a=(1,1,1,1,1,1,1,1)^T/\sqrt{8},\qquad D_8O_ja=|j\rangle.
```

All `O_j` have determinant one: label 0 has no minus signs; every other column
has four. This ordering also gives `det(D8)=1`, so no extra SU phase is required.
Label 0 is the all-zero Walsh pattern; it is one of eight promised codewords,
not a ninth fault-diagnosis hypothesis. **Eight single-path flips are a different,
nonorthogonal code and are not used.**

For independently characterized label-independent positive diagonal losses,
use `T8 = diag(sqrt(eta_0),...,sqrt(eta_7))` and input `a_i=sqrt(p_i)`.
The same explicit first-column preparation completion on [SU4](SU4.md) works
in eight dimensions. Theorem 1 specializes with `m=8`:

```math
B_\lambda=\frac{1+\lambda}{8}vv^T-\lambda\,\mathrm{diag}(\eta),
\quad v_i=\sqrt{\eta_i},\quad p_i=z_i^2,\quad \lambda\ge1/7,
```

where `z` is the positive normalized top eigenvector. Keep `D8` fixed and no
click inconclusive. With `s=sum_i eta_i p_i`, the unconditional ideal rates are

```math
C=\frac{(\sum_i\sqrt{\eta_ip_i})^2}{8},\qquad E=s-C,\qquad F=1-s.
```

At zero error use `p_i=(1/eta_i)/sum_k(1/eta_k)` and
`C=8/sum_i(1/eta_i)`. For uniform `eta_i=t`, uniform preparation gives
`C=t, E=0, F=1-t`. These are already proved photon-theorem specializations;
the matrix and port checks are independent implementation checks.

```bash
python scripts/lab_reference.py --recipe commission-su8-walsh --output results/runs/su8-walsh-commission
python scripts/lab_records.py --route su8-walsh --trials results/runs/su8-walsh-commission/synthetic_trials.csv --output results/runs/su8-walsh-analysis
```

Run from the repository root after [environment setup](../docs/REPRODUCE.md),
with new output directories. The output files are `target_matrices.json`,
`forecast.json`, `synthetic_trials.csv`, `synthetic_summary.json`, and
`RECORD_SCHEMA.json`. The forecast includes the exact code convention and
photon preparation rule; the generated sample is synthetic, not lab data.

For the nonuniform teaching point `eta=(.7,.7,.7,.7,.7,.7,.7,.14)` and
`lambda=5`, the verified specialization gives
`p=(.1090574612,.1090574612,.1090574612,.1090574612,.1090574612,.1090574612,.1090574612,.2365977716)`.
It predicts `C=.5597246159, E=.0077806321, F=.4324947521` and score
`.5208214556`. These are ideal-model reference numbers, not laboratory values
or an eight-mode source-class certificate. The
[committed native-eight example](../examples/lab/commission-su8-walsh/forecast.json)
contains the full numerical precision.

### What changes in the native eight-mode record

| Record item | Four-label SU8 embedding | Native eight-mode Walsh |
|---|---|---|
| Hidden labels | 0–3 | 0–7 |
| Correct single-click masks | `1 << j` for `j=0..3` | `1 << j` for `j=0..7` |
| Output masks retained | All 256 | All 256 |
| Spare-port outcome | Any click on 4–7 is failure | All eight are answer ports |
| Analysis | Explicit four-label adaptation preserves leakage failures | Separate eight-label descriptive analysis |
| Registered source-class certificate | Only applicable four-label P1/P2 contract after calibration | None supplied by this recipe |

Both formats retain attempted-trial IDs, timing, calibration/preparation/receiver
IDs, energy-bound references, and rejected records. Do not feed the native
eight-detector data into `src/analyze_trials.py`, which implements the existing
four-label certificate. `scripts/lab_records.py` refuses a certification plan
for the native route.

The established comparison here is achieved ideal photon rates versus the
existing photon optimum under the flat-code assumptions, plus optical transfer
verification. No exact eight-mode classical frontier or four-mode robustness
result is imported. The general-map classical theorem remains available in the
[proofs](../proofs/THEORY.md), but a native eight-label calibrated comparison and
statistical acquisition require a separate scoped plan. Orthogonal routing alone
does not establish a source-class advantage.

See [commissioning steps](COMMISSIONING.md), [uncertainty inputs](UNCERTAINTY.md),
[theory route](../docs/THEORY_ROUTE.md), and
[four-mode robustness boundaries](../docs/ROBUSTNESS_GUIDE.md).
