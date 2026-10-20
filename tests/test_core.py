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
    "feat(api): validate option names",
    "fix(api)!: reduce parser ambiguity",
    "docs(api): include useful details",
    "style(api)!: return clear errors",
    "refactor(api): support offline mode",
    "perf(api)!: accept custom config",
    "test(api): retain stable order",
    "build(api)!: print concise help",
    "ci(api): handle false values",
    "chore(api)!: add cache support",
    "revert(api): handle empty input",
    "feat(cli)!: improve error output",
    "fix(cli): report missing option",
    "docs(cli)!: support nested scope",
    "style(cli): keep output stable",
    "refactor(cli)!: document examples",
    "perf(cli): cover boundary case",
    "test(cli)!: preserve old behavior",
    "build(cli): add fast path",
    "ci(cli)!: normalize command data",
    "chore(cli): validate option names",
    "revert(cli)!: reduce parser ambiguity",
    "feat(core): include useful details",
    "fix(core)!: return clear errors",
    "docs(core): support offline mode",
    "style(core)!: accept custom config",
    "refactor(core): retain stable order",
    "perf(core)!: print concise help",
    "test(core): handle false values",
    "build(core)!: add cache support",
    "ci(core): handle empty input",
    "chore(core)!: improve error output",
    "revert(core): report missing option",
    "feat(ui)!: support nested scope",
    "fix(ui): keep output stable",
    "docs(ui)!: document examples",
    "style(ui): cover boundary case",
    "refactor(ui)!: preserve old behavior",
    "perf(ui): add fast path",
    "test(ui)!: normalize command data",
    "build(ui): validate option names",
    "ci(ui)!: reduce parser ambiguity",
    "chore(ui): include useful details",
    "revert(ui)!: return clear errors",
    "feat(docs): support offline mode",
    "fix(docs)!: accept custom config",
    "docs(docs): retain stable order",
    "style(docs)!: print concise help",
    "refactor(docs): handle false values",
    "perf(docs)!: add cache support",
    "test(docs): handle empty input",
    "build(docs)!: improve error output",
    "ci(docs): report missing option",
    "chore(docs)!: support nested scope",
    "revert(docs): keep output stable",
    "feat(tests)!: document examples",
    "fix(tests): cover boundary case",
    "docs(tests)!: preserve old behavior",
    "style(tests): add fast path",
    "refactor(tests)!: normalize command data",
    "perf(tests): validate option names",
    "test(tests)!: reduce parser ambiguity",
    "build(tests): include useful details",
    "ci(tests)!: return clear errors",
    "chore(tests): support offline mode",
    "revert(tests)!: accept custom config",
    "feat(build): retain stable order",
    "fix(build)!: print concise help",
    "docs(build): handle false values",
    "style(build)!: add cache support",
    "refactor(build): handle empty input",
    "perf(build)!: improve error output",
    "test(build): report missing option",
    "build(build)!: support nested scope",
    "ci(build): keep output stable",
    "chore(build)!: document examples",
    "revert(build): cover boundary case",
    "feat(ci)!: preserve old behavior",
    "fix(ci): add fast path",
    "docs(ci)!: normalize command data",
    "style(ci): validate option names",
    "refactor(ci)!: reduce parser ambiguity",
    "perf(ci): include useful details",
    "test(ci)!: return clear errors",
    "build(ci): support offline mode",
    "ci(ci)!: accept custom config",
    "chore(ci): retain stable order",
    "revert(ci)!: print concise help",
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
