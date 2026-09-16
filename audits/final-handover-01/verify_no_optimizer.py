"""Audit stored robustness witnesses while trapping numerical optimizers.

Run from any directory with --results FILE --output NEW_DIRECTORY.
This supplements the supplied verifier without changing its implementation.
"""
import argparse
import json
import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "studies" / "robustness-01"))
import study
import verify_certificates
import scipy.optimize


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Use a new output directory")
    calls = []

    def forbidden(*args, **kwargs):
        calls.append(True)
        raise AssertionError("Certificate verification invoked an optimizer")

    with patch.object(study, "linprog", forbidden), patch.object(
        scipy.optimize, "linprog", forbidden
    ), patch.object(scipy.optimize, "minimize", forbidden):
        verify_certificates.verify(args.results, args.output)
    assert not calls
    report = {
        "status": "PASS",
        "optimizer_calls": len(calls),
        "trapped_functions": ["study.linprog", "scipy.optimize.linprog", "scipy.optimize.minimize"],
        "scope": "Stored exact finite-model witnesses; not physical calibration",
    }
    (args.output / "OPTIMIZER_TRAP.json").write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
