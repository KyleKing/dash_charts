"""Test the assets_url app argument.

See docs: https://dash.plot.ly/dash-deployment-server/static-assets

"""

import dash
import dash_html_components as html

# Test two different image files based on the source directory
imgNames= ['casey-horner-1584668-unsplash.jpg', 'question.jpg']

# ======================================================================================================================

# # Should import the relative ./assets/ directory automatically
# app = dash.Dash(__name__)
# expec = 'beige background and nice landscape image (Photo by Casey Horner on Unsplash)'
# imgName, imgAlt = imgNames

# Should import the styles/ dir
from pathlib import Path
app = dash.Dash(__name__, assets_folder=str(Path('styles')))
expec = """light blue background and image of question mark from Wikipedia (Selena Wilke [Public domain]).
Favicon should a G from Google and not the official Plotly/Dash icon"""
imgName, imgAlt = imgNames[::-1]

# ======================================================================================================================

# The favicon ison is lost with PyInstaller
app._favicon = app.get_asset_url('favicon.ico')

app.layout = html.Div([
    html.Div(
        className='app-content',
        children=[
            html.H1(
                children='Dash App Testing',
            ),

            html.P(children='Expected Style: {}'.format(expec)),
            html.Img(src=app.get_asset_url(imgName)),

            # FIXME: this image is cached,by Dash...
            html.P(children='Below image should not exist'),
            html.Img(src=app.get_asset_url(imgAlt)),
        ],
    ),
])

if __name__ == '__main__':
    # FYI: For PyInstaller, debug must be False. Otherwise returns:
    #   "AttributeError: 'FrozenImporter' object has no attribute 'filename'"
    app.run_server(debug=False)
