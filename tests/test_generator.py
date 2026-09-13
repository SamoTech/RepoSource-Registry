import copy
import unittest
from datetime import datetime, timezone
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
        self.reference_time = datetime(2026, 1, 1, tzinfo=timezone.utc)

    def test_classification_is_deterministic(self):
        record = {
            "topics": ["web", "ai", "web"],
            "stars": 12000,
            "pushed_at": "2025-12-01T00:00:00Z",
        }
        result = generate_list.classify(copy.deepcopy(record), self.cfg, self.reference_time)
        self.assertEqual(result["categories"], ["ai", "web"])
        self.assertEqual(result["popularity_band"], "10k+")
        self.assertEqual(result["activity_status"], "active")

    def test_classification_is_independent_of_execution_order(self):
        records = [
            {"topics": ["web"], "stars": 2000, "pushed_at": "2025-12-01T00:00:00Z"},
            {"topics": ["ai"], "stars": 5000, "pushed_at": "2025-01-01T00:00:00Z"},
        ]
        forward = [
            generate_list.classify(copy.deepcopy(record), self.cfg, self.reference_time)
            for record in records
        ]
        reverse = [
            generate_list.classify(copy.deepcopy(record), self.cfg, self.reference_time)
            for record in reversed(records)
        ][::-1]
        self.assertEqual(forward, reverse)

    def test_classification_boundary_dates(self):
        exactly_boundary = {
            "topics": [],
            "stars": 2000,
            "pushed_at": "2025-07-05T00:00:00Z",
        }
        beyond_boundary = {
            "topics": [],
            "stars": 2000,
            "pushed_at": "2025-07-04T00:00:00Z",
        }
        self.assertEqual(
            generate_list.classify(copy.deepcopy(exactly_boundary), self.cfg, self.reference_time)["activity_status"],
            "active",
        )
        self.assertEqual(
            generate_list.classify(copy.deepcopy(beyond_boundary), self.cfg, self.reference_time)["activity_status"],
            "inactive",
        )

    def test_classification_uses_explicit_timezone_aware_reference_time(self):
        record = {
            "topics": [],
            "stars": 2000,
            "pushed_at": "2025-07-01T00:00:00Z",
        }
        utc_result = generate_list.classify(copy.deepcopy(record), self.cfg, self.reference_time)
        offset_result = generate_list.classify(
            copy.deepcopy(record),
            self.cfg,
            datetime(2026, 1, 1, 3, tzinfo=timezone.utc),
        )
        self.assertEqual(utc_result["activity_status"], "inactive")
        self.assertEqual(offset_result["activity_status"], "inactive")

    def test_classification_does_not_require_wall_clock_time(self):
        record = {
            "topics": ["web"],
            "stars": 2000,
            "pushed_at": "2025-12-31T00:00:00Z",
        }
        first = generate_list.classify(copy.deepcopy(record), self.cfg, self.reference_time)
        second = generate_list.classify(copy.deepcopy(record), self.cfg, self.reference_time)
        self.assertEqual(first, second)

    def test_classification_missing_pushed_at_is_deterministic(self):
        record = {"topics": ["web"], "stars": 2000}
        first = generate_list.classify(copy.deepcopy(record), self.cfg, self.reference_time)
        second = generate_list.classify(copy.deepcopy(record), self.cfg, self.reference_time)
        self.assertEqual(first["activity_status"], "unknown")
        self.assertEqual(first, second)

    def test_classification_invalid_timestamp_follows_existing_contract(self):
        record = {
            "topics": [],
            "stars": 2000,
            "pushed_at": "not-a-timestamp",
        }
        with self.assertRaises(ValueError):
            generate_list.classify(record, self.cfg, self.reference_time)

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

    @staticmethod
    def _response(payload):
        response = Mock(status_code=200, headers={})
        response.json.return_value = payload
        return response

    def test_collect_query_full_first_page_partial_second_page(self):
        session = Mock()
        session.get.side_effect = [
            self._response({"items": list(range(100)), "incomplete_results": False}),
            self._response({"items": [100], "incomplete_results": False}),
            self._response({"total_count": 101, "items": [], "incomplete_results": False}),
        ]
        out = []
        generate_list.collect_query(session, "stars:2031..2060", 101, self.cfg, out)
        self.assertEqual(out, list(range(101)))
        self.assertEqual(session.get.call_count, 3)

    def test_collect_query_single_partial_first_page(self):
        session = Mock()
        session.get.side_effect = [
            self._response({"items": list(range(7)), "incomplete_results": False}),
            self._response({"total_count": 7, "items": [], "incomplete_results": False}),
        ]
        out = []
        generate_list.collect_query(session, "stars:2031..2060", 7, self.cfg, out)
        self.assertEqual(out, list(range(7)))
        self.assertEqual(session.get.call_count, 2)

    def test_collect_query_empty_page_after_results_terminates(self):
        session = Mock()
        session.get.side_effect = [
            self._response({"items": list(range(100)), "incomplete_results": False}),
            self._response({"items": [], "incomplete_results": False}),
        ]
        out = []
        generate_list.collect_query(session, "stars:2031..2060", 150, self.cfg, out)
        self.assertEqual(out, list(range(100)))
        self.assertEqual(session.get.call_count, 2)

    def test_collect_query_exact_multiple_does_not_fetch_extra_page(self):
        session = Mock()
        session.get.side_effect = [
            self._response({"items": list(range(100)), "incomplete_results": False}),
            self._response({"items": list(range(100, 200)), "incomplete_results": False}),
        ]
        out = []
        generate_list.collect_query(session, "stars:2000..2050", 200, self.cfg, out)
        self.assertEqual(out, list(range(200)))
        self.assertEqual(session.get.call_count, 2)

    def test_collect_query_one_result_over_page_boundary(self):
        session = Mock()
        session.get.side_effect = [
            self._response({"items": list(range(100)), "incomplete_results": False}),
            self._response({"items": [100], "incomplete_results": False}),
            self._response({"total_count": 101, "items": [], "incomplete_results": False}),
        ]
        out = []
        generate_list.collect_query(session, "stars:2000..2050", 101, self.cfg, out)
        self.assertEqual(len(out), 101)

    def test_collect_query_zero_results(self):
        session = Mock()
        out = []
        generate_list.collect_query(session, "stars:2000..2050", 0, self.cfg, out)
        self.assertEqual(out, [])
        self.assertEqual(session.get.call_count, 0)

    def test_collect_query_api_error_is_not_swallowed(self):
        session = Mock()
        response = Mock(status_code=422, headers={})
        response.raise_for_status.side_effect = RuntimeError("422 validation failed")
        session.get.return_value = response
        with self.assertRaises(RuntimeError):
            generate_list.collect_query(session, "stars:2031..2060", 1, self.cfg, [])

    def test_collect_query_malformed_items_is_rejected(self):
        session = Mock()
        session.get.return_value = self._response({"items": {}, "incomplete_results": False})
        with self.assertRaises(ValueError):
            generate_list.collect_query(session, "stars:2031..2060", 1, self.cfg, [])

    def test_collect_query_incomplete_results_is_fatal(self):
        session = Mock()
        session.get.return_value = self._response({"items": [1], "incomplete_results": True})
        with self.assertRaisesRegex(RuntimeError, "incomplete search results"):
            generate_list.collect_query(session, "stars:2031..2060", 1, self.cfg, [])

    def test_collect_query_dataset_change_refreshes_expected_count(self):
        session = Mock()
        session.get.side_effect = [
            self._response({"items": list(range(100)), "incomplete_results": False}),
            self._response({"items": list(range(100, 120)), "incomplete_results": False}),
            self._response({"total_count": 120, "items": [], "incomplete_results": False}),
        ]
        out = []
        generate_list.collect_query(session, "stars:2031..2060", 200, self.cfg, out)
        self.assertEqual(out, list(range(120)))
        self.assertEqual(session.get.call_count, 3)

    def test_collect_query_does_not_paginate_forever_on_empty_page(self):
        session = Mock()
        session.get.side_effect = [
            self._response({"items": [], "incomplete_results": False}),
        ]
        out = []
        generate_list.collect_query(session, "stars:2031..2060", 1000, self.cfg, out)
        self.assertEqual(out, [])
        self.assertEqual(session.get.call_count, 1)


if __name__ == "__main__":
    unittest.main()
