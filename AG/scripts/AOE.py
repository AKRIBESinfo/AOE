import os
import re
import argparse
import shutil
import json
import uuid
from datetime import datetime

ROOT = "/mnt/c/AK/PRJ"
LOG_ROOT = "/mnt/c/AK/LOG"
SESSION_FILE = "/mnt/c/AK/AG/logs/aoe_apply_session.json"

TYPE_FOLDER_MAP = {
    "DRW": "DRW",
    "EST": "EST",
    "NWC": "COORD",
    "NWD": "COORD",
    "NWF": "COORD",
    "RFI": "RFI",
    "SUB": "SUB",
    "IMG": "IMG",
    "MSC": "MISC",
}

FILENAME_RE = re.compile(
    r"^(?P<project>[A-Z]{3}\d{4})_(?P<type>[A-Z]{3})(?P<seq>\d{3})_(?P<date>\d{6})\.(?P<ext>.+)$"
)


def validate_file(project, folder, filename):
    issues = []

    match = FILENAME_RE.match(filename)
    if not match:
        issues.append("INVALID NAME FORMAT")
        return issues

    file_project = match.group("project")
    file_type = match.group("type")

    if file_project != project:
        issues.append(f"PROJECT MISMATCH ({file_project})")

    if file_type not in TYPE_FOLDER_MAP:
        issues.append(f"INVALID TYPE ({file_type})")
    else:
        expected_folder = TYPE_FOLDER_MAP[file_type]
        if folder != expected_folder:
            issues.append(f"WRONG FOLDER (should be {expected_folder})")

    return issues


def run_summary(project_filter=None, show_files=False):
    print("\nAOE v0.2 — SUMMARY\n" + "-" * 40)

    total_projects = 0
    total_files = 0

    for project in sorted(os.listdir(ROOT)):
        if project_filter and project != project_filter:
            continue

        project_path = os.path.join(ROOT, project)
        exp_path = os.path.join(project_path, "EXP")

        if not os.path.isdir(exp_path):
            continue

        total_projects += 1
        print(f"\nPROJECT: {project}")

        project_total = 0
        empty_folders = []

        for folder in sorted(os.listdir(exp_path)):
            folder_path = os.path.join(exp_path, folder)

            if not os.path.isdir(folder_path):
                continue

            files = [
                f for f in sorted(os.listdir(folder_path))
                if os.path.isfile(os.path.join(folder_path, f))
            ]

            if not files:
                empty_folders.append(folder)
                continue

            print(f"  {folder}: {len(files)}")

            if show_files:
                for f in files:
                    print(f"    - {f}")

            project_total += len(files)

        if empty_folders:
            print(f"  (empty: {', '.join(empty_folders)})")

        print(f"  TOTAL: {project_total}")
        total_files += project_total

    print("\n" + "-" * 40)
    print(f"Projects: {total_projects}")
    print(f"Total Files: {total_files}\n")


def run_check(project_filter=None):
    print("\nAOE v0.2 — CHECK\n" + "-" * 40)

    total_issues = 0

    for project in sorted(os.listdir(ROOT)):
        if project_filter and project != project_filter:
            continue

        project_path = os.path.join(ROOT, project)
        exp_path = os.path.join(project_path, "EXP")

        if not os.path.isdir(exp_path):
            continue

        print(f"\nPROJECT: {project}")

        issues_found = False

        for folder in sorted(os.listdir(exp_path)):
            folder_path = os.path.join(exp_path, folder)

            if not os.path.isdir(folder_path):
                continue

            for filename in sorted(os.listdir(folder_path)):
                file_path = os.path.join(folder_path, filename)

                if not os.path.isfile(file_path):
                    continue

                issues = validate_file(project, folder, filename)

                if issues:
                    issues_found = True
                    total_issues += 1
                    print(f"\n  ISSUE: {folder}/{filename}")
                    for i in issues:
                        print(f"    - {i}")

        if not issues_found:
            print("  ✔ No issues found")

    print("\n" + "-" * 40)
    print(f"Total Issues: {total_issues}\n")


def collect_realignments(project_filter=None):
    actions = []

    for project in sorted(os.listdir(ROOT)):
        if project_filter and project != project_filter:
            continue

        project_path = os.path.join(ROOT, project)
        exp_path = os.path.join(project_path, "EXP")

        if not os.path.isdir(exp_path):
            continue

        for folder in sorted(os.listdir(exp_path)):
            folder_path = os.path.join(exp_path, folder)

            if not os.path.isdir(folder_path):
                continue

            for filename in sorted(os.listdir(folder_path)):
                source_path = os.path.join(folder_path, filename)

                if not os.path.isfile(source_path):
                    continue

                match = FILENAME_RE.match(filename)
                if not match:
                    continue

                file_project = match.group("project")
                file_type = match.group("type")

                if file_project != project:
                    continue

                if file_type not in TYPE_FOLDER_MAP:
                    continue

                expected_folder = TYPE_FOLDER_MAP[file_type]
                if folder == expected_folder:
                    continue

                dest_folder = os.path.join(exp_path, expected_folder)
                dest_path = os.path.join(dest_folder, filename)

                actions.append({
                    "project": project,
                    "filename": filename,
                    "current_folder": folder,
                    "expected_folder": expected_folder,
                    "source_path": source_path,
                    "dest_path": dest_path,
                })

    return actions


def ensure_session_dir():
    os.makedirs(os.path.dirname(SESSION_FILE), exist_ok=True)


def write_session(actions, project_filter):
    ensure_session_dir()
    token = str(uuid.uuid4())[:8]

    payload = {
        "token": token,
        "created": datetime.now().isoformat(),
        "project_filter": project_filter,
        "actions": actions,
    }

    with open(SESSION_FILE, "w") as f:
        json.dump(payload, f, indent=2)

    return token


def read_session():
    if not os.path.exists(SESSION_FILE):
        return None

    with open(SESSION_FILE, "r") as f:
        return json.load(f)


def run_apply(project_filter=None, dry_run=False, session_token=None):
    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"\nAOE v0.2 — {mode}\n" + "-" * 40)

    actions = collect_realignments(project_filter)

    if dry_run:
        if not actions:
            print("\n✔ No safe realignment actions found\n")
            return

        for action in actions:
            print(f"\nPROJECT: {action['project']}")
            print(f"  MOVE: {action['current_folder']}/{action['filename']}")
            print(f"    -> {action['expected_folder']}/{action['filename']}")

            if os.path.exists(action["dest_path"]):
                print("    SKIP: destination already exists")

        token = write_session(actions, project_filter)

        print("\n" + "-" * 40)
        print(f"Planned Moves: {len(actions)}")
        print(f"Session Token: {token}")
        print("\nTo apply these exact changes, run:")
        if project_filter:
            print(f"  AOE --project {project_filter} --apply --session {token}")
        else:
            print(f"  AOE --apply --session {token}")
        print()
        return

    # Apply mode
    session = read_session()
    if not session:
        print("\nERROR: No dry-run session found. Run --apply --dry-run first.\n")
        return

    if not session_token:
        print("\nERROR: --session token required. Run --apply --dry-run first.\n")
        return

    if session_token != session.get("token"):
        print("\nERROR: Invalid session token.\n")
        return

    if project_filter != session.get("project_filter"):
        print("\nERROR: Project scope does not match dry-run session.\n")
        return

    actions = session.get("actions", [])
    if not actions:
        print("\n✔ No actions to apply.\n")
        return

    moved = 0
    skipped = 0

    for action in actions:
        print(f"\nPROJECT: {action['project']}")
        print(f"  MOVE: {action['current_folder']}/{action['filename']}")
        print(f"    -> {action['expected_folder']}/{action['filename']}")

        if not os.path.exists(action["source_path"]):
            print("    SKIP: source no longer exists")
            skipped += 1
            continue

        if os.path.exists(action["dest_path"]):
            print("    SKIP: destination already exists")
            skipped += 1
            continue

        os.makedirs(os.path.dirname(action["dest_path"]), exist_ok=True)
        shutil.move(action["source_path"], action["dest_path"])
        moved += 1

    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

    print("\n" + "-" * 40)
    print(f"Moved: {moved}")
    print(f"Skipped: {skipped}\n")


def main():
    parser = argparse.ArgumentParser(description="AOE CLI")

    parser.add_argument("--check", action="store_true", help="Run validation checks")
    parser.add_argument("--project", type=str, help="Filter by project code")
    parser.add_argument("--log", action="store_true", help="Save output to LOG")
    parser.add_argument("--files", action="store_true", help="Show file list")
    parser.add_argument("--apply", action="store_true", help="Apply safe folder realignment")
    parser.add_argument("--dry-run", action="store_true", help="Preview actions without making changes")
    parser.add_argument("--session", type=str, help="Session token from prior dry-run")

    args = parser.parse_args()

    output = []

    def capture(text=""):
        output.append(text)

    global print
    original_print = print
    print = capture

    if args.apply:
        run_apply(
            project_filter=args.project,
            dry_run=args.dry_run,
            session_token=args.session
        )
    elif args.check:
        run_check(args.project)
    else:
        run_summary(args.project, show_files=args.files)

    print = original_print

    for line in output:
        print(line)

    if args.log:
        os.makedirs(LOG_ROOT, exist_ok=True)
        filename = f"AOE_LOG_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        full_path = os.path.join(LOG_ROOT, filename)

        with open(full_path, "w") as f:
            f.write("\n".join(output))

        print(f"\nSaved to: {full_path}")


if __name__ == "__main__":
    main()
