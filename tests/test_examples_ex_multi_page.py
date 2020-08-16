"""Test the file examples/ex_multi_page.py."""

import time

import pytest

from .configuration import no_log_errors
from .examples import ex_multi_page


@pytest.mark.CHROME
def test_smoke_test_ex_multi_page(dash_duo):
    """Test ex_multi_page."""
    dash_duo.start_server(ex_multi_page.app.app)

    time.sleep(1)  # act

    assert no_log_errors(dash_duo)
