"""PyTest configuration."""


def pytest_configure(config):
    """Configure pytest with custom markers.

    Args:
        config: pytest configuration object

    """
    config.addinivalue_line(
        'markers',
        'CHROME: marks tests that opens a Chrome window to be skipped with `-m "not CHROME"`',
    )
