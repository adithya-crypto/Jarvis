import os
import subprocess
import glob


def list_files(directory=None):
    """List files in a directory. Defaults to Desktop."""
    if directory is None:
        directory = os.path.expanduser("~/Desktop")

    if not os.path.isdir(directory):
        return f"Directory not found: {directory}"

    files = os.listdir(directory)
    if not files:
        return f"The directory {directory} is empty."

    file_list = ", ".join(files[:15])
    total = len(files)
    suffix = f" and {total - 15} more" if total > 15 else ""
    return f"Found {total} items in {directory}: {file_list}{suffix}."


def find_file(filename, search_dir=None):
    """Search for a file by name pattern."""
    if search_dir is None:
        search_dir = os.path.expanduser("~")

    pattern = os.path.join(search_dir, "**", f"*{filename}*")
    matches = glob.glob(pattern, recursive=True)

    # Limit to first 5 results
    matches = matches[:5]

    if not matches:
        return f"No files matching '{filename}' found."

    result = f"Found {len(matches)} match(es): " + ", ".join(os.path.basename(m) for m in matches)
    return result


def open_file(filepath):
    """Open a file with the default macOS application."""
    expanded = os.path.expanduser(filepath)
    if not os.path.exists(expanded):
        return f"File not found: {filepath}"

    subprocess.run(["open", expanded])
    return f"Opening {os.path.basename(expanded)}."


def get_file_info(filepath):
    """Get basic info about a file."""
    expanded = os.path.expanduser(filepath)
    if not os.path.exists(expanded):
        return f"File not found: {filepath}"

    stat = os.stat(expanded)
    size_mb = stat.st_size / (1024 * 1024)
    return f"{os.path.basename(expanded)}: {size_mb:.2f} MB."
