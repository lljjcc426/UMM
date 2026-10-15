import unittest
from scripts.validate_catalog import validate

class CatalogTest(unittest.TestCase):
    def test_valid_catalog(self):
        report = validate()
        self.assertTrue(report["passed"], report["errors"])
        self.assertGreater(report["records"], 90)

if __name__ == "__main__":
    unittest.main()
