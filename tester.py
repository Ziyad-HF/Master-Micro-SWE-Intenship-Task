# test_function_solver.py
import pytest
from PySide2.QtWidgets import QApplication
from index import MainWindow, FunctionParser

@pytest.fixture
def app(qtbot):
    test_app = QApplication([])
    return test_app

@pytest.fixture
def window(app, qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    return window

def test_function_parser_validation():
    parser = FunctionParser()
    
    # Test valid functions
    assert parser.validate_function("2*x + 1")[0] == True
    assert parser.validate_function("x^2 - 3*x")[0] == True
    assert parser.validate_function("log10(x)")[0] == True
    assert parser.validate_function("sqrt(x^2 + 1)")[0] == True
    
    # Test invalid functions
    assert parser.validate_function("2*x + @")[0] == False
    assert parser.validate_function("sin(x)")[0] == False  # sin not supported
    assert parser.validate_function("((2*x)")[0] == False  # unbalanced parentheses

def test_function_parser_evaluation():
    parser = FunctionParser()
    
    # Test basic arithmetic
    assert parser.evaluate("2*x + 1", 2) == 5
    assert parser.evaluate("x^2", 3) == 9
    
    # Test special functions
    assert abs(parser.evaluate("log10(100)", 0) - 2) < 1e-10
    assert parser.evaluate("sqrt(16)", 0) == 4
    
    # Test complex expression
    assert parser.evaluate("2*x^2 + 3*x + 1", 2) == 13

def test_gui_input_validation(window, qtbot):
    # Test invalid input
    window.func1_input.setText("2*x + @")
    window.func2_input.setText("x^2")
    qtbot.mouseClick(window.solve_button, Qt.LeftButton)
    assert window.error_label.text() != ""
    
    # Test valid input
    window.func1_input.setText("2*x + 1")
    window.func2_input.setText("x^2")
    qtbot.mouseClick(window.solve_button, Qt.LeftButton)
    assert window.error_label.text() == ""

def test_intersection_calculation(window, qtbot):
    # Test functions with known intersection
    window.func1_input.setText("x")
    window.func2_input.setText("x^2")
    qtbot.mouseClick(window.solve_button, Qt.LeftButton)
    
    # Check if plot was created
    assert len(window.ax.lines) == 2  # Two functions plotted
    assert len(window.ax.collections) > 0  # Intersection points plotted

if __name__ == '__main__':
    pytest.main(['-v', 'test_function_solver.py'])