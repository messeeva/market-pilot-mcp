import subprocess
from pathlib import Path


def main() -> int:
    project_root = Path(__file__).resolve().parents[2]

    result = subprocess.run(
        [
            "mcp",
            "dev",
            str(project_root / "dev_server.py"),
            "--with-editable",
            str(project_root),
        ],
        cwd=project_root,
        check=False,
    )

    return result.returncode
