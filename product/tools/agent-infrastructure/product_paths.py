"""Map installed repository paths to canonical repository-foundation product sources."""
from __future__ import annotations

from pathlib import Path, PurePosixPath


def source_path(product_root: Path, target_relative: str) -> Path:
    """Return the product-owned source for one path installed into a target repo."""
    product_root = Path(product_root).resolve()
    relative = PurePosixPath(target_relative)
    if relative.is_absolute() or ".." in relative.parts or "\\" in target_relative:
        raise ValueError(f"Invalid target path: {target_relative}")

    prefix_mappings = (
        (".agents/skills/", "skills/"),
        (".agents/profiles/", "profiles/"),
        ("toolkit/agent-infrastructure/", "tools/agent-infrastructure/"),
        ("toolkit/skills/", "tools/skills/"),
        ("toolkit/work-log/", "tools/work-log/"),
        ("toolkit/offers/", "tools/offers/"),
    )
    for target_prefix, source_prefix in prefix_mappings:
        if target_relative.startswith(target_prefix):
            return product_root / source_prefix / target_relative[len(target_prefix):]

    exact = {
        ".logs/README.md": "templates/repository/.logs/README.md",
        "docs/agent-context/decisions/README.md": "templates/repository/docs/agent-context/decisions/README.md.tmpl",
        "docs/agent-context/domain/README.md": "templates/repository/docs/agent-context/domain/README.md.tmpl",
        "docs/missions/README.md": "templates/capabilities/missions/docs/missions/README.md",
        "resources/README.md": "templates/repository/resources/README.md.tmpl",
        "toolkit/domain/README.md": "templates/capabilities/domain-inventories/toolkit/domain/README.md",
    }
    if target_relative in exact:
        return product_root / exact[target_relative]
    if target_relative.startswith("docs/agent-context/"):
        return product_root / "references" / target_relative.removeprefix("docs/agent-context/")
    if target_relative.startswith(("docs/project/", "resources/", "definitions/", "artifacts/", "public/", "toolkit/epics/")):
        return product_root / "templates/capabilities/client-project" / target_relative

    candidate = product_root / target_relative
    if candidate.is_file():
        return candidate
    raise ValueError(f"No product source mapping for target path: {target_relative}")
