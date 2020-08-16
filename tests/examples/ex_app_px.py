"""Launch app_px."""

from dash_charts.app_px import InteractivePXApp
from dash_charts.utils_dash import parse_dash_cli_args

instance = InteractivePXApp
if __name__ == '__main__':
    app = instance()
    app.create()
    app.run(**parse_dash_cli_args())
else:
    app = instance()
    app.create()
    FLASK_HANDLE = app.get_server()
