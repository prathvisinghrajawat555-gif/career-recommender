import unittest
from logic.rules import recommend

class TestRecommend(unittest.TestCase):
    def test_basic_python(self):
        res = recommend("I like python and ml")
        self.assertTrue(any("Data Scientist" in r['role'] for r in res))

    def test_web(self):
        res = recommend("I enjoy javascript and design")
        self.assertTrue(any("Web Developer" in r['role'] for r in res))

    def test_excel(self):
        res = recommend("I like spreadsheets and business analysis")
        self.assertTrue(any("Data Analyst" in r['role'] for r in res))

if __name__ == '__main__':
    unittest.main()
