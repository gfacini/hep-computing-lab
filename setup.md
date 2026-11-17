# Set up the lab

The book displays executed examples and plots. To change or rerun cells, use JupyterLab on your Mac or the optional browser environment below. Basic Python familiarity with lists and loops helps. No data download is required.

## On a Mac

The supported wheel setup uses Python 3.12 on Apple Silicon with macOS 15 or newer. Run `uname -m` in Terminal to check that the shell reports `arm64` and `sw_vers -productVersion` to check macOS. On an Intel Mac or older macOS, use the Linux x86-64 environment below.

1. Get the course folder from your instructor and unpack it if needed. On GitHub, use **Code → Download ZIP** or clone the repository.
2. Install Python 3.12 from [Python.org](https://www.python.org/downloads/macos/). Open Terminal, type `cd` followed by a space, drag the course folder into Terminal, and press Return.
3. Run these commands from the course folder:

   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   python -m pip install --only-binary pythia8mc -e .
   python -m hep_lab.simulation --events 3
   jupyter lab
   ```

The smoke run prints `3 events` followed by a particle count. In JupyterLab, open `notebooks/01-terminal.ipynb`, select the Python 3 kernel and use **Kernel → Restart Kernel and Run All Cells**. Each notebook generates its own sample, so you can run it from a clean kernel without executing earlier lessons.

In a new Terminal tab, enter the course folder and run `source .venv/bin/activate` before running Python or starting JupyterLab. If the notebook reports a version other than 3.12 or cannot import `hep_lab`, close JupyterLab and restart it from the activated environment. If Pythia cannot find its XML files, remove a stale override with `unset PYTHIA8DATA` and repeat the smoke run. The wheel supplies those files.

[Pythia wheel files and Python API](https://pypi.org/project/pythia8mc/8.318.3/)

## In a browser with Codespaces

Once the course repository is available on GitHub, open **Code → Codespaces → Create codespace**. The configuration installs the lab in a Python 3.12 Linux environment. Open a notebook and select `.venv/bin/python` as the kernel. Use the integrated terminal for Lesson 1. A Codespace requires GitHub access and may use your account’s compute quota.

The same installation commands work on x86-64 Linux with Python 3.12 available.
