from pathlib import Path
from typing import Optional


def get_project_path(start_path: Optional[Path] = None) -> Path:
    if start_path is None:
        start_path = Path.cwd()
    previous_path = None
    current_path = start_path.resolve()
    while previous_path != current_path:
        if (current_path / '.git').is_dir():
            return current_path
        previous_path = current_path
        current_path = current_path.parent
    raise FileNotFoundError("Could not find project path")
