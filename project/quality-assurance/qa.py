"""Report, claim and update QA bugs safely while many sessions work at once.

Every command holds one lock (``.qa.lock`` beside this file) while it reads and writes, and
commits and pushes the change before it lets go, so no two sessions get the same id and no bug
is claimed twice. Use it instead of editing ``BUGS.md`` by hand.

    python3 qa.py new "Title" --severity major --area frontend --reporter qa-3
    python3 qa.py next --area frontend,backend --fixer hotfix-front
    python3 qa.py claim QA-012 --fixer hotfix-back
    python3 qa.py set QA-012 --status fixed --note "backend 1.1.16, commit abc1234"
    python3 qa.py list --status open

``new`` prints the new bug file and evidence folder; fill in the file, then commit and push it
(``python3 qa.py save QA-012``). ``next`` claims the open bug of the highest severity in the
given areas and prints it, or prints nothing when none is left.
"""

import argparse
import fcntl
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
INDEX = HERE / "BUGS.md"
BUGS = HERE / "bugs"
EVIDENCE = HERE / "evidence"
TEMPLATE = HERE / "TEMPLATE.md"
LOCK = HERE / ".qa.lock"
STATUSES = ("open", "fixing", "fixed", "verified", "blocked", "wont-fix", "duplicate")
SEVERITIES = ("blocker", "major", "minor", "cosmetic")
LINK = re.compile(r"^\[(QA-\d{3})\]\(([^)]+)\)$")


def git(*args, check=True):
    """Run git in the documents repo and return its output."""
    done = subprocess.run(["git", "-C", str(HERE), *args], capture_output=True, text=True)
    if check and done.returncode != 0:
        sys.exit(f"git {' '.join(args)} failed: {done.stderr.strip()}")
    return done.stdout


def sync():
    """Bring the clone up to date before reading, so ids and claims see every other machine.

    Another session's commit may be landing at the same moment: try a few times before giving up.
    """
    import time

    for _ in range(5):
        done = subprocess.run(
            ["git", "-C", str(HERE), "pull", "-q", "--rebase", "--autostash"], capture_output=True, text=True
        )
        if done.returncode == 0:
            return
        time.sleep(3)
    sys.exit(f"git pull failed five times: {done.stderr.strip()}")


def publish(message, paths):
    """Commit the given paths and push; on a race with another machine, rebase and push again."""
    git("add", "--", *[str(path) for path in paths])
    if not git("diff", "--cached", "--name-only").strip():
        return
    git("commit", "-q", "-m", message)
    for _ in range(3):
        if subprocess.run(["git", "-C", str(HERE), "push", "-q"], capture_output=True).returncode == 0:
            return
        git("pull", "-q", "--rebase")
    sys.exit("push failed three times: run `git -C documents push` by hand")


def rows():
    """Return the index rows as dicts, in file order."""
    found = []
    for line in INDEX.read_text().splitlines():
        if not line.startswith("| [QA-"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        link = LINK.match(cells[0])
        if not link or len(cells) != 7:
            sys.exit(f"BUGS.md: a row I cannot read, fix it by hand first: {line}")
        keys = ("status", "severity", "area", "title", "reporter", "fixer")
        found.append({"id": link.group(1), "file": link.group(2), **dict(zip(keys, cells[1:]))})
    return found


def write_rows(items):
    """Write the index rows back, keeping the text above the table."""
    text = INDEX.read_text()
    head = text[: text.index("| Id |")]
    table = "| Id | Status | Severity | Area | Title | Reporter | Fixer |\n|---|---|---|---|---|---|---|\n"
    lines = [
        f"| [{r['id']}]({r['file']}) | {r['status']} | {r['severity']} | {r['area']} | {r['title']} | {r['reporter']} | {r['fixer']} |"
        for r in items
    ]
    INDEX.write_text(head + table + "\n".join(lines) + "\n")


def set_field(path, field, value):
    """Set one row of a bug file's field table."""
    text = path.read_text()
    pattern = re.compile(rf"^\| {field} \|.*\|$", re.MULTILINE)
    path.write_text(pattern.sub(f"| {field} | {value} |", text, count=1))


def append_note(path, section, note):
    """Add a timestamped line at the end of one section of a bug file."""
    text = path.read_text()
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    marker = f"## {section}\n"
    if marker not in text:
        text += f"\n{marker}"
    start = text.index(marker) + len(marker)
    end = text.find("\n## ", start)
    end = len(text) if end == -1 else end + 1
    body = text[start:end].rstrip("\n")
    text = text[:start] + (body + "\n" if body.strip() else "\n") + f"- {stamp}: {note}\n" + text[end:]
    path.write_text(text)


def slug(title):
    """Return a short file-name slug of a title."""
    words = re.sub(r"[^a-z0-9]+", " ", title.lower()).split()
    return "-".join(words[:6]) or "bug"


def find(items, bug):
    """Return the row of a bug id, or exit."""
    for row in items:
        if row["id"] == bug.upper():
            return row
    sys.exit(f"{bug}: no such bug in BUGS.md")


def cmd_new(args):
    """Take the next id, add its row and file, commit and push; print the paths."""
    items = rows()
    number = max((int(r["id"][3:]) for r in items), default=0) + 1
    bug = f"QA-{number:03d}"
    if args.severity not in SEVERITIES:
        sys.exit(f"severity: expected one of {', '.join(SEVERITIES)}")
    title = args.title.replace("|", "/")
    path = BUGS / f"{bug}-{slug(title)}.md"
    text = TEMPLATE.read_text().replace("QA-<nnn>", bug).replace("<title, one line>", title)
    path.write_text(text)
    set_field(path, "Severity", args.severity)
    set_field(path, "Area", args.area)
    set_field(path, "Reporter", args.reporter)
    set_field(path, "Found", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"))
    (EVIDENCE / bug).mkdir(parents=True, exist_ok=True)
    keep = EVIDENCE / bug / ".gitkeep"
    keep.touch()
    items.append({"id": bug, "file": f"bugs/{path.name}", "status": "open", "severity": args.severity,
                  "area": args.area, "title": title, "reporter": args.reporter, "fixer": ""})
    write_rows(items)
    publish(f"{bug}: reported by {args.reporter}: {title}", [INDEX, path, keep])
    print(f"{bug}\n{path}\n{EVIDENCE / bug}")


def claim(row, fixer):
    """Mark one open bug as fixing by ``fixer`` in the index and its file."""
    row["status"], row["fixer"] = "fixing", fixer
    path = HERE / row["file"]
    set_field(path, "Status", "fixing")
    set_field(path, "Fixer", fixer)
    return path


def cmd_claim(args):
    """Claim one bug; refuse one that is not open."""
    items = rows()
    row = find(items, args.bug)
    if row["status"] != "open":
        sys.exit(f"{row['id']} is {row['status']} (fixer: {row['fixer'] or 'none'}); not claimed")
    path = claim(row, args.fixer)
    write_rows(items)
    publish(f"{row['id']}: claimed by {args.fixer}", [INDEX, path])
    print(f"{row['id']}\n{path}")


def cmd_next(args):
    """Claim the open bug of the highest severity in the given areas, oldest first."""
    areas = {area.strip() for area in args.area.split(",")} if args.area else None
    items = rows()
    open_rows = [
        r for r in items
        if r["status"] == "open"
        and (areas is None or areas & {part.strip() for part in r["area"].split(",")})
    ]
    if not open_rows:
        return
    row = min(open_rows, key=lambda r: (SEVERITIES.index(r["severity"]) if r["severity"] in SEVERITIES else 9, r["id"]))
    path = claim(row, args.fixer)
    write_rows(items)
    publish(f"{row['id']}: claimed by {args.fixer}", [INDEX, path])
    print(f"{row['id']}\n{path}")


def cmd_set(args):
    """Change a bug's status (and fixer, area), with an optional note in its Fix or Retest section."""
    if args.status not in STATUSES:
        sys.exit(f"status: expected one of {', '.join(STATUSES)}")
    items = rows()
    row = find(items, args.bug)
    path = HERE / row["file"]
    row["status"] = args.status
    set_field(path, "Status", args.status)
    if args.fixer is not None:
        row["fixer"] = args.fixer
        set_field(path, "Fixer", args.fixer)
    if args.area is not None:
        row["area"] = args.area
        set_field(path, "Area", args.area)
    if args.note:
        section = "Retest" if args.status in ("verified",) or args.retest else "Fix"
        append_note(path, section, args.note)
    write_rows(items)
    publish(f"{row['id']}: {args.status}" + (f": {args.note}" if args.note else ""), [INDEX, path])
    print(f"{row['id']} {args.status}")


def cmd_save(args):
    """Commit and push a bug's file and evidence after you filled them in."""
    row = find(rows(), args.bug)
    publish(f"{row['id']}: details and evidence", [HERE / row["file"], EVIDENCE / row["id"]])
    print(f"{row['id']} saved")


SCENARIOS = HERE / "SCENARIOS.md"


def cmd_scenario(args):
    """Set the Status, Stopped at and Bugs cells of one scenario row; commit and push it."""
    lines = SCENARIOS.read_text().splitlines()
    for i, line in enumerate(lines):
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if line.startswith("| ") and cells and cells[0] == args.scenario.upper():
            if len(cells) != 6:
                sys.exit(f"SCENARIOS.md: row {cells[0]} has {len(cells)} cells, expected 6")
            for index, value in ((3, args.status), (4, args.stopped), (5, args.bugs)):
                if value is not None:
                    cells[index] = value.replace("|", "/")
            lines[i] = "| " + " | ".join(cells) + " |"
            break
    else:
        sys.exit(f"{args.scenario}: no such scenario in SCENARIOS.md")
    SCENARIOS.write_text("\n".join(lines) + "\n")
    publish(f"QA {args.scenario.upper()}: {args.status or ''} {args.stopped or ''}".strip(), [SCENARIOS])
    print(f"{args.scenario.upper()} updated")


def cmd_list(args):
    """Print the rows, filtered by status and area."""
    for row in rows():
        if args.status and row["status"] != args.status:
            continue
        if args.area and args.area not in row["area"]:
            continue
        print(f"{row['id']} {row['status']:9} {row['severity']:8} {row['area']:20} {row['fixer']:14} {row['title']}")


def main():
    """Parse the command, then run it under the lock, after a pull."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    new = sub.add_parser("new")
    new.add_argument("title")
    new.add_argument("--severity", required=True)
    new.add_argument("--area", required=True)
    new.add_argument("--reporter", required=True)
    one = sub.add_parser("claim")
    one.add_argument("bug")
    one.add_argument("--fixer", required=True)
    nxt = sub.add_parser("next")
    nxt.add_argument("--area")
    nxt.add_argument("--fixer", required=True)
    put = sub.add_parser("set")
    put.add_argument("bug")
    put.add_argument("--status", required=True)
    put.add_argument("--fixer")
    put.add_argument("--area", help="move the bug to other areas, e.g. geomind")
    put.add_argument("--note")
    put.add_argument("--retest", action="store_true")
    save = sub.add_parser("save")
    save.add_argument("bug")
    scen = sub.add_parser("scenario")
    scen.add_argument("scenario")
    scen.add_argument("--status")
    scen.add_argument("--stopped")
    scen.add_argument("--bugs")
    show = sub.add_parser("list")
    show.add_argument("--status")
    show.add_argument("--area")
    args = parser.parse_args()
    with open(LOCK, "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if args.command != "list":
            sync()
        {"new": cmd_new, "claim": cmd_claim, "next": cmd_next, "set": cmd_set, "save": cmd_save, "scenario": cmd_scenario, "list": cmd_list}[args.command](args)


if __name__ == "__main__":
    main()
