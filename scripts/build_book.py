"""Execute notebooks in fresh kernels and build the student site."""

from pathlib import Path
import shutil
import subprocess
import sys

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT / "_build" / "student-book"


def main():
    STAGE.mkdir(parents=True, exist_ok=True)
    (STAGE / "notebooks").mkdir(exist_ok=True)
    for name in ("myst.yml", "index.md", "setup.md"):
        shutil.copyfile(ROOT / name, STAGE / name)

    for source in sorted((ROOT / "notebooks").glob("*.ipynb")):
        print(f"Executing {source.name}", flush=True)
        notebook = nbformat.read(source, as_version=4)
        executor = ExecutePreprocessor(
            timeout=180, kernel_name="python3", kernel_manager_class=CourseKernelManager
        )
        executor.preprocess(notebook, {"metadata": {"path": str(source.parent)}})
        nbformat.write(notebook, STAGE / "notebooks" / source.name)

    cli = Path(sys.executable).parent / "jupyter-book"
    subprocess.run([cli, "build", "--html", "--strict"], cwd=STAGE, check=True)


if __name__ == "__main__":
    from jupyter_client import KernelManager

    class CourseKernelManager(KernelManager):
        """Use the exact interpreter that invoked the build."""

        def format_kernel_cmd(self, extra_arguments=None):
            command = super().format_kernel_cmd(extra_arguments)
            command[0] = sys.executable
            return command

    main()
