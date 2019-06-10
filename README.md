# Dash-HelloWorld/debug/assets-path

Demo using the assets/ folder or a custom one on Windows and Mac/UNIX. Additionally can be built with pyInstaller.

```sh
poetry install

# # Optional - uses custom version of Dash with extra debugging
# poetry run pip install -e "/Users/kyleking/Developer/Pull Requests/dash/"

# Launch the app and open in browser
poetry run python main.py

# In main.py, try different `app` variables to test the path

# FIXME: are styles/ and assets/ directories added to onefile output by PyInstaller automatically?
poetry run pyinstaller main.py --noupx --onefile

# Build with PyInstaller (Windows)
poetry run pyinstaller main.py --noupx --add-data styles;styles --onefile
poetry run pyinstaller main.py --noupx --add-data styles/blue-bg.css;styles --add-data styles/question.jpg;styles --add-data styles/favicon.ico;styles --onefile
# Build with PyInstaller (*NIX)
poetry run pyinstaller main.py --noupx --add-data styles/blue-bg.css:styles --add-data styles/question.jpg:styles --onefile
```
