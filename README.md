# Scientific Data Report

Codex skill for auditable scientific data-processing report packages.

Use this skill when scientific data processing needs reproducible provenance, input fingerprints, command logs, output lineage, QC checks, figure captions, scientific assumptions, risks, and claims boundaries.

## Contents

- `SKILL.md`: skill instructions.
- `scripts/init_report_package.py`: creates the standard report package.
- `scripts/validate_report_package.py`: validates required structure and manifest fields using Python standard library only.
- `agents/openai.yaml`: Codex UI metadata.

## Basic Use

```powershell
python scripts/init_report_package.py --root . --task "short task title" --mode exploratory
python scripts/validate_report_package.py <package_dir> --allow-draft
```

For projects organized with task packages:

```powershell
python scripts/init_report_package.py --root . --task "short task title" --task-package 10_tasks/T012_some_task --mode formal
```

Formal data processing should start with `PROCESSING_PLAN.md` and wait for user confirmation unless execution was explicitly preapproved.
