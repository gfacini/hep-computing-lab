# HEP Computing Lab

Four introductory collider-computing lessons using JupyterLab and Pythia 8. See the [course overview](index.md) and [student setup](setup.md).

## Build and preview the student book

Use Python 3.12 and Node.js 24 on your PATH. From the repository root, after activating the virtual environment in the setup instructions:

```bash
python -m pip install --only-binary pythia8mc -e '.[build]'
python -m pytest -q
python scripts/build_book.py
python -m http.server 8000 --bind 127.0.0.1 --directory _build/student-book/_build/html
```

Open [the local preview](http://127.0.0.1:8000). The first build downloads a public book theme. The build executes each student notebook in a fresh kernel using the course environment, writes executed copies into a staging directory, and publishes only the staged student pages. Notebook sources stay clean. To stop the preview server, press Control-C.

## Publish on GitHub Pages

1. Push the repository to the intended GitHub repository on `main`.
2. In **Settings → Pages → Build and deployment**, select **GitHub Actions** as the source.
3. Run **Publish student book** manually from `main` for the first deployment if the initial push preceded Pages setup. The workflow also runs on subsequent pushes to `main`. Open the Pages deployment URL from the completed workflow.

Pull requests run the physics tests and build the book on Linux and Apple Silicon runners. The Pages workflow uses the configured URL path and deploys the built HTML only.

[Jupyter Book publishing guide](https://jupyterbook.org/stable/get-started/publish/) · [GitHub Pages configuration for MyST](https://mystmd.org/guide/deployment-github-pages)
