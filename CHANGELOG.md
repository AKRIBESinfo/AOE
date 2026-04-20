# AOE Changelog

---

## v0.2 — Operational CLI Foundation

AOE v0.2 marks the transition from a defined filesystem standard
to an operational command-driven environment.

### Added
- AOE CLI (`AOE.py`) with core commands:
  - `AOE`
  - `AOE --check`
  - `AOE --apply`
  - `AOE --project <code>`
- System-wide project scanning and summarization
- Structured reporting output with file visibility
- Validation of folder structure and file placement
- Controlled correction workflow (`--apply` with optional `--dry-run`)
- Git integration with `.gitignore` for system-only tracking
- GitHub remote repository (AKRIBESinfo/AOE)
- README.md for system overview and usage
- CHANGELOG.md for version tracking

### Established
- Clear separation of:
  - system logic (tracked in Git)
  - project data (excluded from Git)
- WSL2 + Python as execution layer
- PowerShell tools (`BIN/`) for Windows-side operations
- VS Code as unified development environment

### Principles Reinforced
- AOE remains:
  - lightweight
  - deterministic
  - predictable
  - agent-compatible

AOE does not replace judgment.
It enforces structure, observability, and safe system behavior.

---

## v0.1 — Structural Foundation

### Established
- Root directory: `C:\AK`
- Core system folders:
  - `AG/` → automation / agent layer
  - `BIN/` → command tools
  - `PRJ/` → project data
  - `LOG/` → logs and generated outputs

### Defined
- Project structure:
  - `EXP/` → deliverables
  - `IMP/` → incoming data
- Naming standards:
  - Project codes
  - File naming conventions

### Purpose
To create a consistent, scalable foundation for managing BIM data
across projects with clarity and structure.
