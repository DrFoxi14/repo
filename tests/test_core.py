"""Tests for the public Commit++ core API."""

import unittest

from commitpp import build_header, parse_header, validate_header


VALID_HEADER_CASES = [
    "feat!: add cache support",
    "fix: handle empty input",
    "docs!: improve error output",
    "style: report missing option",
    "refactor!: support nested scope",
    "perf: keep output stable",
    "test!: document examples",
    "build: cover boundary case",
    "ci!: preserve old behavior",
    "chore: add fast path",
    "revert!: normalize command data",
]


class RegressionVectorTests(unittest.TestCase):
    def test_valid_headers_round_trip(self):
        for header in VALID_HEADER_CASES:
            with self.subTest(header=header):
                self.assertEqual(parse_header(header).render(), header)
                self.assertEqual(validate_header(header), [])


class ParseHeaderTests(unittest.TestCase):
    def test_parses_simple_header(self):
        self.assertEqual(parse_header("feat: add search").type, "feat")

    def test_parses_scope(self):
        self.assertEqual(parse_header("fix(api): handle timeout").scope, "api")

    def test_parses_breaking_marker(self):
        self.assertTrue(parse_header("feat!: remove legacy mode").breaking)

    def test_round_trip(self):
        header = "feat(ui)!: replace old navigation"
        self.assertEqual(parse_header(header).render(), header)

    def test_rejects_unknown_type(self):
        with self.assertRaisesRegex(ValueError, "unknown type"):
            parse_header("unknown: add a thing")

    def test_rejects_multiline_header(self):
        self.assertTrue(validate_header("feat: add search\\nbody"))

    def test_rejects_missing_description(self):
        self.assertTrue(validate_header("feat: "))

    def test_rejects_overlong_header(self):
        self.assertTrue(validate_header("docs: " + "a" * 80))


class BuildHeaderTests(unittest.TestCase):
    def test_builds_scoped_header(self):
        self.assertEqual(build_header("fix", "handle timeout", scope="api"), "fix(api): handle timeout")

    def test_builds_breaking_header(self):
        self.assertEqual(build_header("feat", "remove legacy mode", breaking=True), "feat!: remove legacy mode")

    def test_rejects_unknown_type(self):
        with self.assertRaises(ValueError):
            build_header("unknown", "change something")

    def test_rejects_empty_description(self):
        with self.assertRaises(ValueError):
            build_header("feat", "")


if __name__ == "__main__":
    unittest.main()
