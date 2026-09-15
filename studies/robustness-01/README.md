# Robustness of input-only retuning: four-mode pre-experiment check

**Completed local study; pending repository commit.** Start with [REPORT.md](REPORT.md),
then [PROOFS.md](PROOFS.md) and [CALIBRATION_WORKSHEET.md](CALIBRATION_WORKSHEET.md).
The target is the existing `research/robustness-01` branch at work-order commit
`ddb17c5040e17cb0078121081afe15de70158fe8`, based on main
`de73c9b094036b756d1ff008eaccbc52cec46207`. No main files or old evidence are changed.

## The result

A common calibratable basis change does not invalidate A. Symmetric dephasing
has an exact fixed-decoder optimum with a modified input rule. A systematic
marked-phase error can instead give a positive, tightly certified benefit from
changing the receiver. More general map errors and rotated loss admit conservative
bounds. Calibration must distinguish these structures before final tolerances
are chosen. All example parameters are hypothetical.

## Reproduce

From the repository root after applying the additions:

```bash
python -m pip install -r studies/robustness-01/requirements.txt
python studies/robustness-01/test_local.py
python studies/robustness-01/study.py --output results/runs/robustness-01-new
python studies/robustness-01/verify_certificates.py --results results/runs/robustness-01-new/RESULTS.json --output results/runs/robustness-01-verified
```

Each output directory must be new. The scripts use no canonical module and write
no frozen result. Regenerating proposals uses SciPy linprog, not an SDP solver.
Stored witness verification invokes no optimizer. Exact rational checks apply
to the explicitly defined finite models, not automatically to physical hardware.

`EVIDENCE.tar.xz` holds the final result, second-run environment, verifier ledger,
execution logs and result-hash comparison. Extract it to a new temporary directory
to check the recorded witnesses without rerunning the numerical search. Archive
member hashes are in SUMMARY.json. No third-party articles are included.

[SOURCES.md](SOURCES.md) credits the baseline, known detector-SDP methods and
calibration literature. [DEVELOPMENT_NOTES.md](DEVELOPMENT_NOTES.md) records the
read-only GitHub access, local execution distinction and numerical retry. No
priority, experiment, pipeline-wide interval guarantee, or new remote CI result
is claimed. The existing operational protocol and laboratory questions remain
unchanged. The next external input is laboratory feedback, not another broad
noise survey.
