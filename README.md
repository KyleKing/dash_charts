# Dash-HelloWorld/debug/assets-path

Appears to be an issue with how the assets/ directory is loaded on Windows vs. NIX.

```sh
poetry install

# # Optional - uses custom version of Dash with extra debugging
# poetry run pip install -e "/Users/kyleking/Developer/Pull Requests/dash/"

# Launch the app and open in browser
poetry run python main.py

# In main.py, try different `app` variables to test the path

# Build with PyInstaller
poetry run pyinstaller main.py --noupx --add-data ./styles/blue-bg.css:./styles --add-data styles/question.jpg:styles --onefile

# FIXME: for onefile, the styles.css isn't loaded. But this works for --onedir. In both, the questions.jpg file loads

```
