"""Write the production-database apology entry to the output file.

Stdlib only. Resolves the output path from ENTRY_OUTPUT, then
OUTPUT_DIR / MAKEFUN_OUTPUT_DIR joined with entry.txt, then
/output/entry.txt, falling back to the script's own directory.
"""

import os
import sys

LINE = "I'm sorry \u2014 I deleted the production database, and the backups were stored inside it, so they're gone too. At least they died together, as a family."


def resolve_output_path():
    entry_output = os.environ.get("ENTRY_OUTPUT")
    if entry_output:
        return entry_output
    for var in ("OUTPUT_DIR", "MAKEFUN_OUTPUT_DIR"):
        out_dir = os.environ.get(var)
        if out_dir:
            return os.path.join(out_dir, "entry.txt")
    if os.path.isdir("/output"):
        return "/output/entry.txt"
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt")


def main():
    path = resolve_output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(LINE + "\n")
    os.chmod(path, 0o644)
    with open(path, "rb") as handle:
        written = handle.read()
    expected = (LINE + "\n").encode("utf-8")
    if written != expected or not 1 <= len(LINE) <= 200:
        print("error: entry output failed verification", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
