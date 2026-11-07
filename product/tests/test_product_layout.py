"""Repository Foundation product layout and self-contained source mappings."""
from pathlib import Path
import json
import sys
import unittest


PRODUCT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PRODUCT / "tools/agent-infrastructure"))
from product_paths import source_path
import repository_architecture


class ProductLayout(unittest.TestCase):
    def test_descriptor_and_entrypoint(self):
        descriptor = json.loads((PRODUCT / "local-product.json").read_text(encoding="utf-8"))
        self.assertEqual(descriptor["namespace"], "repository-foundation")
        self.assertEqual(descriptor["groups"], [])
        self.assertTrue((PRODUCT / descriptor["entrypoint"]).is_file())
        self.assertTrue((PRODUCT / descriptor["agent_map"]).is_file())

    def test_every_capability_source_is_inside_product(self):
        targets = {item for bundle in repository_architecture.CAPABILITY_BUNDLES.values() for item in bundle}
        for target in sorted(targets):
            with self.subTest(target=target):
                source = source_path(PRODUCT, target)
                self.assertTrue(source.is_file(), source)
                self.assertTrue(source.resolve().is_relative_to(PRODUCT.resolve()))

    def test_all_product_skills_have_frontmatter(self):
        skills = sorted((PRODUCT / "skills").glob("*/SKILL.md"))
        self.assertGreaterEqual(len(skills), 20)
        for skill in skills:
            text = skill.read_text(encoding="utf-8-sig")
            self.assertTrue(text.startswith("---\n"), skill)
            self.assertIn("\nname:", text.split("---", 2)[1], skill)


if __name__ == "__main__":
    unittest.main()
