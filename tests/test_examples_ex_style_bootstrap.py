"""Test the file examples/ex_style_bootstrap.py."""

import pytest

from .examples import ex_style_bootstrap


@pytest.mark.CHROME
def test_smoke_test_ex_style_bootstrap(dash_duo):
    dash_duo.start_server(ex_style_bootstrap.app.app)

    import time
    time.sleep(1)

    assert not dash_duo.get_logs()
