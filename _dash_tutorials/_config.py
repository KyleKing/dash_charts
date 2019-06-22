"""Configure Globals for Examples."""

from pathlib import Path

import dash

# Configure the path to the local assets directory
examplesDir = Path.cwd()
if 'examples' not in str(examplesDir):
    examplesDir = examplesDir / 'examples'
assetsDir = examplesDir / 'assets'

# Initialize the Dash application
app = dash.Dash(__name__, assets_folder=str(assetsDir))
