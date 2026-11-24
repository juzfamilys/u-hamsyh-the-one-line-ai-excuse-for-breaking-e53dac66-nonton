#!/usr/bin/env python3
"""The One-Line AI Excuse for Breaking Production.

Writes exactly one line — the excuse — to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output). No network, pure Python stdlib, fully deterministic.
"""

import os

LINE = "I didn't break production \u2014 I gave it the day off it had been quietly requesting in the error logs for months."

MAX_LENGTH = 200


def validate(text: str) -> None:
    """Guard: the entry must be a single, clean, non-empty line."""
    if not text:
        raise ValueError("entry is empty")
    if len(text) > MAX_LENGTH:
        raise ValueError(f"entry is {len(text)} chars, over the {MAX_LENGTH} limit")
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")
    if "\n" in text or "\r" in text or "\t" in text:
        raise ValueError("entry contains a newline or tab character")
    if "  " in text:
        raise ValueError("entry contains a double space")
    # The em dash is a single Unicode character; make sure the line is
    # exactly the intended excuse, not a look-alike with a hyphen.
    if " - " in text or "--" in text:
        raise ValueError("entry uses a hyphen where the em dash belongs")


def main() -> None:
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    output_path = os.path.join(output_dir, "entry.txt")

    validate(LINE)

    os.makedirs(output_dir, exist_ok=True)
    # Exact UTF-8 bytes, no trailing newline.
    with open(output_path, "wb") as fh:
        fh.write(LINE.encode("utf-8"))

    # Read back and re-validate the exact bytes on disk.
    with open(output_path, "rb") as fh:
        on_disk = fh.read()
    if on_disk != LINE.encode("utf-8"):
        raise ValueError("bytes on disk do not match the entry")
    validate(on_disk.decode("utf-8"))

    print(f"Wrote {len(on_disk)} bytes to {output_path}")


if __name__ == "__main__":
    main()
