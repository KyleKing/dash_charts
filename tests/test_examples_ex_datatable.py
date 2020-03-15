"""Test the file examples/ex_datatable.py."""

import pytest

from .examples import ex_datatable


@pytest.mark.CHROME
def test_smoke_test_ex_datatable(dash_duo):
    dash_duo.start_server(ex_datatable.app.app)

    import time
    time.sleep(1)

    assert not dash_duo.get_logs()
