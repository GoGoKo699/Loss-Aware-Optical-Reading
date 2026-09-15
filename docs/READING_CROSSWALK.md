# Optional reading crosswalk

Start with the repository's [SU4](../experiment/SU4.md) or
[SU8](../experiment/SU8.md) procedure. The
[local theory route](THEORY_ROUTE.md) explains the experiment without outside
reading. These two complementary anchors offer engineering and discrimination
background when a reader wants it; they are not a two-source prerequisite.

## Engineering: from optical blocks to a working measurement

José Capmany and Daniel Pérez, *Programmable Integrated Photonics*, Oxford
University Press, 2020. [Publisher book page](https://academic.oup.com/book/40570).

**Access checked 2026-09-15:** the publisher's contents and the four chapter
abstracts below were inspected. Full chapters were not accessible. This is a
verified **contents/abstract mapping**, not a claim to have inspected their full
text. No subsection, equation, figure, or pinpoint page reference is inferred.

| External topic and verified chapter | Local explanation | Relevant experiment | Detailed local proof or contract |
|---|---|---|---|
| [Chapter 2: Basic Building Blocks and Techniques](https://academic.oup.com/book/40570/chapter/347979697): component matrices, couplers, phase shifts, composition | [State, phase, and loss](THEORY_ROUTE.md#1-the-question-asked-by-one-photon); [interfaces](../experiment/INTERFACES.md) | [Classical-light commissioning](../experiment/COMMISSIONING.md) on both chips | [Canonical photon model, §1](../proofs/THEORY.md) |
| [Chapter 4: Integrated Multi-port Interferometers](https://academic.oup.com/book/40570/chapter/347980262): multiport unitaries and programmed transforms | [Fixed decoder](THEORY_ROUTE.md#3-what-the-fixed-decoder-does) and chip port maps | [SU4](../experiment/SU4.md); [SU8 routes A/B](../experiment/SU8.md) | [Theorems 1–2](../proofs/THEORY.md) |
| [Chapter 6: Practical Implementation of Programmable Photonic Circuits](https://academic.oup.com/book/40570/chapter/347980684): nonidealities, control, characterization | [Uncertainty worksheet](../experiment/UNCERTAINTY.md) and [physical interfaces](../experiment/INTERFACES.md) | [Commissioning](../experiment/COMMISSIONING.md), then [M1](../experiment/M1.md) | [Map calibration and photon perturbation bounds, §§2/5](../proofs/THEORY.md); [numerical contract](NUMERICAL_CONTRACT.md) |
| [Chapter 7: Programmable Integrated Photonics for Quantum Systems](https://academic.oup.com/book/40570/chapter/347980956): integrated quantum optics, external sources/detectors, Hadamard transforms | [Global path encoding](PHYSICAL_SETTING.md); [Walsh specialization](THEORY_ROUTE.md#7-what-carries-to-the-existing-su8-chip) | [SU8 native eight-mode route](../experiment/SU8.md) | [Flat-code photon theorem, §1](../proofs/THEORY.md) |

The chapter-topic descriptions come from accessible abstracts. Their connection
to our recipes is our pedagogical mapping. The book does not establish which
supporting interfaces this laboratory has, or prove this repository's results.
Optical component matrices lead to exact target matrices, then programming,
calibration, and measurement; each local recipe supplies that route directly.

## Theory: from possible states to a decision

Stephen M. Barnett and Sarah Croke, *Quantum state discrimination*,
*Advances in Optics and Photonics* **1**, 238–278 (2009).
[arXiv entry](https://arxiv.org/abs/0810.1970),
[accessible full text](https://arxiv.org/html/0810.1970v1),
[arXiv PDF](https://arxiv.org/pdf/0810.1970).

**Access checked 2026-09-15:** the relevant full-text passages in arXiv v1 were
inspected. The locators below use that version, dated 10 October 2008, not
unverified journal pagination. No external article is redistributed here.

| Inspected external topic | Local explanation | Relevant experiment | Detailed local proof |
|---|---|---|---|
| §1: possible states and priors; §2: generalized measurements | [Returned ensemble, vacuum, and C/E/F](THEORY_ROUTE.md#2-what-returns-including-the-lost-photon) | [M1](../experiment/M1.md), [P1](../experiment/P1.md), [P2](../experiment/P2.md) | [Scope and notation, §0](../proofs/THEORY.md) |
| §3.1: minimum error; §3.1.a: measurement optimality conditions | [Two optimization questions](THEORY_ROUTE.md#4-two-different-optimization-questions); [achieved/bound/optimum](THEORY_ROUTE.md#5-a-measured-score-a-ceiling-and-an-optimum) | [M1](../experiment/M1.md) | [Theorems 1–2](../proofs/THEORY.md) |
| §3.1.b: square-root measurement | [Fixed decoder and credited ingredient](THEORY_ROUTE.md#4-two-different-optimization-questions) | [SU4 mechanism](../experiment/SU4.md); [SU8 photon specialization](../experiment/SU8.md) | [Fixed-input reductions R1–R3](../audits/novelty-01/REDUCTIONS.md) |
| §3.2 and §3.2.a: unambiguous discrimination and inconclusive outcomes | [Inverse-loss preparation](THEORY_ROUTE.md#3-what-the-fixed-decoder-does) | [M1 zero-error control](../experiment/M1.md) | [Theorem 2, zero-error endpoint](../proofs/THEORY.md) |
| §3.3.a and §3.4: alternative objectives and error/inconclusive tradeoffs | [Score and vacuum decision](THEORY_ROUTE.md#4-two-different-optimization-questions) | [M1](../experiment/M1.md); registered [P1](../experiment/P1.md)/[P2](../experiment/P2.md) scores | [Theorems 1–2 and score witnesses, §§1/4](../proofs/THEORY.md) |
| §4.1–§4.3: optical implementations | [Commissioning](../experiment/COMMISSIONING.md) | Both chip routes, followed by single-photon tests | [Physical scope](PHYSICAL_SETTING.md); [trial contract](../experiment/FIRST_EXPERIMENT.md) |

The review's optical examples illustrate measurement construction. Its §4.1
also distinguishes linear-optical amplitude/intensity checks from use of a
single-photon source. A successful commissioning pattern is not a certified
source-class advantage. Polarization examples are analogies, not permission to
add resources to this project's global-path contract.

## Attribution beyond the two anchors

The [source map](../SOURCE_AUDIT.md),
[claim ledger](../CLAIM_STATUS.md), and
[completed follow-up reductions](../audits/novelty-02/REDUCTIONS.md) retain the
primary research attribution. They are directly reachable reference material,
not another reading curriculum.

The local candidate A concerns complete input-only retuning in the stated joint
optimization problem. Its fixed-input square-root measurement and zero-error
endpoint are credited ingredients. B is the derived optical source-class
benchmark; its completed reductions and resolved source-access qualifications
remain controlling. Neither educational anchor supplies novelty clearance, and
neither numerical verification nor a favorable optical pattern establishes it.
