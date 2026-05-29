---
name: scientific-data-report
description: Use when processing scientific data or reporting scientific data-processing work, especially when the user needs an auditable report package with provenance, commands, parameters, input fingerprints, output lineage, QC checks, scientific assumptions, risks, reproducibility status, and claims boundaries.
---

# Scientific Data Report

Use this skill for any scientific data processing task where results may support figures, tables, reports, manuscripts, decisions, or later review. The output is a data-processing report package, not just prose.

## Core Rule

Deliver an auditable package that lets the user check what was done, why it was scientifically defensible, what evidence proves it was executed, and what remains uncertain.

Never blur missing provenance. If key information is unavailable, stop, ask, or downgrade the report status.

## Required Package

Package placement:

1. If the project follows the `research-folder-organizer` task-package layout and this work belongs to one concrete task, place the report package under that task:

   ```text
   <project_root>/10_tasks/T###_short_slug/runs/YYYYMMDD_HHMMSS_<task_slug>/
   ```

2. If the output is a cross-task stage summary, reviewer-facing report, or project-level audit, place it under:

   ```text
   <project_root>/50_reports/YYYYMMDD_HHMMSS_<task_slug>/
   ```

3. If no project structure is known, use:

```text
<project_root>/data_processing_reports/YYYYMMDD_HHMMSS_<task_slug>/
```

If a project has any other established reports/runs structure, follow it. Always record the chosen path in `AUDIT_MANIFEST.json`.

Required files:

```text
PROCESSING_PLAN.md
REPORT.md
AUDIT_MANIFEST.json
COMMAND_LOG.md
QC_CHECKLIST.md
FIGURE_INDEX.md
outputs/
figures/
tables/
logs/
```

`AUDIT_MANIFEST.json` is the machine-readable source of truth. YAML is optional.

## Helper Scripts

Create a package with:

```bash
python <skill_dir>/scripts/init_report_package.py --root . --task "short task title" --mode exploratory
```

For a known task package:

```bash
python <skill_dir>/scripts/init_report_package.py --root . --task "short task title" --task-package 10_tasks/T012_some_task --mode formal
```

For a cross-task report:

```bash
python <skill_dir>/scripts/init_report_package.py --root . --task "short task title" --cross-task-report --mode formal
```

Use `--mode formal` for manuscript, final figure, final table, or conclusion-supporting work.

Validate before final delivery with:

```bash
python <skill_dir>/scripts/validate_report_package.py <package_dir>
```

For a freshly initialized empty template only:

```bash
python <skill_dir>/scripts/validate_report_package.py <package_dir> --allow-draft
```

If a script cannot run, create the same structure manually and record the failure in `COMMAND_LOG.md`.

## Processing Modes

- `formal`: final/report/manuscript/conclusion-supporting processing. Write `PROCESSING_PLAN.md` first and wait for user confirmation before executing, unless the user explicitly preapproved execution.
- `exploratory`: exploratory analysis may proceed without waiting, but `audit_status` must be `exploratory` and conclusions must stay provisional.
- `repair`: fix or patch an existing data-processing workflow. Record the defect, changed code, and verification.
- `reproduce`: rerun or verify an existing workflow. Record exact reproduction scope and deviations.

If the user says to directly process and report, still write `PROCESSING_PLAN.md` and set `plan.user_preapproved = true`.

## Hard Constraints

- Treat raw data as read-only. Do not modify, move, rename, delete, or overwrite original data unless the user explicitly authorizes it.
- Never silently overwrite outputs. Use a new timestamped run directory if output paths already exist.
- Separate executed evidence from inferred descriptions.
- Existing output files are `existing_file`, not `executed_this_session`.
- If a step is inferred from code or filenames, label it `inferred_from_code`.
- If provenance, metadata, units, scale, sampling, code version, parameters, or execution evidence are missing, block or downgrade.
- For non-scripted work such as GUI, Excel, Origin, MATLAB interactive work, COMSOL GUI, or notebooks, capture configuration, screenshots/exports when relevant, file fingerprints, and exact manual steps. Reproducibility is at most `partially_reproducible` unless the workflow can be rerun deterministically.

## Required Status Fields

Set these near the top of `REPORT.md` and in `AUDIT_MANIFEST.json`:

```text
Audit status: complete | partial | blocked | exploratory
Reproducibility: reproducible | partially_reproducible | not_reproducible | not_assessed
Scientific confidence: high | medium | low | not_assessed
```

`complete` requires reproducible outputs, complete provenance, complete input fingerprints or documented fallback fingerprints, no unresolved blockers, and no unknown critical fields.

## Plan Before Processing

`PROCESSING_PLAN.md` must state:

- Objective and whether the work is `formal`, `exploratory`, `repair`, or `reproduce`.
- Raw inputs to be used and expected metadata.
- Planned steps, algorithms, thresholds, filters, fitting/statistics, unit conversions, and visualization choices.
- Method basis for each key choice: user instruction, paper, instrument metadata, code default, domain convention, or exploratory judgment.
- Expected outputs and review checkpoints.
- What would block or downgrade the result.

For `formal` work, stop after writing the plan until the user confirms.

## What Counts As A Key Step

Any operation that can affect data values, sample membership, coordinates, units, time interpretation, statistics, visual interpretation, or claims is a key step.

Key steps include:

- Reading, conversion, channel/variable selection.
- Sample filtering, region/time cropping, bad-point or outlier removal.
- Unit conversion, coordinate transformation, calibration, normalization, nondimensionalization.
- Filtering, smoothing, interpolation, resampling, registration, denoising.
- Fitting, statistical testing, error estimation, uncertainty propagation.
- Parameter or threshold choice, including defaults.
- Aggregation or post-processing that affects figures, tables, or core values.
- Visualization choices that affect interpretation: color limits, axis truncation, log scales, normalized display.

Every key step must appear in `AUDIT_MANIFEST.json` with:

```text
method_basis
assumptions
risks
verification
```

Non-key operational steps may be summarized in `COMMAND_LOG.md`.

## Provenance Requirements

Each important input must record:

- Path and role.
- Whether it existed at runtime.
- Size and modified time when available.
- Full SHA256 for small/medium files.
- Fallback fingerprint for very large files or directory datasets: file count, total size, modified-time summary, key metadata hash, or sampled-block hash.
- Format, dimensions/shape, dtype, units, coordinates, sampling rate, or other scientific metadata where relevant.

For Zarr, HDF5, MAT, NetCDF, TIFF stacks, and similar structured data, record dataset/group names, shapes, dtypes, attrs, and units where available.

If even fallback fingerprinting is absent, the report cannot be `complete`.

## Output Lineage

Every figure, table, processed dataset, model, or statistic used in conclusions must trace back to:

- Input IDs.
- Step IDs.
- Script/function/command or evidence source.
- Parameters and method basis.

The report cannot just say "generated figure X." It must state how X was derived.

## Figures And Captions

Reports that produce, audit, or rely on figures must include figures and figure captions.

Required behavior:

- Put generated or copied review figures under `figures/`, or reference existing figure paths if copying would duplicate large files.
- Add every review-relevant figure to `FIGURE_INDEX.md`.
- In `REPORT.md`, embed or link the key figures near the discussion that uses them.
- Every figure must have a caption that states what is shown, data source, processing step IDs, key parameters, units/scale/colorbar meaning, and any caveat needed for interpretation.
- Every figure output in `AUDIT_MANIFEST.json` must include `caption`, `derived_from_steps`, and `derived_from_inputs`.
- If a figure is pre-existing, label it `existing_file` and record its source path/fingerprint when possible.
- If a figure is only illustrative or exploratory, label it as such; do not let it support a formal claim.

Minimal caption pattern:

```text
Figure N. What is shown. Input IDs and step IDs. Key parameters and units. Interpretation boundary or caveat.
```

## Execution Evidence

`COMMAND_LOG.md` records actual operations only:

- Commands run, working directories, timestamps, exit status, important output.
- Script paths, function entry points, notebook paths/cells, software versions.
- Failures and corrections.

Use these evidence labels in `AUDIT_MANIFEST.json`:

```text
executed_this_session | existing_file | inferred_from_code | user_provided | gui_manual | unknown
```

`unknown` requires downgrade or blockage.

## Environment And Code Version

Record:

- Working directory and OS.
- Python/MATLAB/R/COMSOL/Origin/Excel or other relevant runtime versions.
- Important package versions.
- Git repo, commit, and dirty status when applicable.
- Script/notebook/model file paths, Git status, and SHA256 when not fully tracked.
- Random seeds and nondeterministic settings.

If environment or code version cannot be confirmed, reproducibility is at most `partially_reproducible`.

## Scientific Review

`REPORT.md` and `QC_CHECKLIST.md` must include:

- Unit and coordinate checks.
- Sampling rate, time step, spatial scale, and calibration checks.
- Filtering, smoothing, interpolation, fitting, statistics, and threshold justification.
- Outlier/missing-data policy.
- Sensitivity checks for important thresholds, or explicit `not_assessed`.
- Physical/statistical plausibility checks.
- What would invalidate the result.
- The 3-5 highest-priority manual review targets for formal outputs.
- Figure-level checks: axes, units, colorbars, legends, annotations, cropping, normalization, and caption accuracy.

Do not write "no issue found" unless the attack surfaces checked are listed.

## Claims Boundary

Separate data-processing conclusions from scientific interpretation:

- `Claims allowed by this processing`
- `Claims not supported by this processing`
- `Claims requiring external evidence`

Do not turn processed trends into final scientific mechanism claims unless the evidence chain actually supports that.

## Final Response

When finished, tell the user:

- Package path.
- Audit status, reproducibility, and scientific confidence.
- Whether validation passed.
- The most important blockers or manual review targets.

If validation was not run, state why.
