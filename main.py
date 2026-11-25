#!/usr/bin/env python3
"""Worst Fix Ever: Funniest Commit Message.

Writes one commit-message line (at most 100 characters) to
/output/entry.txt: a fix for duplicate emails that made the bug worse
by sending each duplicate twice as fast.

The gate requires /output/entry.txt to be UTF-8 text of 1 to 100
characters, not only white space, so the program validates the line
before writing it and writes it with no trailing newline, so the file
is exactly the message.
"""

import os
import sys

# The entry: a single commit-message line, imperative mood, the kind a
# tired engineer would actually type at the end of a bad day.
COMMIT_MESSAGE = "Fix duplicate emails by sending each one twice as fast"

MAX_LENGTH = 100


def validate(message: str) -> None:
    """Reject anything that would fail the gate or is not one line."""
    if not message or not message.strip():
        raise ValueError("commit message must not be empty or whitespace only")
    if len(message) > MAX_LENGTH:
        raise ValueError(
            f"commit message is {len(message)} characters, over the "
            f"{MAX_LENGTH}-character limit"
        )
    if message != message.strip():
        raise ValueError("commit message must not start or end with whitespace")
    if "\n" in message or "\r" in message:
        raise ValueError("commit message must be a single line")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in message):
        raise ValueError("commit message must not contain control characters")
    try:
        message.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError("commit message must be valid UTF-8") from exc


def main() -> int:
    validate(COMMIT_MESSAGE)
    output_dir = os.environ.get("ENTRY_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "entry.txt")
    with open(output_path, "w", encoding="utf-8", newline="") as fh:
        fh.write(COMMIT_MESSAGE)
    print(f"Wrote {len(COMMIT_MESSAGE)} characters to {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
