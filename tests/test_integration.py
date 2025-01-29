import pytest
from PySide2.QtCore import Qt
from PySide2.QtTest import QTest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from widgets.main_window import MainWindow

def test_end_to_end_workflow(qapp):
    # Create main window
    window = MainWindow()
    
    # Enter functions
    QTest.keyClicks(window.func1_input, "x^2")
    QTest.keyClicks(window.func2_input, "2*x")
    
    # Modify plot settings
    window.plot_settings.domain_start.setValue(-5)
    window.plot_settings.domain_end.setValue(5)
    window.plot_settings.num_points.setValue(500)
    window.plot_settings.precision.setValue(3)
    
    # Click solve button
    QTest.mouseClick(window.solve_button, Qt.LeftButton)
    
    # Verify results
    assert window.error_label.text() == ""
    assert len(window.ax.lines) > 0
    assert window.intersection_table.rowCount() > 0

def test_domain_restrictions(qapp):
    window = MainWindow()
    
    # Test sqrt domain restriction
    window.func1_input.setText("sqrt(x)")
    window.func2_input.setText("x")
    window.solve_and_plot()
    
    # Verify plot shows only valid domain
    assert len(window.ax.lines) > 0
    x_data = window.ax.lines[0].get_xdata()
    assert all(x >= 0 for x in x_data)