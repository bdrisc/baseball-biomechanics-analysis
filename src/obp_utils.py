from pathlib import Path

import pandas as pd


def find_project_root(start=None):
    """
    Find the baseball-biomechanics-analysis project directory.

    This works whether a notebook is launched from the repository root
    or from one of the notebook subfolders.
    """
    start_path = Path(start or Path.cwd()).resolve()

    for candidate in [start_path, *start_path.parents]:
        if (candidate / "src").is_dir() and (candidate / "notebooks").is_dir():
            return candidate

    raise FileNotFoundError(
        "Could not locate the project root. Open the notebook from inside "
        "the baseball-biomechanics-analysis repository."
    )


def get_data_path(discipline, filename):
    """
    Return the path to a locally stored OpenBiomechanics CSV.
    """
    valid_disciplines = {"pitching", "hitting"}

    if discipline not in valid_disciplines:
        raise ValueError(
            f"discipline must be one of {valid_disciplines}, " f"not {discipline!r}"
        )

    project_root = find_project_root()
    file_path = project_root / "data" / "raw" / discipline / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Required OBP file was not found:\n{file_path}\n\n"
            "Confirm that the file is stored in the correct data/raw folder."
        )

    return file_path


def load_obp_csv(discipline, filename, **read_csv_kwargs):
    """
    Load an OpenBiomechanics CSV from the project's data/raw directory.
    """
    file_path = get_data_path(discipline, filename)
    return pd.read_csv(file_path, **read_csv_kwargs)
