"""Test the assets_url app argument.

See docs: https://dash.plot.ly/dash-deployment-server/static-assets

"""

import dash
import dash_html_components as html

# ======================================================================================================================

# # Should import the relative ./assets/ directory automatically
# app = dash.Dash(__name__)
# expec = 'beige background and nice landscape image (Photo by Casey Horner on Unsplash)'
# imgName = 'casey-horner-1584668-unsplash.jpg'

# Should import the styles/ dir
from pathlib import Path
app = dash.Dash(__name__, assets_folder=str(Path('styles')))
expec = 'light blue background and image of question mark from Wikipedia (Selena Wilke [Public domain])'
imgName = 'question.jpg'


# ======================================================================================================================

app.layout = html.Div([
    html.Div(
        className='app-content',
        children=[
            html.H1(
                children='Test Import Local Assets Styles',
            ),
            html.P(
                children='Expected Style: {}'.format(expec),
            ),
            # FIXME: this image is cached,by Dash...
            html.Img(src=app.get_asset_url(imgName)),
        ],
    ),
])

if __name__ == '__main__':
    # For PyInstaller, debug must be False. Otherwise returns:
    #   "AttributeError: 'FrozenImporter' object has no attribute 'filename'"
    app.run_server(debug=False)
