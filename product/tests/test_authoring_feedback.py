from __future__ import annotations

from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


PRODUCT = Path(__file__).resolve().parents[1]
TOOL = PRODUCT / "tools/authoring-feedback/authoring_feedback.py"
spec = importlib.util.spec_from_file_location("authoring_feedback", TOOL)
feedback = importlib.util.module_from_spec(spec)
spec.loader.exec_module(feedback)


def valid_event():
    return {
        "schema_version": "1.0",
        "event_id": "AF-test-run-0001",
        "run_id": "run-test-1",
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "project_ref": "project:test",
        "task": {"summary": "Test feedback recorder", "purpose_refs": ["issue:test"]},
        "resolution": None,
        "usages": [
            {
                "usage_id": "usage-skill",
                "kind": "skill",
                "id": "intra-table-changes",
                "product": "intranet-authoring",
                "group_id": "B.3",
                "source": "intranet-authoring/skills/intra-table-changes/SKILL.md",
                "version": "test",
                "sha256": None,
                "role": "primary",
                "stages": ["selected", "loaded", "executed", "validated"],
                "call_count": 1,
                "retry_count": 1,
                "outcome": "success",
                "attribution_confidence": 0.9,
            }
        ],
        "errors": [
            {
                "error_id": "err-1",
                "category": "validation",
                "status": "recovered",
                "summary": "Fixture failed and was corrected.",
                "usage_ids": ["usage-skill"],
                "detected_by_usage_id": "usage-skill",
                "recovered_by_usage_id": "usage-skill",
                "evidence_refs": ["validation:test"],
            }
        ],
        "completion": {
            "outcome": "success",
            "validation_state": "PASS",
            "successful_factors": ["Corrected fixture passed."],
            "dead_ends": [],
        },
        "human_feedback": {
            "status": "not_provided",
            "scope": "run",
            "rating_1_5": None,
            "comment": None,
        },
        "evidence_refs": ["validation:test"],
        "privacy": {"classification": "internal", "redacted": True},
    }


class AuthoringFeedbackTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / ".logs").mkdir()
        (self.root / ".logs/README.md").write_text("# Work logs\n", encoding="utf-8")

    def test_record_validate_and_scan(self):
        event = valid_event()
        path = feedback.record_event(self.root, event)
        self.assertTrue(path.is_file())
        embedded = list(feedback.embedded_events(self.root))
        self.assertEqual([event["event_id"]], [item[1]["event_id"] for item in embedded])
        aggregate = feedback.aggregate(self.root)
        item = next(iter(aggregate["capabilities"].values()))
        self.assertEqual(1, item["executed"])
        self.assertEqual(1, item["logical_use_count"])
        self.assertEqual(1, item["distinct_run_count"])
        self.assertEqual(1, item["retry_count"])
        self.assertEqual(1, item["recovered_errors"])

    def test_duplicate_event_is_rejected(self):
        event = valid_event()
        feedback.record_event(self.root, event)
        with self.assertRaisesRegex(feedback.FeedbackError, "duplicate event_id"):
            feedback.record_event(self.root, event)

    def test_loaded_is_not_executed(self):
        event = valid_event()
        event["usages"][0]["stages"] = ["selected", "loaded"]
        event["usages"][0]["call_count"] = 0
        event["errors"] = []
        feedback.record_event(self.root, event)
        item = next(iter(feedback.aggregate(self.root)["capabilities"].values()))
        self.assertEqual(1, item["loaded"])
        self.assertEqual(0, item["executed"])

    def test_unknown_usage_reference_and_sensitive_key_are_rejected(self):
        event = valid_event()
        event["errors"][0]["usage_ids"] = ["missing"]
        with self.assertRaisesRegex(feedback.FeedbackError, "unknown usage"):
            feedback.validate_event(event)
        event = valid_event()
        event["token"] = "forbidden"
        with self.assertRaisesRegex(feedback.FeedbackError, "forbidden"):
            feedback.validate_event(event)

    def test_schema_extras_timezone_and_duplicate_logical_use_are_rejected(self):
        event = valid_event()
        event["unexpected"] = True
        with self.assertRaisesRegex(feedback.FeedbackError, "unexpected fields"):
            feedback.validate_event(event)
        event = valid_event()
        event["recorded_at"] = "2026-11-09T08:00:00"
        with self.assertRaisesRegex(feedback.FeedbackError, "timezone"):
            feedback.validate_event(event)
        event = valid_event()
        duplicate = dict(event["usages"][0])
        duplicate["usage_id"] = "usage-skill-duplicate"
        event["usages"].append(duplicate)
        with self.assertRaisesRegex(feedback.FeedbackError, "logical run/version/role"):
            feedback.validate_event(event)


if __name__ == "__main__":
    unittest.main()
