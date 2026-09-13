import unittest

from tools import generate_discovery


class DiscoveryTests(unittest.TestCase):
    def test_dataset_metadata_identifies_snapshot_and_distributions(self):
        dataset = {"dataset_version": "1.0.0"}
        stats = {"generated_at": "2026-09-13T06:39:43Z", "repository_count": 2}
        manifest = {"inclusion_policy": {"minimum_stars": 2000}}
        metadata = generate_discovery.render_dataset_metadata(dataset, stats, manifest)
        self.assertEqual(metadata["@type"], "Dataset")
        self.assertEqual(metadata["version"], "1.0.0")
        self.assertEqual(metadata["provenance"]["repositoryCount"], 2)
        self.assertEqual(metadata["inclusionPolicy"]["minimum_stars"], 2000)
        self.assertIn("github-public-api", metadata["provenance"]["source"])

    def test_slugify_is_stable_for_catalog_paths(self):
        self.assertEqual(generate_discovery.slugify("C++"), "c")
        self.assertEqual(generate_discovery.slugify("No declared language"), "no-declared-language")

    def test_readme_uses_actual_context_values(self):
        dataset = {"dataset_version": "1.0.0", "schema_version": "1.1.0", "repositories": [{"full_name": "example/project", "html_url": "https://github.com/example/project", "stars": 2500, "primary_language": "Python"}]}
        stats = {"generated_at": "2026-09-13T06:39:43Z", "repository_count": 1, "minimum_stars": 2000, "languages": {"Python": 1}, "categories": {"ai": 1}, "archived_repositories": 0, "no_primary_language": 0, "no_description": 0, "star_distribution": {"minimum": 2500, "maximum": 2500, "median": 2500}}
        manifest = {"inclusion_policy": {"minimum_stars": 2000}}
        readme = generate_discovery.render_readme(dataset, stats, manifest)
        self.assertIn("**1**", readme)
        self.assertIn("example/project", readme)
        self.assertIn("2026-09-13T06:39:43Z", readme)
        self.assertIn("Python", readme)
        self.assertNotIn("33,180", readme)

    def test_data_dictionary_uses_schema_fields(self):
        schema = {"required": ["repository_id"], "properties": {"repository_id": {"type": "integer"}, "custom_field": {"type": "string"}}}
        dictionary = generate_discovery.render_data_dictionary(schema)
        self.assertIn("`repository_id`", dictionary)
        self.assertIn("`custom_field`", dictionary)
        self.assertIn("yes", dictionary)


if __name__ == "__main__":
    unittest.main()
