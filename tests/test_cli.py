"""Tests for the Commit++ CLI."""

import contextlib
import io
import unittest

from commitpp.cli import main


class CliTests(unittest.TestCase):
    def run_cli(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = main(list(args))
        return code, output.getvalue().strip()

    def test_check_accepts_valid_header(self):
        code, output = self.run_cli("check", "feat: add search")
        self.assertEqual((code, output), (0, "Valid"))

    def test_check_rejects_invalid_header(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(["check", "not a header"]), 1)

    def test_make_simple_header(self):
        code, output = self.run_cli("make", "feat", "add search")
        self.assertEqual((code, output), (0, "feat: add search"))

    def test_make_scoped_breaking_header(self):
        code, output = self.run_cli("make", "feat", "remove legacy mode", "--scope", "api", "--breaking")
        self.assertEqual((code, output), (0, "feat(api)!: remove legacy mode"))


if __name__ == "__main__":
    unittest.main()
