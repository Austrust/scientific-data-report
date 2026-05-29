#!/usr/bin/env python3
"""Initialize an auditable scientific data-processing report package."""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
from datetime import datetime
from pathlib import Path


MODES = {"formal", "exploratory", "repair", "reproduce"}


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text[:60] or "task"


def initial_status(mode: str) -> str:
    if mode == "formal":
        return "blocked"
    if mode == "exploratory":
        return "exploratory"
    return "partial"


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8", newline="\n")


def manifest_template(package_dir: Path, task: str, slug: str, mode: str, language: str, user_preapproved: bool) -> dict:
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    return {
        "schema_version": "1.0",
        "generated_at": now,
        "task": {
            "title": task,
            "slug": slug,
            "mode": mode,
        },
        "language": language,
        "audit_status": initial_status(mode),
        "reproducibility": "not_assessed",
        "scientific_confidence": "not_assessed",
        "report_package_root": str(package_dir.resolve()),
        "placement": {
            "policy": "task_package_runs | cross_task_50_reports | data_processing_reports | custom",
            "reason": "",
        },
        "plan": {
            "required": True,
            "approved_by_user": False,
            "user_preapproved": user_preapproved,
            "approval_evidence": "",
        },
        "blockers": [
            "Draft package initialized; fill provenance, steps, outputs, QC, and execution evidence before final delivery."
        ],
        "inputs": [],
        "steps": [],
        "outputs": [],
        "figures": [],
        "environment": {
            "working_directory": str(Path.cwd().resolve()),
            "os": platform.platform(),
            "python": platform.python_version(),
            "packages": {},
            "git_repo": None,
            "git_commit": "",
            "git_dirty": None,
            "execution_time": "",
            "random_seed": "",
        },
        "code_artifacts": [],
        "review_targets": [],
        "claims": {
            "allowed": [],
            "not_supported": [],
            "requiring_external_evidence": [],
        },
    }


def plan_template(task: str, mode: str, user_preapproved: bool) -> str:
    approval = "yes" if user_preapproved else "no"
    return f"""# Processing Plan

Task: {task}
Mode: {mode}
User preapproved execution: {approval}

## Objective

TODO: State the scientific/data-processing objective and intended use of the outputs.

## Planned Inputs

| ID | Path | Role | Expected format | Required metadata | Fingerprint plan |
| --- | --- | --- | --- | --- | --- |
| TODO | TODO | raw_data | TODO | units, shape, sampling/scale | sha256 or fallback |

## Planned Key Steps

| Step ID | Purpose | Method/algorithm | Parameters | Method basis | Assumptions | Risks | Verification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| step_01 | TODO | TODO | TODO | TODO | TODO | TODO | TODO |

## Planned Outputs

| Output ID | Path | Role | Derived from | Review need |
| --- | --- | --- | --- | --- |
| TODO | TODO | figure/table/data/statistic | TODO | TODO |

## Blocking Or Downgrade Conditions

- TODO: Missing raw data provenance, units, scale, code version, parameters, execution evidence, or other critical metadata.

## Approval

- Formal work must wait for user confirmation unless `user_preapproved` is true.
- Approval evidence: TODO
"""


def report_template(task: str) -> str:
    return f"""# Scientific Data Processing Report

Task: {task}

Audit status: TODO
Reproducibility: TODO
Scientific confidence: TODO

## Executive Summary

TODO: Summarize what was processed, what was produced, and whether the result is final, partial, exploratory, or blocked.

## Inputs And Provenance

TODO: List raw data, metadata, calibration/config inputs, fingerprints, units, dimensions, sampling, and coordinate definitions.

## Actual Processing Steps

TODO: For each key step, cite execution evidence, method basis, assumptions, risks, parameters, and verification.

## Output Lineage

TODO: Trace every important figure/table/statistic/processed dataset to input IDs and step IDs.

## Figures And Captions

TODO: Embed or link review-relevant figures here. Every figure needs a caption with data source, step IDs, parameters, units/scale, and caveats.

```text
Figure 1. TODO: What is shown. Input IDs and step IDs. Key parameters and units. Interpretation boundary or caveat.
```

## Scientific Review

### Unit, Coordinate, Scale, And Calibration Checks

TODO

### Filtering, Interpolation, Fitting, Statistics, And Threshold Justification

TODO

### Outlier, Missing Data, And Exclusion Policy

TODO

### Sensitivity And Robustness Checks

TODO or `not_assessed` with reason.

### Physical Or Statistical Plausibility

TODO

## Review Targets / Attack Points

TODO: List the 3-5 highest-priority manual checks or explain why the work is blocked.

## Claims Boundary

### Claims Allowed By This Processing

TODO

### Claims Not Supported By This Processing

TODO

### Claims Requiring External Evidence

TODO

## Blockers And Downgrades

TODO: Explicitly list unresolved provenance, reproducibility, or scientific concerns.

## Reproduction Entry

TODO: Exact command/script/notebook/software path, working directory, environment, and expected outputs. If not reproducible, explain why.
"""


def command_log_template() -> str:
    return """# Command Log

Record actual executed evidence only. Do not place inferred workflow descriptions here.

| Time | Working directory | Command/action | Evidence type | Exit/status | Key output |
| --- | --- | --- | --- | --- | --- |
| TODO | TODO | TODO | executed_this_session / existing_file / inferred_from_code / gui_manual / user_provided | TODO | TODO |

## Failures And Corrections

TODO
"""


def qc_template() -> str:
    return """# QC Checklist

## Provenance And Reproducibility

- [ ] Raw inputs have paths and fingerprints or documented fallback fingerprints.
- [ ] Code artifacts and environment are recorded.
- [ ] Commands/manual actions are recorded with evidence type.
- [ ] Outputs trace to input IDs and step IDs.
- [ ] Review-relevant figures are listed in FIGURE_INDEX.md and embedded or linked in REPORT.md.
- [ ] Every figure has a caption with data source, step IDs, parameters, units/scale, and caveats.
- [ ] A reproduction entry or explicit downgrade is provided.

## Scientific Checks

- [ ] Units, coordinates, scale, calibration, and sampling are checked.
- [ ] Filtering/smoothing/interpolation/resampling choices have method basis.
- [ ] Thresholds/default parameters are justified.
- [ ] Outlier and missing-data policies are documented.
- [ ] Fitting/statistics assumptions are stated.
- [ ] Sensitivity checks are performed or marked `not_assessed` with reason.
- [ ] Physical/statistical plausibility is assessed.
- [ ] Figure axes, units, colorbars, legends, annotations, cropping, normalization, and captions are checked.
- [ ] What would invalidate the result is stated.

## Claims Boundary

- [ ] Allowed claims are separated from unsupported claims.
- [ ] Claims requiring external evidence are listed.
- [ ] Formal outputs have 3-5 manual review targets.

## Blockers

TODO: List blockers, or state that no blockers remain and identify checked attack surfaces.
"""


def figure_index_template() -> str:
    return """# Figure Index

| Figure ID | Path | Caption | Derived from inputs | Derived from steps | Evidence type | Status | Review notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TODO | figures/TODO.png | TODO: what is shown, source data, step IDs, parameters, units/scale, caveat | TODO | TODO | executed_this_session / existing_file / inferred_from_code | exploratory/final | TODO |
"""


def looks_like_task_package(path: Path) -> bool:
    return (path / "README.md").exists() and ((path / "inputs").exists() or (path / "runs").exists())


def choose_output_root(args: argparse.Namespace, root: Path) -> tuple[Path, str, str]:
    if args.output_root:
        return Path(args.output_root).resolve(), "custom", "--output-root was provided"
    if args.task_package:
        task_package = Path(args.task_package)
        if not task_package.is_absolute():
            task_package = root / task_package
        return task_package.resolve() / "runs", "task_package_runs", "--task-package was provided"
    if args.cross_task_report:
        return root / "50_reports", "cross_task_50_reports", "--cross-task-report was provided"
    if looks_like_task_package(root):
        return root / "runs", "task_package_runs", "root looks like a task package"
    return root / "data_processing_reports", "data_processing_reports", "no task package or cross-task placement was specified"


def create_package(args: argparse.Namespace) -> Path:
    root = Path(args.root).resolve()
    slug = slugify(args.slug or args.task)
    timestamp = args.timestamp or datetime.now().strftime("%Y%m%d_%H%M%S")
    output_root, placement_policy, placement_reason = choose_output_root(args, root)
    package_dir = output_root / f"{timestamp}_{slug}"

    counter = 1
    original = package_dir
    while package_dir.exists():
        package_dir = original.with_name(f"{original.name}_{counter:02d}")
        counter += 1

    package_dir.mkdir(parents=True)
    for name in ["outputs", "figures", "tables", "logs"]:
        (package_dir / name).mkdir()

    manifest = manifest_template(package_dir, args.task, slug, args.mode, args.language, args.user_preapproved)
    manifest["placement"]["policy"] = placement_policy
    manifest["placement"]["reason"] = placement_reason
    write_text(package_dir / "PROCESSING_PLAN.md", plan_template(args.task, args.mode, args.user_preapproved))
    write_text(package_dir / "REPORT.md", report_template(args.task))
    write_text(package_dir / "AUDIT_MANIFEST.json", json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    write_text(package_dir / "COMMAND_LOG.md", command_log_template())
    write_text(package_dir / "QC_CHECKLIST.md", qc_template())
    write_text(package_dir / "FIGURE_INDEX.md", figure_index_template())
    return package_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Project root. Default: current directory.")
    parser.add_argument("--task", required=True, help="Short task title.")
    parser.add_argument("--slug", default="", help="Optional ASCII slug for the run directory.")
    parser.add_argument("--mode", choices=sorted(MODES), default="exploratory")
    parser.add_argument("--language", default="auto", help="Report language policy, such as auto, zh, en.")
    parser.add_argument("--output-root", default="", help="Optional report root directory.")
    parser.add_argument("--task-package", default="", help="Task package path. Writes the report under <task-package>/runs.")
    parser.add_argument("--cross-task-report", action="store_true", help="Write under <root>/50_reports.")
    parser.add_argument("--timestamp", default="", help="Optional timestamp for deterministic tests.")
    parser.add_argument("--user-preapproved", action="store_true", help="Mark that the user explicitly approved execution.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    package_dir = create_package(args)
    print(package_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
