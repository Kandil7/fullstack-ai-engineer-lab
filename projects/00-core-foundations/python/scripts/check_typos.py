"""
_dev/check_typos.py
====================
Scans the entire Python module for common filename typos and
naming inconsistencies.

Usage:
    python _dev/check_typos.py
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Known correct spellings for common technical terms
DICTIONARY = {
    r"corrilation": "correlation",
    r"correltion": "correlation",
    r"correletion": "correlation",
    r"algorith": "algorithm",
    r"implment": "implement",
    r"inheritence": "inheritance",
    r"polimorphism": "polymorphism",
    r"encapsulation": "encapsulation",  # Check spelling
    r"iterat": "iterate",  # Watch for "iteratior" etc.
    r"multiproces": "multiprocess",
    r"threding": "threading",
    r"decorator": "decorator",  # Check for "decorator" vs "decorator"
    r"functool": "functools",
    r"itertool": "itertools",
    r"dataclass": "dataclasses",
    r"metaclass": "metaclasses",
    r"descriptor": "descriptors",
}

SKIP_DIRS = {".git", "__pycache__", ".mimocode", ".idea", "output"}


def check_filename_typos(dirpath: str, filename: str, typos: list):
    """Check a single filename against the dictionary."""
    lower = filename.lower()
    for pattern, correction in DICTIONARY.items():
        if re.search(pattern, lower):
            rel = os.path.relpath(os.path.join(dirpath, filename), HERE)
            typos.append((rel, pattern, correction))


def check_content_typos(filepath: str, typos: list):
    """Check file content for common typos in comments/docs."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except (UnicodeDecodeError, OSError):
        return
    
    for pattern, correction in DICTIONARY.items():
        for i, line in enumerate(content.split("\n"), 1):
            if re.search(pattern, line, re.IGNORECASE):
                rel = os.path.relpath(filepath, HERE)
                typos.append((f"{rel}:{i}", pattern, correction))


def main():
    typos = []
    
    print("Scanning for typos...")
    print()
    
    for dirpath, dirnames, filenames in os.walk(HERE):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            
            # Check filenames
            check_filename_typos(dirpath, filename, typos)
            
            # Check .py and .md file contents
            if filename.endswith((".py", ".md")):
                check_content_typos(filepath, typos)
    
    if typos:
        print(f"❌ Found {len(typos)} potential typo(s):")
        print()
        for filepath, pattern, correction in typos:
            print(f"  {filepath}")
            print(f"    → '{pattern}' might be '{correction}'")
        print()
        return 1
    else:
        print("✅ No typos found!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
