"""Test the file examples/ex_app_px.py."""

import pytest

from .examples import ex_app_px


@pytest.mark.CHROME
def test_smoke_test_ex_app_px(dash_duo):
    dash_duo.start_server(ex_app_px.app.app)

    import time
    time.sleep(1)

    assert not dash_duo.get_logs()
