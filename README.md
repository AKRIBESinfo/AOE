# AOE - Akribes Operating Environment

AOE is a structured filesystem and CLI framework for managing BIM project data, automation, and coordination workflows.

## Structure

- AG/     → Automation & scripts
- BIN/    → Command tools (PowerShell)
- PRJ/    → Project data (not tracked in Git)
- LOG/    → Generated outputs (not tracked in Git)

## Core Commands

  AOE
  AOE --check
  AOE --apply

## Philosophy

AOE separates:
- system logic (tracked in Git)
- project data (managed in filesystem)

Designed for:
- clarity
- predictability
- agent-ready workflows
