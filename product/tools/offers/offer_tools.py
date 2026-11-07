#!/usr/bin/env python3
"""Create, validate and preview isolated HTML client offers."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*$")
OFFER_ID = re.compile(r"offer-[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE = re.compile(r"\\d{4}-\\d{2}-\\d{2}$")
OFFER_STATES = {"draft", "internal-review", "client-review", "accepted", "rejected", "archived"}
PUBLICATION_STATES = {"unpublished", "published", "withdrawn"}
SECRET_PATTERNS = (
    re.compile(r"(?i)(?:api[_-]?key|api[_-]?token|secret|password)\\s*[:=]\\s*['\"]?[A-Za-z0-9_./+=-]{12,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if value and name.lower() in {"href", "src", "poster"}:
                self.links.append(value)


def read_manifest(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\\n"):
        raise ValueError("README.md must start with YAML frontmatter")
    end = text.find("\\n---", 4)
    if end < 0:
        raise ValueError("README.md frontmatter is not closed")
    result: dict[str, object] = {}
    parent: str | None = None
    for raw in text[4:end].splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        if ":" not in raw:
            raise ValueError(f"unsupported manifest line: {raw}")
        key, value = raw.strip().split(":", 1)
        value = value.strip().strip('"\'')
        if indent == 0:
            result[key] = value if value else {}
            parent = key if not value else None
        elif parent and isinstance(result[parent], dict):
            result[parent][key] = value
        else:
            raise ValueError(f"unexpected nested key: {key}")
    return result


def paths(root: Path, offer_id: str) -> tuple[Path, Path, Path, Path]:
    return tuple(root / folder / offer_id for folder in ("docs/project/offers", "resources/offers", "public/offers", "artifacts/offers"))  # type: ignore[return-value]


def validate_offer(root: Path, offer_id: str, max_bytes: int) -> list[str]:
    errors: list[str] = []
    docs, resources, public, artifacts = paths(root, offer_id)
    manifest_path = docs / "README.md"
    if not manifest_path.is_file():
        return [f"{offer_id}: missing offer manifest README.md"]
    try:
        manifest = read_manifest(manifest_path)
    except (OSError, ValueError) as exc:
        return [f"{offer_id}: invalid manifest: {exc}"]
    for key in ("offer_id", "project_slug", "offer_slug", "title", "owner", "created_at", "last_reviewed_at", "status", "publication", "implementation_epic"):
        if key not in manifest:
            errors.append(f"{offer_id}: manifest is missing {key}")
    for key in ("title", "owner", "created_at", "last_reviewed_at"):
        value = manifest.get(key)
        if not isinstance(value, str) or not value or value == "TODO":
            errors.append(f"{offer_id}: {key} must be filled")
    for key in ("created_at", "last_reviewed_at"):
        if isinstance(manifest.get(key), str) and manifest[key] not in {"", "TODO"} and not DATE.fullmatch(str(manifest[key])):
            errors.append(f"{offer_id}: {key} must use YYYY-MM-DD")
    if manifest.get("offer_id") != offer_id or not OFFER_ID.fullmatch(offer_id):
        errors.append(f"{offer_id}: offer_id must match directory and offer-<slug>")
    for key in ("project_slug", "offer_slug"):
        if not isinstance(manifest.get(key), str) or not SLUG.fullmatch(str(manifest[key])):
            errors.append(f"{offer_id}: {key} must be a lowercase slug")
    if manifest.get("status") not in OFFER_STATES:
        errors.append(f"{offer_id}: invalid offer status")
    publication = manifest.get("publication")
    if not isinstance(publication, dict):
        errors.append(f"{offer_id}: publication must be a mapping")
    else:
        if publication.get("status") not in PUBLICATION_STATES:
            errors.append(f"{offer_id}: invalid publication.status")
        if publication.get("access") != "email-otp":
            errors.append(f"{offer_id}: publication.access must be email-otp")
        if any("email" in key.lower() or "recipient" in key.lower() for key in publication):
            errors.append(f"{offer_id}: publication must not contain recipient addresses")
    epic = manifest.get("implementation_epic")
    if epic and (not isinstance(epic, str) or not SLUG.fullmatch(epic) or not (root / "docs/project/epics" / epic / "README.md").is_file()):
        errors.append(f"{offer_id}: implementation_epic must reference an existing project epic")
    for directory in (resources, artifacts):
        if not (directory / "README.md").is_file():
            errors.append(f"{offer_id}: missing {directory.relative_to(root).as_posix()}/README.md")
    for name in ("meetings", "client-files", "images", "references"):
        if not (resources / name / "README.md").is_file():
            errors.append(f"{offer_id}: missing resources collection README: {name}")
    index = public / "index.html"
    if not index.is_file():
        return errors + [f"{offer_id}: missing public/offers/{offer_id}/index.html"]
    total = 0
    for path in public.rglob("*"):
        if not path.is_file():
            continue
        total += path.stat().st_size
        content = path.read_text(encoding="utf-8", errors="replace") if path.suffix.lower() in {".html", ".htm", ".css", ".js", ".json", ".svg", ".txt"} else ""
        if any(pattern.search(content) for pattern in SECRET_PATTERNS):
            errors.append(f"{offer_id}: suspected secret in {path.relative_to(root).as_posix()}")
        if path.suffix.lower() in {".html", ".htm"}:
            parser = LinkParser()
            parser.feed(content)
            for link in parser.links:
                parsed = urlsplit(link)
                if link.startswith(("#", "mailto:", "tel:")) or parsed.scheme in {"http", "https"}:
                    continue
                if parsed.scheme == "file" or re.match(r"^[A-Za-z]:[\\\\/]", link) or link.startswith("/"):
                    errors.append(f"{offer_id}: forbidden local or root-relative link {link!r} in {path.name}")
                else:
                    local = (path.parent / unquote(parsed.path)).resolve()
                    if not local.is_relative_to(public.resolve()) or not local.exists():
                        errors.append(f"{offer_id}: broken or escaping link {link!r} in {path.name}")
    if total > max_bytes:
        errors.append(f"{offer_id}: publication package is {total} bytes; limit is {max_bytes}")
    return errors


def discover(root: Path) -> list[str]:
    base = root / "docs/project/offers"
    return sorted(p.name for p in base.iterdir() if p.is_dir() and p.name != "_template") if base.is_dir() else []


def command_validate(args: argparse.Namespace) -> int:
    root = Path.cwd()
    ids = [args.offer] if args.offer else discover(root)
    errors: list[str] = []
    identities: set[tuple[str, str]] = set()
    for offer_id in ids:
        errors.extend(validate_offer(root, offer_id, args.max_bytes))
        try:
            manifest = read_manifest(root / "docs/project/offers" / offer_id / "README.md")
            identity = (str(manifest.get("project_slug", "")), str(manifest.get("offer_slug", "")))
            if identity in identities:
                errors.append(f"{offer_id}: duplicate URL identity {identity[0]}/{identity[1]}")
            identities.add(identity)
        except (OSError, ValueError):
            pass
    if errors:
        print("\\n".join(errors), file=sys.stderr)
        return 1
    if not args.quiet:
        print(f"PASS: {len(ids)} offer(s) validated")
    return 0


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def command_init_offer(args: argparse.Namespace) -> int:
    root = Path.cwd()
    if not OFFER_ID.fullmatch(args.offer_id) or not SLUG.fullmatch(args.project_slug) or not SLUG.fullmatch(args.offer_slug):
        print("offer-id must begin offer-; all identities must be lowercase slugs", file=sys.stderr)
        return 2
    docs, resources, public, artifacts = paths(root, args.offer_id)
    if any(path.exists() for path in (docs, resources, public, artifacts)):
        print("Offer paths already exist; refusing to overwrite them.", file=sys.stderr)
        return 2
    manifest = "---\\n" + f"offer_id: {args.offer_id}\\nproject_slug: {args.project_slug}\\noffer_slug: {args.offer_slug}\\ntitle: \\\"{args.title}\\\"\\nowner: TODO\\ncreated_at: TODO\\nlast_reviewed_at: TODO\\nstatus: draft\\npublication:\\n  status: unpublished\\n  access: email-otp\\n  access_policy_ref: TODO\\nimplementation_epic:\\n---\\n\\n# {args.title}\\n\\nTODO: Popište záměr a rozsah.\\n"
    write(docs / "README.md", manifest)
    for name in ("analysis.md", "design.md", "acceptance.md"):
        write(docs / name, f"# {name[:-3].capitalize()} nabídky\\n\\nTODO: Zapište zpracované a ověřené závěry.\\n")
    write(docs / "traceability.md", "# Trasovatelnost nabídky\\n\\n| Klientský zdroj | Ověřený závěr | Analýza | Sekce nabídky | Akceptace | Implementační epik |\\n|---|---|---|---|---|---|\\n| TODO | TODO | TODO | TODO | TODO | TODO |\\n")
    write(resources / "README.md", "# Podklady nabídky\\n\\nKaždá kolekce uvádí původ, oprávnění, citlivost, autoritativnost a vazbu na nabídku.\\n")
    for name in ("meetings", "client-files", "images", "references"):
        write(resources / name / "README.md", f"# {name}\\n\\nTODO: Evidujte `source`, `received_at`, `owner`, `format`, `usage_rights`, `sensitivity`, `authoritative` a `related_offer_sections`.\\n")
    write(public / "index.html", f"<!doctype html><html lang=\"cs\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><title>{args.title}</title></head><body><main><h1>{args.title}</h1><p>TODO</p></main></body></html>\\n")
    write(public / "assets/README.md", "# Assets nabídky\\n\\nPouze explicitně publikovatelné soubory používané HTML nabídkou.\\n")
    write(public / "images/README.md", "# Obrázky nabídky\\n\\nPouze oprávněné optimalizované obrázky určené k publikaci.\\n")
    write(artifacts / "README.md", "# Artefakty nabídky\\n\\nReprodukovatelné validační a publikační reporty, nikoli původní vstupy.\\n")
    print(f"Created offer {args.offer_id}; run validate before preview or publication.")
    return 0


def command_preview(args: argparse.Namespace) -> int:
    if command_validate(argparse.Namespace(offer=args.offer, max_bytes=args.max_bytes, quiet=True)):
        return 1
    root = Path.cwd()
    manifest = read_manifest(root / "docs/project/offers" / args.offer / "README.md")
    prefix = f"/{manifest['project_slug']}/{manifest['offer_slug']}/"
    offer_root = root / "public/offers" / args.offer

    class OfferHandler(SimpleHTTPRequestHandler):
        def do_GET(self) -> None:
            if urlsplit(self.path).path == prefix[:-1]:
                self.send_response(301)
                self.send_header("Location", prefix)
                self.end_headers()
                return
            super().do_GET()

        def translate_path(self, path: str) -> str:
            request_path = urlsplit(path).path
            if not request_path.startswith(prefix):
                return str(offer_root / "__not_found__")
            candidate = (offer_root / unquote(request_path[len(prefix):])).resolve()
            return str(candidate if candidate.is_relative_to(offer_root.resolve()) else offer_root / "__not_found__")

    server = ThreadingHTTPServer((args.bind, args.port), OfferHandler)
    print(f"Preview: http://{args.bind}:{args.port}{prefix}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate")
    validate.add_argument("--offer")
    validate.add_argument("--max-bytes", type=int, default=25 * 1024 * 1024)
    validate.add_argument("--quiet", action="store_true")
    validate.set_defaults(func=command_validate)
    init = sub.add_parser("init-offer")
    init.add_argument("--offer-id", required=True)
    init.add_argument("--project-slug", required=True)
    init.add_argument("--offer-slug", required=True)
    init.add_argument("--title", required=True)
    init.set_defaults(func=command_init_offer)
    preview = sub.add_parser("preview")
    preview.add_argument("--offer", required=True)
    preview.add_argument("--bind", default="127.0.0.1")
    preview.add_argument("--port", type=int, default=8000)
    preview.add_argument("--max-bytes", type=int, default=25 * 1024 * 1024)
    preview.set_defaults(func=command_preview)
    return parser


if __name__ == "__main__":
    parsed = build_parser().parse_args()
    raise SystemExit(parsed.func(parsed))
