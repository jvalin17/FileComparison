import os
import hashlib


def collect_file_paths(directory):
    """Recursively collects all file paths relative to the given directory."""
    file_paths = set()
    for current_dir, subdirs, files in os.walk(directory):
        for file_name in files:
            relative_path = os.path.relpath(
                os.path.join(current_dir, file_name), directory
            )
            file_paths.add(relative_path)
    return file_paths


def collect_file_paths_absolute(directory):
    """Recursively collects all absolute file paths in the given directory."""
    file_paths = []
    for current_dir, subdirs, files in os.walk(directory):
        for file_name in files:
            file_paths.append(os.path.join(current_dir, file_name))
    return file_paths


def compute_file_hash(file_path, chunk_size=8192):
    """Computes SHA-256 hash of a file, reading in chunks."""
    file_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            file_hash.update(chunk)
    return file_hash.hexdigest()
