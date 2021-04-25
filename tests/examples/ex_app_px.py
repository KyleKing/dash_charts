"""Launch app_px."""

from dash_charts.app_px import InteractivePXApp
from dash_charts.utils_helpers import parse_dash_cli_args

instance = InteractivePXApp
app = instance()
app.create()
if __name__ == '__main__':
    app.run(**parse_dash_cli_args())
else:
    FLASK_HANDLE = app.get_server()
