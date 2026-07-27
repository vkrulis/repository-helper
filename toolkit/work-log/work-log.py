#!/usr/bin/env python3
"""Create, search and validate repository work logs."""

from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta
from pathlib import Path
import re
import subprocess
import sys
import unicodedata

DAY_PATH_RE = re.compile(r"^\.logs/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{4}-\d{2}-\d{2})\.md$")
ENTRY_RE = re.compile(r"(?ms)^## (?P<title>.+?)\n(?P<body>.*?)(?=^## |\Z)")
FIELD_RE = re.compile(r"(?m)^- (?P<key>ID|Typ|Stav|Témata):\s*(?P<value>.+)$")
TYPES = ("change", "fix", "refactor", "docs", "decision", "maintenance", "investigation")
STATUSES = ("done", "partial", "planned", "blocked")


def repository(value: str) -> Path:
    root = Path(value).resolve()
    if not root.is_dir():
        raise argparse.ArgumentTypeError(f"Repozitář neexistuje: {root}")
    return root


def parse_day(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Datum musí mít formát YYYY-MM-DD") from exc


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")[:48] or "work"


def day_file(root: Path, selected: date) -> Path:
    return root / ".logs" / selected.strftime("%Y") / selected.strftime("%m") / f"{selected.isoformat()}.md"


def ensure_day(path: Path, selected: date) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    text = f"# Pracovní log — {selected.isoformat()}\n\n"
    path.write_text(text, encoding="utf-8")
    return text


def git_changes(root: Path) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "status", "--short"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return []
    if result.returncode:
        return []
    paths = []
    for line in result.stdout.splitlines():
        raw = line[3:].strip().strip('"')
        if " -> " in raw:
            raw = raw.split(" -> ", 1)[1]
        if raw and raw not in paths:
            paths.append(raw.replace("\\", "/"))
    return paths


def linked_item(root: Path, log_path: Path, value: str) -> str:
    normalized = value.replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    candidate = root / normalized
    if candidate.exists():
        relative = Path("../../..") / normalized
        return f"[{normalized}]({relative.as_posix()})"
    return value


def bullets(values: list[str], fallback: str) -> str:
    return "\n".join(f"- {value}" for value in values) if values else f"- {fallback}"


def command_add(args: argparse.Namespace) -> int:
    root = args.repository
    now = datetime.now().astimezone()
    selected = args.date or now.date()
    path = day_file(root, selected)
    current = ensure_day(path, selected)
    prefix = f"{selected.isoformat()}-{now.strftime('%H%M')}-{slugify(args.title)}"
    entry_id = args.id or prefix
    suffix = 2
    while re.search(rf"(?m)^- ID:\s*`{re.escape(entry_id)}`\s*$", current):
        entry_id = f"{prefix}-{suffix}"
        suffix += 1
    changes = args.change or git_changes(root)
    changes = [linked_item(root, path, item) for item in changes]
    tags = ", ".join(f"`{tag}`" for tag in args.tag) if args.tag else "—"
    timestamp = now.strftime("%H:%M") if selected == now.date() else "00:00"
    sections = [
        f"## {timestamp} — {args.title}",
        f"- ID: `{entry_id}`",
        f"- Typ: `{args.type}`",
        f"- Stav: `{args.status}`",
        f"- Témata: {tags}",
        "",
        "### Shrnutí",
        "",
        args.summary.strip(),
    ]
    if args.context:
        sections += ["", "### Kontext", "", args.context.strip()]
    sections += ["", "### Změněné soubory", "", bullets(changes, "Neuvedeny.")]
    sections += ["", "### Ověření", "", bullets(args.validation, "Neprovedeno nebo neuvedeno.")]
    if args.next:
        sections += ["", "### Navazující práce", "", bullets(args.next, "Žádná.")]
    if args.decision:
        decisions = [linked_item(root, path, item) for item in args.decision]
        sections += ["", "### Rozhodnutí", "", bullets(decisions, "Žádná.")]
    if args.link:
        sections += ["", "### Odkazy", "", bullets(args.link, "Žádné.")]
    entry = "\n".join(sections).rstrip() + "\n"
    with path.open("a", encoding="utf-8", newline="\n") as stream:
        if current and not current.endswith("\n\n"):
            stream.write("\n")
        stream.write(entry)
    print(path.relative_to(root).as_posix())
    print(entry_id)
    return 0


def log_files(root: Path) -> list[Path]:
    return sorted((root / ".logs").glob("????/??/????-??-??.md")) if (root / ".logs").is_dir() else []


def entries(path: Path):
    text = path.read_text(encoding="utf-8", errors="replace")
    for match in ENTRY_RE.finditer(text):
        body = match.group("body").rstrip()
        fields = {m.group("key"): m.group("value") for m in FIELD_RE.finditer(body)}
        yield match.group("title"), body, fields


def command_search(args: argparse.Namespace) -> int:
    matches = []
    query = (args.query or "").casefold()
    for path in log_files(args.repository):
        selected = date.fromisoformat(path.stem)
        if args.from_date and selected < args.from_date:
            continue
        if args.to_date and selected > args.to_date:
            continue
        for title, body, fields in entries(path):
            blob = f"{title}\n{body}".casefold()
            if query and query not in blob:
                continue
            if args.type and fields.get("Typ", "").strip("`") != args.type:
                continue
            if args.status and fields.get("Stav", "").strip("`") != args.status:
                continue
            if args.tag and f"`{args.tag.casefold()}`" not in blob:
                continue
            matches.append((path, title, body))
    for path, title, body in reversed(matches[-args.limit:]):
        print(f"{path.relative_to(args.repository).as_posix()} :: {title}")
        if args.verbose:
            print(body, "\n")
    return 0 if matches else 1


def command_recent(args: argparse.Namespace) -> int:
    args.from_date = datetime.now().astimezone().date() - timedelta(days=args.days - 1)
    args.to_date = None
    args.query = None
    args.tag = None
    args.type = None
    args.status = None
    return command_search(args)


def command_validate(args: argparse.Namespace) -> int:
    root = args.repository
    errors = []
    readme = root / ".logs" / "README.md"
    if not readme.is_file():
        errors.append("Chybí .logs/README.md")
    ids: dict[str, str] = {}
    for path in log_files(root):
        rel = path.relative_to(root).as_posix()
        match = DAY_PATH_RE.match(rel)
        if not match or match["year"] != path.stem[:4] or match["month"] != path.stem[5:7]:
            errors.append(f"Neplatná cesta denního logu: {rel}")
        text = path.read_text(encoding="utf-8", errors="replace")
        if not text.startswith(f"# Pracovní log — {path.stem}\n"):
            errors.append(f"Neplatná hlavička: {rel}")
        found = list(entries(path))
        if not found:
            errors.append(f"Denní log nemá žádný záznam: {rel}")
        for title, _body, fields in found:
            for key in ("ID", "Typ", "Stav", "Témata"):
                if key not in fields:
                    errors.append(f"{rel} / {title}: chybí pole {key}")
            entry_id = fields.get("ID", "").strip("`")
            if entry_id:
                if entry_id in ids:
                    errors.append(f"Duplicitní ID {entry_id}: {ids[entry_id]} a {rel}")
                ids[entry_id] = rel
            entry_type = fields.get("Typ", "").strip("`")
            status = fields.get("Stav", "").strip("`")
            if entry_type and entry_type not in TYPES:
                errors.append(f"{rel} / {title}: neplatný typ {entry_type}")
            if status and status not in STATUSES:
                errors.append(f"{rel} / {title}: neplatný stav {status}")
            decision_section = re.search(r"(?ms)^### Rozhodnutí\s*$\n(?P<body>.*?)(?=^### |\Z)", _body)
            if decision_section:
                links = re.findall(r"\[[^]]+\]\(([^)]+)\)", decision_section.group("body"))
                if not links:
                    errors.append(f"{rel} / {title}: sekce Rozhodnutí nemá odkaz")
                for link in links:
                    target = (path.parent / link).resolve()
                    if not target.is_file():
                        errors.append(f"{rel} / {title}: neplatný odkaz na rozhodnutí {link}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"FAIL: {len(errors)} error(s)")
        return 1
    print(f"PASS: {len(log_files(root))} daily log file(s), {len(ids)} unique entry ID(s)")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add", help="Append a structured entry to a daily log")
    add.add_argument("repository", nargs="?", default=".", type=repository)
    add.add_argument("--title", required=True)
    add.add_argument("--type", choices=TYPES, default="change")
    add.add_argument("--status", choices=STATUSES, default="done")
    add.add_argument("--summary", required=True)
    add.add_argument("--context")
    add.add_argument("--change", action="append", default=[])
    add.add_argument("--validation", action="append", default=[])
    add.add_argument("--next", action="append", default=[])
    add.add_argument("--link", action="append", default=[])
    add.add_argument("--decision", action="append", default=[], help="Repository-relative ADR path")
    add.add_argument("--tag", action="append", default=[])
    add.add_argument("--date", type=parse_day)
    add.add_argument("--id")
    add.set_defaults(func=command_add)

    search = sub.add_parser("search", help="Search structured work-log entries")
    search.add_argument("repository", nargs="?", default=".", type=repository)
    search.add_argument("--query")
    search.add_argument("--tag")
    search.add_argument("--type", choices=TYPES)
    search.add_argument("--status", choices=STATUSES)
    search.add_argument("--from-date", type=parse_day)
    search.add_argument("--to-date", type=parse_day)
    search.add_argument("--limit", type=int, default=20)
    search.add_argument("--verbose", action="store_true")
    search.set_defaults(func=command_search)

    recent = sub.add_parser("recent", help="Show recent work-log entries")
    recent.add_argument("repository", nargs="?", default=".", type=repository)
    recent.add_argument("--days", type=int, default=7)
    recent.add_argument("--limit", type=int, default=20)
    recent.add_argument("--verbose", action="store_true")
    recent.set_defaults(func=command_recent)

    validate = sub.add_parser("validate", help="Validate work-log structure and metadata")
    validate.add_argument("repository", nargs="?", default=".", type=repository)
    validate.set_defaults(func=command_validate)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
