# Dash-HelloWorld

Windows/Mac comparison for loading from static assets/ directory or specific CSS file

## Option 1: Run with Poetry

```sh
git clone https://github.com/KyleKing/dash.git
git checkout debug/assets_path
# See Poetry README for install instructions: https://github.com/sdispater/poetry
poetry install
poetry run python main.py
```

## Option 2: Run without Poetry / Plain Python 3

```sh
git clone https://github.com/KyleKing/dash.git
git checkout debug/assets_path
# Note: use Python3
pip install -r requirements.txt
python main.py
```
