#!/usr/bin/env python3
"""Validate, append and aggregate Flexideo authoring feedback events."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import date, datetime
import json
from pathlib import Path
import re
import sys


SCHEMA_VERSION = "1.0"
EVENT_ID_RE = re.compile(r"^AF-[A-Za-z0-9][A-Za-z0-9._-]{5,127}$")
GROUP_RE = re.compile(r"^[A-E]\.[1-6]$")
SHA_RE = re.compile(r"^[a-f0-9]{64}$")
BLOCK_RE = re.compile(
    r"(?ms)^### Authoring feedback\s*\n\s*```json\s*\n(?P<payload>.*?)\n```\s*$"
)
STAGES = {"selected", "loaded", "executed", "validated", "rated"}
OUTCOMES = {"success", "partial", "failed", "blocked", "cancelled", "unknown"}
ERROR_CATEGORIES = {
    "routing", "guidance", "tool_defect", "tool_contract", "input",
    "host_environment", "permission", "external_runtime", "validation",
    "executor_misuse", "expected_gate", "unknown",
}
ERROR_STATUSES = {"recovered", "unresolved", "expected_gate"}
ROLES = {"primary", "supplemental", "validator", "executor", "reference", "feedback_collector"}
FORBIDDEN_KEYS = {
    "password", "secret", "token", "authorization", "credentials", "prompt",
    "raw_output", "chat", "conversation",
}


class FeedbackError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise FeedbackError(message)


def require_string(value, path: str) -> None:
    require(isinstance(value, str) and bool(value.strip()), f"{path} must be a non-empty string")


def require_bounded_string(value, path: str, maximum: int, nullable: bool = False) -> None:
    if nullable and value is None:
        return
    require_string(value, path)
    require(len(value) <= maximum, f"{path} exceeds {maximum} characters")


def require_object_keys(value: dict, path: str, allowed: set[str], required: set[str]) -> None:
    require(isinstance(value, dict), f"{path} must be an object")
    missing = sorted(required - set(value))
    unexpected = sorted(set(value) - allowed)
    require(not missing, f"{path} is missing required fields: {', '.join(missing)}")
    require(not unexpected, f"{path} contains unexpected fields: {', '.join(unexpected)}")


def require_ref_list(value, path: str) -> None:
    require(isinstance(value, list), f"{path} must be an array")
    require(len(value) == len(set(value)), f"{path} must contain unique values")
    for index, item in enumerate(value):
        require_bounded_string(item, f"{path}[{index}]", 500)


def reject_forbidden_keys(value, path="event") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            require(key.casefold() not in FORBIDDEN_KEYS, f"{path}.{key} is forbidden")
            reject_forbidden_keys(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            reject_forbidden_keys(child, f"{path}[{index}]")


def validate_event(event: dict) -> dict:
    require(isinstance(event, dict), "event must be an object")
    reject_forbidden_keys(event)
    required = {
        "schema_version", "event_id", "run_id", "recorded_at", "project_ref",
        "task", "usages", "errors", "completion", "human_feedback",
        "evidence_refs", "privacy",
    }
    require_object_keys(event, "event", required | {"resolution"}, required)
    require(event["schema_version"] == SCHEMA_VERSION, "unsupported schema_version")
    require_bounded_string(event["event_id"], "event_id", 131)
    require(bool(EVENT_ID_RE.fullmatch(event["event_id"])), "invalid event_id")
    require_bounded_string(event["run_id"], "run_id", 160)
    require_bounded_string(event["recorded_at"], "recorded_at", 80)
    try:
        recorded_at = datetime.fromisoformat(event["recorded_at"].replace("Z", "+00:00"))
    except ValueError as exc:
        raise FeedbackError("recorded_at must be ISO 8601 with timezone") from exc
    require(recorded_at.tzinfo is not None, "recorded_at must include timezone")
    require_bounded_string(event["project_ref"], "project_ref", 300)

    task = event["task"]
    require_object_keys(task, "task", {"summary", "purpose_refs"}, {"summary", "purpose_refs"})
    require_bounded_string(task["summary"], "task.summary", 1000)
    require_ref_list(task["purpose_refs"], "task.purpose_refs")

    resolution = event.get("resolution")
    if resolution is not None:
        resolution_keys = {"assembly_id", "resolution_id", "capability_lock_ref", "map_version", "map_sha256"}
        require_object_keys(resolution, "resolution", resolution_keys, set())
        for key, maximum in (("assembly_id", 160), ("resolution_id", 160), ("capability_lock_ref", 500), ("map_version", 80)):
            if key in resolution:
                require_bounded_string(resolution[key], f"resolution.{key}", maximum, nullable=True)
        if "map_sha256" in resolution:
            digest = resolution["map_sha256"]
            require(digest is None or (isinstance(digest, str) and SHA_RE.fullmatch(digest)), "resolution.map_sha256 is invalid")

    usages = event["usages"]
    require(isinstance(usages, list) and usages, "usages must be a non-empty array")
    usage_ids = set()
    logical_usages = set()
    for index, usage in enumerate(usages):
        path = f"usages[{index}]"
        required_usage = {"usage_id", "kind", "id", "product", "group_id", "source", "role", "stages", "call_count", "retry_count", "outcome"}
        allowed_usage = required_usage | {"version", "sha256", "attribution_confidence"}
        require_object_keys(usage, path, allowed_usage, required_usage)
        for key in ("usage_id", "id", "product", "source"):
            maximum = {"usage_id": 160, "id": 200, "product": 120, "source": 500}[key]
            require_bounded_string(usage[key], f"{path}.{key}", maximum)
        require(usage["usage_id"] not in usage_ids, f"duplicate usage_id {usage['usage_id']}")
        usage_ids.add(usage["usage_id"])
        require(usage.get("kind") in {"skill", "tool", "validator"}, f"{path}.kind is invalid")
        group = usage.get("group_id")
        require(group is None or (isinstance(group, str) and GROUP_RE.fullmatch(group)), f"{path}.group_id is invalid")
        digest = usage.get("sha256")
        require(digest is None or (isinstance(digest, str) and SHA_RE.fullmatch(digest)), f"{path}.sha256 is invalid")
        if "version" in usage:
            require_bounded_string(usage["version"], f"{path}.version", 120, nullable=True)
        require(usage["role"] in ROLES, f"{path}.role is invalid")
        version_identity = digest or usage.get("version") or "unversioned"
        logical_key = (usage["product"], usage["kind"], usage["id"], version_identity, usage["role"])
        require(logical_key not in logical_usages, f"{path} duplicates one logical run/version/role use")
        logical_usages.add(logical_key)
        stages = usage.get("stages")
        require(isinstance(stages, list) and stages, f"{path}.stages must be non-empty")
        require(len(stages) == len(set(stages)) and set(stages) <= STAGES, f"{path}.stages is invalid")
        require(usage.get("outcome") in OUTCOMES, f"{path}.outcome is invalid")
        for key in ("call_count", "retry_count"):
            require(isinstance(usage.get(key), int) and not isinstance(usage[key], bool) and usage[key] >= 0, f"{path}.{key} is invalid")
        confidence = usage.get("attribution_confidence")
        require(confidence is None or (isinstance(confidence, (int, float)) and not isinstance(confidence, bool) and 0 <= confidence <= 1), f"{path}.attribution_confidence is invalid")

    errors = event["errors"]
    require(isinstance(errors, list), "errors must be an array")
    error_ids = set()
    for index, error in enumerate(errors):
        path = f"errors[{index}]"
        required_error = {"error_id", "category", "status", "summary", "usage_ids", "evidence_refs"}
        allowed_error = required_error | {"detected_by_usage_id", "recovered_by_usage_id"}
        require_object_keys(error, path, allowed_error, required_error)
        require_bounded_string(error["error_id"], f"{path}.error_id", 160)
        require(error["error_id"] not in error_ids, f"duplicate error_id {error['error_id']}")
        error_ids.add(error["error_id"])
        require(error.get("category") in ERROR_CATEGORIES, f"{path}.category is invalid")
        require(error.get("status") in ERROR_STATUSES, f"{path}.status is invalid")
        require_bounded_string(error["summary"], f"{path}.summary", 1000)
        linked = error.get("usage_ids")
        require(isinstance(linked, list) and len(linked) == len(set(linked)) and set(linked) <= usage_ids, f"{path}.usage_ids contains duplicate or unknown usage")
        for key in ("detected_by_usage_id", "recovered_by_usage_id"):
            ref = error.get(key)
            require(ref is None or ref in usage_ids, f"{path}.{key} contains unknown usage")
        require_ref_list(error["evidence_refs"], f"{path}.evidence_refs")

    completion = event["completion"]
    completion_keys = {"outcome", "validation_state", "successful_factors", "dead_ends"}
    require_object_keys(completion, "completion", completion_keys, completion_keys)
    require(completion.get("outcome") in OUTCOMES, "completion.outcome is invalid")
    require(completion.get("validation_state") in {"PASS", "FAIL", "PARTIAL", "NOT_RUN", "UNKNOWN"}, "completion.validation_state is invalid")
    require(isinstance(completion.get("successful_factors"), list), "completion.successful_factors must be an array")
    require(isinstance(completion.get("dead_ends"), list), "completion.dead_ends must be an array")
    for index, factor in enumerate(completion["successful_factors"]):
        require_bounded_string(factor, f"completion.successful_factors[{index}]", 1000)
    for index, dead_end in enumerate(completion["dead_ends"]):
        path = f"completion.dead_ends[{index}]"
        required_dead_end = {"summary", "reason_abandoned"}
        require_object_keys(dead_end, path, required_dead_end | {"replacement_ref"}, required_dead_end)
        require_bounded_string(dead_end["summary"], f"{path}.summary", 1000)
        require_bounded_string(dead_end["reason_abandoned"], f"{path}.reason_abandoned", 1000)
        if "replacement_ref" in dead_end:
            require_bounded_string(dead_end["replacement_ref"], f"{path}.replacement_ref", 500, nullable=True)

    human = event["human_feedback"]
    required_human = {"status", "scope"}
    require_object_keys(human, "human_feedback", required_human | {"usage_ids", "rating_1_5", "comment"}, required_human)
    require(human.get("status") in {"not_asked", "requested", "received", "declined", "not_provided"}, "human_feedback.status is invalid")
    require(human.get("scope") in {"run", "usage"}, "human_feedback.scope is invalid")
    rating = human.get("rating_1_5")
    if human["status"] == "received":
        require(isinstance(rating, int) and 1 <= rating <= 5, "received human feedback requires rating_1_5")
    else:
        require(rating is None, "rating_1_5 is allowed only for received feedback")
    if "usage_ids" in human:
        linked = human["usage_ids"]
        require(isinstance(linked, list) and len(linked) == len(set(linked)) and set(linked) <= usage_ids, "human_feedback.usage_ids contains duplicate or unknown usage")
    if "comment" in human:
        require_bounded_string(human["comment"], "human_feedback.comment", 2000, nullable=True)

    require_ref_list(event["evidence_refs"], "evidence_refs")
    privacy = event["privacy"]
    privacy_keys = {"classification", "redacted"}
    require_object_keys(privacy, "privacy", privacy_keys, privacy_keys)
    require(privacy.get("classification") in {"internal", "client_confidential", "public"}, "privacy.classification is invalid")
    require(isinstance(privacy.get("redacted"), bool), "privacy.redacted must be boolean")
    return event


def load_event(path: Path) -> dict:
    try:
        event = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise FeedbackError(f"cannot read event: {exc}") from exc
    return validate_event(event)


def log_files(root: Path) -> list[Path]:
    logs = root / ".logs"
    return sorted(logs.glob("????/??/????-??-??.md")) if logs.is_dir() else []


def embedded_events(root: Path):
    for path in log_files(root):
        text = path.read_text(encoding="utf-8", errors="strict")
        for match in BLOCK_RE.finditer(text):
            try:
                event = json.loads(match.group("payload"))
            except json.JSONDecodeError as exc:
                raise FeedbackError(f"{path}: invalid embedded JSON: {exc}") from exc
            yield path, validate_event(event)


def repository(value: str) -> Path:
    root = Path(value).resolve()
    if not root.is_dir():
        raise argparse.ArgumentTypeError(f"repository does not exist: {root}")
    if not (root / ".logs" / "README.md").is_file():
        raise argparse.ArgumentTypeError(f"repository has no .logs/README.md: {root}")
    return root


def event_status(outcome: str) -> str:
    return {"success": "done", "partial": "partial", "blocked": "blocked"}.get(outcome, "partial")


def record_event(root: Path, event: dict, selected_date: date | None = None) -> Path:
    event = validate_event(event)
    for path, existing in embedded_events(root):
        if existing["event_id"] == event["event_id"]:
            raise FeedbackError(f"duplicate event_id {event['event_id']} in {path}")
    now = datetime.now().astimezone()
    day = selected_date or now.date()
    path = root / ".logs" / day.strftime("%Y") / day.strftime("%m") / f"{day.isoformat()}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        current = path.read_text(encoding="utf-8")
        require(current.startswith(f"# Pracovní log — {day.isoformat()}\n"), f"invalid work-log header: {path}")
    else:
        current = f"# Pracovní log — {day.isoformat()}\n\n"
        path.write_text(current, encoding="utf-8", newline="\n")
    timestamp = now.strftime("%H:%M") if day == now.date() else "00:00"
    products = sorted({usage["product"] for usage in event["usages"]})
    tags = ", ".join(["`authoring-feedback`", *[f"`{item}`" for item in products]])
    refs = list(dict.fromkeys(event["task"]["purpose_refs"] + event["evidence_refs"]))
    reference_lines = "\n".join(f"- {item}" for item in refs) if refs else "- Žádné."
    entry = (
        f"## {timestamp} — Authoring feedback: {event['task']['summary']}\n"
        f"- ID: `{event['event_id']}`\n"
        "- Typ: `investigation`\n"
        f"- Stav: `{event_status(event['completion']['outcome'])}`\n"
        f"- Témata: {tags}\n\n"
        "### Shrnutí\n\n"
        f"Authoring run `{event['run_id']}` skončil jako `{event['completion']['outcome']}`; "
        f"validace: `{event['completion']['validation_state']}`.\n\n"
        "### Změněné soubory\n\n"
        "- Neuvedeny; tento záznam eviduje průběh a účinnost authoringového běhu.\n\n"
        "### Ověření\n\n"
        "- Authoring Feedback Event prošel strukturální validací před zápisem.\n\n"
        "### Authoring feedback\n\n"
        "```json\n"
        f"{json.dumps(event, ensure_ascii=False, indent=2, sort_keys=True)}\n"
        "```\n\n"
        "### Odkazy\n\n"
        f"{reference_lines}\n"
    )
    with path.open("a", encoding="utf-8", newline="\n") as stream:
        if current and not current.endswith("\n\n"):
            stream.write("\n")
        stream.write(entry)
    return path


def aggregate(root: Path) -> dict:
    seen = set()
    capabilities = defaultdict(lambda: {
        "run_ids": set(), "selected": 0, "loaded": 0, "executed": 0,
        "validated": 0, "rated": 0, "call_count": 0, "retry_count": 0,
        "outcomes": Counter(), "errors": Counter(), "recovered_errors": 0,
    })
    event_count = 0
    for path, event in embedded_events(root):
        event_id = event["event_id"]
        require(event_id not in seen, f"duplicate event_id {event_id} in {path}")
        seen.add(event_id)
        event_count += 1
        by_usage = {}
        for usage in event["usages"]:
            version = usage.get("sha256") or usage.get("version") or "unversioned"
            key = f"{usage['product']}:{usage['kind']}:{usage['id']}@{version}#{usage['role']}"
            by_usage[usage["usage_id"]] = key
            item = capabilities[key]
            item["run_ids"].add(event["run_id"])
            for stage in STAGES:
                if stage in usage["stages"]:
                    item[stage] += 1
            item["call_count"] += usage["call_count"]
            item["retry_count"] += usage["retry_count"]
            item["outcomes"][usage["outcome"]] += 1
        for error in event["errors"]:
            for usage_id in error["usage_ids"]:
                key = by_usage.get(usage_id)
                if key:
                    capabilities[key]["errors"][error["category"]] += 1
                    if error["status"] == "recovered":
                        capabilities[key]["recovered_errors"] += 1
    rendered = {}
    for key, item in sorted(capabilities.items()):
        rendered[key] = {
            "logical_use_count": len(item["run_ids"]),
            "distinct_run_count": len(item.pop("run_ids")),
            **{name: item[name] for name in ("selected", "loaded", "executed", "validated", "rated", "call_count", "retry_count")},
            "outcomes": dict(sorted(item["outcomes"].items())),
            "errors": dict(sorted(item["errors"].items())),
            "recovered_errors": item["recovered_errors"],
        }
    return {"schema_version": SCHEMA_VERSION, "event_count": event_count, "capabilities": rendered}


def command_validate_event(args) -> int:
    event = load_event(args.event)
    print(f"PASS: {event['event_id']}")
    return 0


def command_record(args) -> int:
    event = load_event(args.event)
    path = record_event(args.repository, event, args.date)
    print(path.relative_to(args.repository).as_posix())
    print(event["event_id"])
    return 0


def command_validate(args) -> int:
    events = list(embedded_events(args.repository))
    ids = [event["event_id"] for _path, event in events]
    require(len(ids) == len(set(ids)), "duplicate event_id across work logs")
    print(f"PASS: {len(events)} authoring feedback event(s)")
    return 0


def command_scan(args) -> int:
    print(json.dumps(aggregate(args.repository), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("date must use YYYY-MM-DD") from exc


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)
    validate_event_parser = commands.add_parser("validate-event")
    validate_event_parser.add_argument("--event", type=Path, required=True)
    validate_event_parser.set_defaults(func=command_validate_event)
    record_parser = commands.add_parser("record")
    record_parser.add_argument("repository", type=repository)
    record_parser.add_argument("--event", type=Path, required=True)
    record_parser.add_argument("--date", type=parse_date)
    record_parser.set_defaults(func=command_record)
    validate_parser = commands.add_parser("validate")
    validate_parser.add_argument("repository", type=repository)
    validate_parser.set_defaults(func=command_validate)
    scan_parser = commands.add_parser("scan")
    scan_parser.add_argument("repository", type=repository)
    scan_parser.set_defaults(func=command_scan)
    return root


def main() -> int:
    try:
        args = parser().parse_args()
        return args.func(args)
    except FeedbackError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
