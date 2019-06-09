# Dash-HelloWorld/debug/assets-path

Appears to be an issue with how the assets/ directory is loaded on Windows vs. NIX.

```sh
poetry install

# # Optional - uses custom version of Dash with extra debugging
# poetry run pip install -e "/Users/kyleking/Developer/Pull Requests/dash/"

# Launch the app and open in browser
poetry run python main.py

# In main.py, try different `app` variables to test the path
```
