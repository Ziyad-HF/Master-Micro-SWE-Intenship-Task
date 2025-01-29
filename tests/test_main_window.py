import pytest
from PySide2.QtCore import Qt
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from widgets.main_window import MainWindow

@pytest.fixture
def window(qapp):
    return MainWindow()

def test_window_creation(window):
    assert window.windowTitle() == "Function Solver"
    assert window.isVisible() == False

def test_input_validation(window):
    # Test empty inputs
    window.func1_input.setText("")
    window.func2_input.setText("")
    window.solve_and_plot()
    assert "Please enter both functions" in window.error_label.text()
    
    # Test invalid function
    window.func1_input.setText("x + $")
    window.func2_input.setText("x + 1")
    window.solve_and_plot()
    assert "Invalid characters detected" in window.error_label.text()

def test_valid_functions(window):
    window.func1_input.setText("x^2")
    window.func2_input.setText("2*x")
    window.solve_and_plot()
    assert window.error_label.text() == ""
    
    # Check if plot was created
    assert len(window.ax.lines) > 0

def test_intersection_points(window):
    window.func1_input.setText("x")
    window.func2_input.setText("x")
    window.solve_and_plot()
    
    # Should show intersection interval
    assert window.intersection_table.rowCount() > 0
    assert "Interval" in window.intersection_table.item(0, 0).text()
