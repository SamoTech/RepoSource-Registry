import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class WebContractTests(unittest.TestCase):
    def test_required_web_surface_exists(self):
        required = [
            "package.json",
            "next.config.mjs",
            "app/layout.js",
            "app/page.js",
            "app/search/page.js",
            "app/repo/[owner]/[name]/page.js",
            "app/data/page.js",
            "app/globals.css",
            "app/robots.js",
            "app/sitemap.js",
            "docs/vercel.md",
        ]
        for path in required:
            self.assertTrue((ROOT / path).is_file(), path)

    def test_package_has_minimal_next_stack(self):
        package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
        self.assertIn("next", package["dependencies"])
        self.assertIn("react", package["dependencies"])
        self.assertIn("react-dom", package["dependencies"])
        self.assertEqual(package["scripts"]["build"], "next build")

    def test_web_layer_has_no_business_access_restriction_language(self):
        forbidden = (
            "premium api",
            "api subscription",
            "api pricing",
            "api billing",
            "paid-api",
            "enterprise api",
            "higher api limits",
            "api monetization",
        )
        files = list((ROOT / "app").rglob("*.js")) + [ROOT / "docs/vercel.md", ROOT / "README.md"]
        corpus = "\n".join(path.read_text(encoding="utf-8").lower() for path in files)
        for phrase in forbidden:
            self.assertNotIn(phrase, corpus, phrase)


if __name__ == "__main__":
    unittest.main()
