import pytest
from PySide2.QtWidgets import QApplication
import sys

@pytest.fixture(scope="session")
def qapp():
    """Create a QApplication instance for all tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app
