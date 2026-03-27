import os

from file_utilities import collect_file_paths, collect_file_paths_absolute, compute_file_hash


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
    files_in_first = collect_file_paths(dir_1)
    files_in_second = collect_file_paths(dir_2)

    results = {
        'matching': [],
        'differing': [],
        'only_in_first': sorted(files_in_first - files_in_second),
        'only_in_second': sorted(files_in_second - files_in_first),
    }

    for relative_path in sorted(files_in_first & files_in_second):
        full_path_1 = os.path.join(dir_1, relative_path)
        full_path_2 = os.path.join(dir_2, relative_path)
        if compare_files(full_path_1, full_path_2, chunk_size):
            results['matching'].append(relative_path)
        else:
            results['differing'].append(relative_path)

    return results


def find_duplicates(directory, chunk_size=8192):
    """
    Scans a directory recursively and groups duplicate files.
    Uses a 3-stage filter: size → hash → byte-by-byte verification.
    """
    all_file_paths = collect_file_paths_absolute(directory)

    # Stage 1: Group by file size
    files_by_size = {}
    for file_path in all_file_paths:
        try:
            file_size = os.path.getsize(file_path)
            files_by_size.setdefault(file_size, []).append(file_path)
        except OSError:
            continue

    total_files = len(all_file_paths)
    duplicate_groups = []
    unique_count = 0

    for file_size, same_size_files in files_by_size.items():
        if len(same_size_files) == 1:
            unique_count += 1
            continue

        # Stage 2: Group by hash
        files_by_hash = {}
        for file_path in same_size_files:
            try:
                file_hash = compute_file_hash(file_path, chunk_size)
                files_by_hash.setdefault(file_hash, []).append(file_path)
            except OSError:
                continue

        for file_hash, same_hash_files in files_by_hash.items():
            if len(same_hash_files) == 1:
                unique_count += 1
                continue

            # Stage 3: Byte-by-byte verification
            clusters = []
            for file_path in same_hash_files:
                matched_cluster = False
                for cluster in clusters:
                    if compare_files(file_path, cluster[0], chunk_size):
                        cluster.append(file_path)
                        matched_cluster = True
                        break
                if not matched_cluster:
                    clusters.append([file_path])

            for cluster in clusters:
                if len(cluster) > 1:
                    duplicate_groups.append(sorted(cluster))
                else:
                    unique_count += 1

    return {
        'duplicates': duplicate_groups,
        'unique_count': unique_count,
        'total_files': total_files,
        'total_groups': len(duplicate_groups),
    }
