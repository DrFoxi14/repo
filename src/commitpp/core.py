"""Build and validate Conventional Commit headers."""

from __future__ import annotations

from dataclasses import dataclass
import re

KNOWN_TYPES = frozenset(
    {"build", "chore", "ci", "docs", "feat", "fix", "perf", "refactor", "revert", "style", "test"}
)
_HEADER_RE = re.compile(
    r"^(?P<type>[a-z][a-z0-9-]*)(?:\((?P<scope>[A-Za-z0-9][A-Za-z0-9._/-]*)\))?(?P<breaking>!)?: (?P<description>\S(?:.*\S)?)$"
)
_SCOPE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]*$")
_TYPE_RE = re.compile(r"^[a-z][a-z0-9-]*$")


@dataclass(frozen=True, slots=True)
class CommitHeader:
    """Structured representation of a Conventional Commit header."""

    type: str
    description: str
    scope: str | None = None
    breaking: bool = False

    def render(self) -> str:
        """Return the canonical single-line header."""
        scope = f"({self.scope})" if self.scope else ""
        breaking = "!" if self.breaking else ""
        return f"{self.type}{scope}{breaking}: {self.description}"


def parse_header(header: str) -> CommitHeader:
    """Parse a header, raising ``ValueError`` when its structure is invalid."""
    if not isinstance(header, str):
        raise TypeError("header must be a string")
    if not header or "\n" in header or "\r" in header:
        raise ValueError("header must contain exactly one non-empty line")
    match = _HEADER_RE.fullmatch(header)
    if match is None:
        raise ValueError("expected 'type(scope)!: description' format")
    commit_type = match.group("type")
    if commit_type not in KNOWN_TYPES:
        allowed = ", ".join(sorted(KNOWN_TYPES))
        raise ValueError(f"unknown type '{commit_type}'; expected one of: {allowed}")
    return CommitHeader(
        type=commit_type,
        scope=match.group("scope"),
        breaking=bool(match.group("breaking")),
        description=match.group("description"),
    )


def validate_header(header: str, *, max_length: int = 72) -> list[str]:
    """Return validation errors; an empty list means the header is valid."""
    if not isinstance(header, str):
        return ["header must be a string"]
    try:
        parse_header(header)
    except (TypeError, ValueError) as exc:
        return [str(exc)]
    if max_length < 1:
        return ["max_length must be at least 1"]
    if len(header) > max_length:
        return [f"header is {len(header)} characters; maximum is {max_length}"]
    return []


def build_header(
    commit_type: str,
    description: str,
    *,
    scope: str | None = None,
    breaking: bool = False,
) -> str:
    """Build a valid header from its parts."""
    if not isinstance(commit_type, str) or not _TYPE_RE.fullmatch(commit_type):
        raise ValueError("type must be lowercase letters, digits, or hyphens and start with a letter")
    if commit_type not in KNOWN_TYPES:
        raise ValueError(f"unknown type '{commit_type}'")
    if not isinstance(description, str) or not description or description != description.strip():
        raise ValueError("description must be non-empty and have no surrounding whitespace")
    if "\n" in description or "\r" in description:
        raise ValueError("description must be a single line")
    if scope is not None and (not isinstance(scope, str) or not _SCOPE_RE.fullmatch(scope)):
        raise ValueError("scope must start with a letter or digit and contain only letters, digits, '.', '_', '/', or '-'")
    header = CommitHeader(commit_type, description, scope, bool(breaking)).render()
    issues = validate_header(header)
    if issues:
        raise ValueError(issues[0])
    return header
