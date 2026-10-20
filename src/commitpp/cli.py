"""Command-line interface for Commit++."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from .core import KNOWN_TYPES, build_header, validate_header


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="commitpp", description="Build or validate Conventional Commit headers.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    check = subparsers.add_parser("check", help="validate an existing commit header")
    check.add_argument("header", help="complete one-line commit header")

    make = subparsers.add_parser("make", help="build a commit header from parts")
    make.add_argument("type", choices=sorted(KNOWN_TYPES), help="Conventional Commit type")
    make.add_argument("description", help="short imperative description")
    make.add_argument("--scope", help="optional affected area")
    make.add_argument("--breaking", action="store_true", help="mark a breaking change")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "check":
        issues = validate_header(args.header)
        if issues:
            for issue in issues:
                print(f"Invalid: {issue}", file=sys.stderr)
            return 1
        print("Valid")
        return 0
    try:
        header = build_header(args.type, args.description, scope=args.scope, breaking=args.breaking)
    except ValueError as exc:
        print(f"Invalid: {exc}", file=sys.stderr)
        return 1
    print(header)
    return 0
