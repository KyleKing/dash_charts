"""Test the file examples/ex_tabs.py."""

import pytest

from .configuration import no_log_errors
from .examples import ex_tabs


@pytest.mark.CHROME
def test_smoke_test_ex_tabs(dash_duo):
    dash_duo.start_server(ex_tabs.app.app)

    import time
    time.sleep(1)

    assert no_log_errors(dash_duo)
