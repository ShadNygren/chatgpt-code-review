import os
from typing import Iterable
from git import Repo

def list_code_files_in_repository(repo_url: str, extensions: list[str] = None) -> Iterable[str]:
    """Clone the GitHub repository and return a list of code files with the specified extensions."""
    if extensions is None:
        extensions = []  # Default to an empty list if no extensions are provided
    print("ShadDEBUG repo_url = " + repo_url)
    local_path = clone_github_repository(repo_url)
    print("ShadDEBUG local_path = " + local_path)
    return get_all_files_in_directory(local_path, extensions)

def clone_github_repository(repo_url: str) -> str:
    """Clone a GitHub repository and return the local path."""
    print("ShadDEBUG clone_github_repository")
    print("ShadDEBUG repo_url = " + repo_url)
    local_path = repo_url.split("/")[-1]
    print("ShadDEBUG local_path = " + local_path)

    if not os.path.exists(local_path):
        Repo.clone_from(repo_url, local_path)
        print("ShadDEBUG - should be after Repo.clone")
    else:
        print("ShadDEBUG - os.path.exists(local_path) = " + str(os.path.exists(local_path)))

    return local_path

def get_all_files_in_directory(path: str, extensions: list[str] = None) -> list[str]:
    """Return a list of all files in a directory with the specified extension."""
    if extensions is None:
        extensions = []  # Ensure extensions is always a list
    files = []
    for root, _, filenames in os.walk(path):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in extensions):
                files.append(os.path.join(root, filename))
    return files

def create_file_tree(code_files: Iterable[str]) -> list[dict[str, str]]:
    """This function could be kept for internal logic or if a structured representation of files is needed elsewhere."""
    file_tree = []
    code_files = sorted(code_files)
    for file in code_files:
        parts = file.split(os.sep)
        current_level = file_tree
        for i, part in enumerate(parts):
            existing = [node for node in current_level if node["label"] == part]
            if existing:
                current_level = existing[0].setdefault("children", [])
            else:
                new_node = {"label": part, "value": os.sep.join(parts[: i + 1]),}
                current_level.append(new_node)
                if i != len(parts) - 1:
                    current_level = new_node.setdefault("children", [])
    return file_tree
