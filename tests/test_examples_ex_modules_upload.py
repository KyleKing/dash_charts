"""Test the file examples/ex_modules_upload.py."""

import time

import pytest

from .configuration import no_log_errors
from .examples import ex_modules_upload


@pytest.mark.INTERACTIVE()
def test_smoke_test_ex_modules_upload(dash_duo):
    """Test ex_modules_upload."""
    dash_duo.start_server(ex_modules_upload.app.app)

    time.sleep(1)  # act

    assert no_log_errors(dash_duo)
