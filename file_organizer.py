#!/usr/bin/env python3
"""
file_organizer.py - Organize the files in a directory into subfolders by type.

Each file in the target directory is moved into a category subfolder chosen
by its extension (PDFs/, Images/, Documents/, ...). Anything unrecognized goes
into Other/. Existing subfolders are left alone, name collisions are resolved
by appending " (1)", " (2)", ... and --dry-run previews the moves without
touching anything.

Usage:
    python file_organizer.py [directory] [--dry-run]
"""

import argparse
import shutil
import sys
from pathlib import Path

# Category folder name -> set of extensions (lowercase, with leading dot).
CATEGORIES = {
    "PDFs": {".pdf"},
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".svg"},
    "Documents": {".doc", ".docx", ".txt", ".md", ".rtf"},
    "Spreadsheets": {".xls", ".xlsx", ".csv"},
    "Archives": {".zip", ".rar", ".tar", ".gz"},
}
FALLBACK_CATEGORY = "Other"


def get_category(path):
    """Return the category folder name for a file based on its extension."""
    ext = path.suffix.lower()  # case-insensitive match: .PDF == .pdf
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return FALLBACK_CATEGORY


def unique_destination(dest_dir, filename, claimed):
    """
    Return a path in dest_dir for filename that isn't already taken.

    A path is taken if it exists on disk or is in `claimed` (destinations
    already planned this run - needed for --dry-run, where nothing actually
    moves). If dest_dir/filename is taken, try "name (1).ext", "name (2).ext",
    ... until a free name is found.
    """
    candidate = dest_dir / filename
    stem, suffix = Path(filename).stem, Path(filename).suffix
    counter = 1
    while candidate.exists() or candidate in claimed:
        candidate = dest_dir / f"{stem} ({counter}){suffix}"
        counter += 1
    return candidate


def organize(target, dry_run=False):
    """
    Move every file directly inside `target` into its category subfolder.

    Returns a tuple (moved_count, folders_used, error_count).
    """
    moved = 0
    errors = 0
    folders_used = set()
    claimed = set()  # destinations assigned so far (see unique_destination)

    # Never move this script itself if it lives in the target directory.
    this_script = Path(__file__).resolve()

    # Snapshot the listing first so moving files doesn't affect iteration.
    entries = sorted(target.iterdir())

    for entry in entries:
        # Skip directories (including our own category folders) - only
        # top-level files are organized.
        if not entry.is_file():
            continue
        if entry.resolve() == this_script:
            continue

        category = get_category(entry)
        dest_dir = target / category
        dest = unique_destination(dest_dir, entry.name, claimed)
        claimed.add(dest)

        rel_dest = dest.relative_to(target)
        if dry_run:
            print(f"[dry-run] {entry.name} -> {rel_dest}")
            moved += 1
            folders_used.add(category)
            continue

        try:
            # exist_ok=True: creating a folder that's already there is fine.
            dest_dir.mkdir(exist_ok=True)
            shutil.move(str(entry), str(dest))
            print(f"Moved {entry.name} -> {rel_dest}")
            moved += 1
            folders_used.add(category)
        except PermissionError:
            print(f"Error: permission denied moving '{entry.name}'", file=sys.stderr)
            errors += 1
        except OSError as exc:
            print(f"Error: could not move '{entry.name}': {exc}", file=sys.stderr)
            errors += 1

    return moved, folders_used, errors


def main():
    """Parse command-line arguments, validate the target, and run the organizer."""
    parser = argparse.ArgumentParser(
        description="Organize files in a directory into subfolders by file type."
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=".",
        help="directory to organize (default: current directory)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="show what would be moved without moving anything",
    )
    args = parser.parse_args()

    target = Path(args.directory).resolve()

    # Validate the target before doing any work.
    if not target.exists():
        print(f"Error: directory '{target}' does not exist.", file=sys.stderr)
        return 1
    if not target.is_dir():
        print(f"Error: '{target}' is not a directory.", file=sys.stderr)
        return 1

    try:
        moved, folders, errors = organize(target, dry_run=args.dry_run)
    except PermissionError:
        print(f"Error: permission denied reading '{target}'.", file=sys.stderr)
        return 1

    # Summary line, with correct singular/plural wording.
    verb = "Would move" if args.dry_run else "Moved"
    file_word = "file" if moved == 1 else "files"
    folder_word = "folder" if len(folders) == 1 else "folders"
    print(f"\n{verb} {moved} {file_word} into {len(folders)} {folder_word}.")
    if errors:
        print(f"{errors} file(s) could not be moved (see errors above).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
