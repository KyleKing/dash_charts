"""Test the file examples/ex_px.py."""

from .examples import ex_px


def test_inin001_simple_callback(dash_duo):
    dash_duo.start_server(ex_px.app.app)

    import time
    time.sleep(2)

    assert not dash_duo.get_logs()
