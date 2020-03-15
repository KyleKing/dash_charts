"""Test the file examples/ex_multi_page.py."""

import pytest

from .examples import ex_multi_page


@pytest.mark.CHROME
def test_smoke_test_ex_multi_page(dash_duo):
    dash_duo.start_server(ex_multi_page.app.app)

    import time
    time.sleep(1)

    assert not dash_duo.get_logs()
