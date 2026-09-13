import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

import generate_list


class GeneratorTests(unittest.TestCase):
    def setUp(self):
        self.cfg = {
            "min_stars": 2000,
            "include_forks": False,
            "include_archived": True,
            "per_page": 100,
            "request_timeout_seconds": 1,
            "max_retries": 1,
            "dataset_version": "test",
            "categories": {"ai": ["ai", "llm"], "web": ["web"]},
        }

    def test_classification_is_deterministic(self):
        record = {
            "topics": ["web", "ai", "web"],
            "stars": 12000,
            "pushed_at": "2026-09-01T00:00:00Z",
        }
        result = generate_list.classify(record, self.cfg)
        self.assertEqual(result["categories"], ["ai", "web"])
        self.assertEqual(result["popularity_band"], "10k+")

    def test_normalization_uses_github_native_fields(self):
        repo = {
            "id": 123,
            "full_name": "example/project",
            "name": "project",
            "html_url": "https://github.com/example/project",
            "url": "https://api.github.com/repos/example/project",
            "stargazers_count": 2000,
            "forks_count": 10,
            "watchers_count": 5,
            "open_issues_count": 2,
            "language": "Python",
            "topics": ["python"],
            "owner": {"login": "example"},
            "license": {"spdx_id": "MIT"},
            "archived": False,
            "fork": False,
        }
        result = generate_list.normalize(repo, "2026-09-13T00:00:00Z", self.cfg)
        self.assertEqual(result["repository_id"], 123)
        self.assertEqual(result["source"], "github-public-api")
        self.assertEqual(result["stars"], 2000)

    def test_request_retries_transient_failure(self):
        session = Mock()
        failed = Mock(status_code=503, headers={})
        successful = Mock(status_code=200, headers={}, json=lambda: {"total_count": 1})
        session.get.side_effect = [failed, successful]
        result = generate_list.request_json(session, "https://api.github.com/test", {}, self.cfg)
        self.assertEqual(result["total_count"], 1)
        self.assertEqual(session.get.call_count, 2)

    def test_csv_formula_safety(self):
        self.assertEqual(generate_list.csv_safe("=SUM(A1:A2)"), "'=SUM(A1:A2)")
        self.assertEqual(generate_list.csv_safe("normal"), "normal")


if __name__ == "__main__":
    unittest.main()
