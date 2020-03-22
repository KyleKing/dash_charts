"""Launch app_px."""

from dash_charts.app_px import InteractivePXApp
from dash_charts.dash_helpers import parse_cli_port

instance = InteractivePXApp
if __name__ == '__main__':
    port = parse_cli_port()
    app = instance()
    app.create()
    app.run(port=port, debug=True)
else:
    app = instance()
    app.create()
    FLASK_HANDLE = app.get_server()
