import os


def compare_files(file_1, file_2, chunk_size=8192):
    """
    Compares two files byte by byte.
    Returns True if the files match, False otherwise.
    """
    try:
        if os.path.samefile(file_1, file_2):
            return True

        file_1_size = os.path.getsize(file_1)
        file_2_size = os.path.getsize(file_2)

        file_size_read = 0

        if file_1_size != file_2_size:
            return False

        if file_2_size == 0:
            return True

        with open(file_1, "rb") as f1, open(file_2, "rb") as f2:
            while file_size_read < file_1_size:
                if f1.read(chunk_size) != f2.read(chunk_size):
                    return False
                file_size_read += chunk_size

        return True

    except (FileNotFoundError, PermissionError, OSError):
        return False


def compare_files_detailed(file_1, file_2, chunk_size=8192):
    """
    Compares two files and returns detailed results.
    Returns a dict with: 'match' (bool), 'reason' (str), 'first_diff_offset' (int or None)
    """
    try:
        if os.path.samefile(file_1, file_2):
            return {'match': True, 'reason': 'same_file', 'first_diff_offset': None}
    except OSError:
        pass

    try:
        size_1 = os.path.getsize(file_1)
        size_2 = os.path.getsize(file_2)
    except (FileNotFoundError, PermissionError, OSError) as e:
        return {'match': False, 'reason': f'error: {e}', 'first_diff_offset': None}

    if size_1 != size_2:
        return {'match': False, 'reason': 'size_mismatch', 'first_diff_offset': None}

    if size_1 == 0:
        return {'match': True, 'reason': 'both_empty', 'first_diff_offset': None}

    offset = 0
    with open(file_1, "rb") as f1, open(file_2, "rb") as f2:
        while offset < size_1:
            chunk_1 = f1.read(chunk_size)
            chunk_2 = f2.read(chunk_size)
            if chunk_1 != chunk_2:
                for i in range(len(chunk_1)):
                    if i < len(chunk_2) and chunk_1[i] != chunk_2[i]:
                        return {'match': False, 'reason': 'content_mismatch', 'first_diff_offset': offset + i}
            offset += chunk_size

    return {'match': True, 'reason': 'identical', 'first_diff_offset': None}


def compare_directories(dir_1, dir_2, chunk_size=8192):
    """
    Compares two directories recursively.
    Returns a dict with keys: 'matching', 'differing', 'only_in_first', 'only_in_second'
    """
    results = {
        'matching': [],
        'differing': [],
        'only_in_first': [],
        'only_in_second': []
    }

    files_1 = set()
    for root, dirs, files in os.walk(dir_1):
        for f in files:
            rel_path = os.path.relpath(os.path.join(root, f), dir_1)
            files_1.add(rel_path)

    files_2 = set()
    for root, dirs, files in os.walk(dir_2):
        for f in files:
            rel_path = os.path.relpath(os.path.join(root, f), dir_2)
            files_2.add(rel_path)

    results['only_in_first'] = sorted(files_1 - files_2)
    results['only_in_second'] = sorted(files_2 - files_1)

    for rel_path in sorted(files_1 & files_2):
        f1 = os.path.join(dir_1, rel_path)
        f2 = os.path.join(dir_2, rel_path)
        if compare_files(f1, f2, chunk_size):
            results['matching'].append(rel_path)
        else:
            results['differing'].append(rel_path)

    return results
