import unittest
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

class TestFlightAndItineraryAccuracy(unittest.TestCase):
    def setUp(self):
        self.costs_file = ROOT / "costs-and-stays.md"
        self.approaches_file = ROOT / "itinerary-approaches.md"
        self.costs_content = self.costs_file.read_text(encoding="utf-8")
        self.approaches_content = self.approaches_file.read_text(encoding="utf-8")

    def test_hyd_ixe_flight_numbers_and_timings(self):
        """Verify IndiGo 6E 7581 (06:50 AM -> 08:35 AM) is documented correctly."""
        self.assertIn("6E 7581", self.costs_content)
        self.assertIn("06:50 AM", self.costs_content)
        self.assertIn("08:35 AM", self.costs_content)
        self.assertIn("sole operator of direct non-stop flights", self.costs_content)

    def test_hbx_hyd_flight_numbers_and_timings(self):
        """Verify Fly91 IC 3402 (21:25 PM -> 22:55 PM) and IndiGo 6E 7416 (09:55 AM) are documented."""
        self.assertIn("IC 3402", self.costs_content)
        self.assertIn("21:25 PM", self.costs_content)
        self.assertIn("22:55 PM", self.costs_content)
        self.assertIn("6E 7416", self.costs_content)
        self.assertIn("09:55 AM", self.costs_content)

    def test_verified_indigo_live_fares(self):
        """Verify flight cost table uses exact verified fares from IndiGo (₹8,331 Saver / ₹9,201 Flexi Plus)."""
        self.assertIn("8,331", self.costs_content)
        self.assertIn("9,201", self.costs_content)
        self.assertIn("24,993", self.costs_content)
        self.assertIn("IC 3402", self.costs_content)

    def test_all_markdown_links_valid(self):
        """Verify no broken markdown links in the repository."""
        link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
        for md_file in ROOT.glob("**/*.md"):
            if ".git" in md_file.parts:
                continue
            content = md_file.read_text(encoding="utf-8")
            for match in link_pattern.finditer(content):
                url = match.group(2)
                if url.startswith("http://") or url.startswith("https://") or url.startswith("#") or url.startswith("mailto:"):
                    continue
                target = url.split("#")[0]
                if not target:
                    continue
                resolved = (md_file.parent / target).resolve()
                self.assertTrue(resolved.exists(), f"Broken link in {md_file}: {url}")

if __name__ == "__main__":
    unittest.main()
