import unittest

from tools import publish


class PublishTests(unittest.TestCase):
    def test_slug_collision_is_resolved(self):
        slugs = publish.unique_slugs(["C", "C++", "C#"])
        self.assertEqual(len(set(slugs.values())), 3)
        self.assertIn("c", slugs.values())

    def test_formula_safe_change_comparison_ignores_generated_fields(self):
        old = {1: {"repository_id": 1, "full_name": "a/b", "stars": 2000, "indexed_at": "old", "activity_status": "active"}}
        new = [{"repository_id": 1, "full_name": "a/b", "stars": 2000, "indexed_at": "new", "activity_status": "inactive"}]
        result = publish.build_changes(old, new)
        self.assertEqual(result["summary"]["changed"], 0)

    def test_threshold_and_order_validation(self):
        payload = {"repositories": [
            {"repository_id": 2, "full_name": "z/repo", "stars": 3000},
            {"repository_id": 1, "full_name": "a/repo", "stars": 3000},
        ]}
        with self.assertRaises(ValueError):
            publish.validate_dataset(payload, 2000)


if __name__ == "__main__":
    unittest.main()
