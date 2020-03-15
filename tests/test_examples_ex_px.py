"""Test the file examples/ex_px.py."""

import pytest

from .examples import ex_px


@pytest.mark.CHROME
def test_smoke_test_ex_px(dash_duo):
    dash_duo.start_server(ex_px.app.app)

    import time
    time.sleep(1)

    assert not dash_duo.get_logs()
