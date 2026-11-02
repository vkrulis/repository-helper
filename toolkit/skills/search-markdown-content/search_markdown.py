#!/usr/bin/env python3
"""Deterministic AND/OR search over Markdown source files."""
from __future__ import annotations
import argparse, json, re, sys, unicodedata
from pathlib import Path

def fold(value: str, ignore: bool) -> str:
    value = value.casefold()
    if ignore:
        value = unicodedata.normalize("NFKD", value)
        value = "".join(c for c in value if not unicodedata.combining(c))
    return value

def groups(query: str) -> list[list[str]]:
    result = []
    for raw_group in query.split("|"):
        terms = [part.strip() for part in raw_group.split("+") if part.strip()]
        if terms: result.append(terms)
    if not result: raise ValueError("Dotaz neobsahuje žádný termín")
    return result

def title(text: str, path: Path) -> str:
    for line in text.splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if match: return match.group(1)
    return path.stem

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--query", required=True, help="OR skupiny oddělené |, AND termíny oddělené +")
    parser.add_argument("--glob", default="**/*.md")
    parser.add_argument("--ignore-diacritics", action="store_true")
    parser.add_argument("--regex", action="store_true")
    parser.add_argument("--context", type=int, default=1)
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--include-generated", action="store_true", help="Nevynechávat node_modules, .docusaurus ani site")
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
    root = args.root.resolve()
    parsed = groups(args.query)
    compiled = [[re.compile(term, re.I) for term in group] for group in parsed] if args.regex else None
    found = []
    excluded = {".git", "node_modules", ".docusaurus"}
    if not args.include_generated: excluded.add("site")
    for path in sorted(root.glob(args.glob)):
        if not path.is_file() or any(part in excluded for part in path.relative_to(root).parts): continue
        try: text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError: continue
        haystack = fold(text, args.ignore_diacritics)
        matched = []
        for index, group in enumerate(parsed):
            checks = []
            for term_index, term in enumerate(group):
                if args.regex: checks.append(bool(compiled[index][term_index].search(text)))
                else: checks.append(fold(term, args.ignore_diacritics) in haystack)
            if all(checks): matched.append(index)
        if not matched: continue
        lines = text.splitlines()
        hits = []
        for number, line in enumerate(lines, 1):
            if any((re.search(term, line, re.I) if args.regex else fold(term, args.ignore_diacritics) in fold(line, args.ignore_diacritics)) for group in parsed for term in group):
                start, end = max(1, number - args.context), min(len(lines), number + args.context)
                hits.append({"line": number, "text": "\n".join(f"{n}: {lines[n-1]}" for n in range(start, end + 1))})
                if len(hits) >= 3: break
        found.append({"path": path.relative_to(root).as_posix(), "title": title(text, path), "groups": [i + 1 for i in matched], "hits": hits})
    found = found[:args.limit]
    if args.json: print(json.dumps({"query": args.query, "groups": parsed, "results": found}, ensure_ascii=False, indent=2))
    else:
        print(f"Dotaz: {args.query}\nSkupiny: " + " OR ".join(" AND ".join(g) for g in parsed))
        for item in found:
            print(f"\n{item['path']} :: {item['title']} [OR skupiny: {','.join(map(str, item['groups']))}]")
            for hit in item["hits"]: print(hit["text"])
    return 0 if found else 1
if __name__ == "__main__": raise SystemExit(main())