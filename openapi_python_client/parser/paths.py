from typing import Iterable, Dict

import os.path


def table_names_from_paths(paths: Iterable[str]) -> Dict[str, str]:
    """Try to extract a suitable table name from endpoint paths.

    This function should be called with paths of ALL endpoints in the spec.

    E.g. `/api/v2/users/{id}` -> `users`

    Returns:
        dict of `{<path>: <table_name>}`
    """
    # Remove common prefix for endpoints. For example  all paths might
    # start with /api/v2 and we don't want this to be part of the name
    paths = list(paths)
    if not paths:
        return {}
    if len(paths) > 1:
        api_prefix = os.path.commonpath(paths)
        norm_paths = [p.removeprefix(api_prefix) for p in paths]
    else:
        norm_paths = paths

    # Get all path components without slashes and without {parameters}
    split_paths = [[p for p in path.split("/") if p and not p.startswith("{")] for path in norm_paths]

    return {key: "_".join(value) for key, value in zip(paths, split_paths)}
