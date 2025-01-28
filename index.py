# main.py
from PySide2.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLineEdit, QPushButton, QLabel,
                               QTableWidget, QTableWidgetItem, QSplitter)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
import re
from math import sqrt, log10
import sys


class FunctionParser:
    """Parse and evaluate mathematical functions."""

    @staticmethod
    def validate_function(func_str):
        """
        Validate function string format.
        Returns (bool, str) tuple - (is_valid, error_message)
        """
        # Check for invalid characters
        allowed = set('x0123456789+-*/^() .logsqrt')
        if not all(c in allowed for c in func_str.lower()):
            return False, "Invalid characters detected. Allowed: numbers, x, +, -, *, /, ^, log10(), sqrt()"

        # Check for balanced parentheses
        if func_str.count('(') != func_str.count(')'):
            return False, "Unbalanced parentheses"

        # Basic format validation using regex
        try:
            # Replace valid function patterns with 'x' to simplify validation
            simplified = func_str.lower()
            simplified = re.sub(r'log10\([^)]+\)', 'x', simplified)
            simplified = re.sub(r'sqrt\([^)]+\)', 'x', simplified)
            simplified = re.sub(r'\d+\.?\d*', 'x', simplified)

            # Check remaining format
            valid_pattern = r'^[x+\-*/^\s()]+$'
            if not re.match(valid_pattern, simplified):
                return False, "Invalid function format"

            return True, ""

        except Exception as e:
            return False, f"Validation error: {str(e)}"

    @staticmethod
    def evaluate(func_str, x_val):
        """Evaluate function at given x value."""
        # Replace mathematical operations with Python syntax
        expr = func_str.lower().replace('^', '**')

        # Handle special functions
        expr = expr.replace('log10', 'log10').replace('sqrt', 'sqrt')

        # Create safe local environment
        safe_dict = {
            'x': x_val,
            'sqrt': sqrt,
            'log10': log10
        }

        try:
            return eval(expr, {"__builtins__": {}}, safe_dict)
        except Exception as e:
            raise ValueError(f"Error evaluating function: {str(e)}")


class IntersectionTable(QTableWidget):
    """Table widget to display intersection points."""

    def __init__(self):
        super().__init__()
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(['X', 'Y'])
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setVisible(False)

    def update_points(self, points):
        """Update table with new intersection points."""
        self.setRowCount(len(points))
        for i, (x, y) in enumerate(points):
            self.setItem(i, 0, QTableWidgetItem(f"{x:.3f}"))
            self.setItem(i, 1, QTableWidgetItem(f"{y:.3f}"))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Function Solver")
        self.setMinimumSize(1000, 800)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Create input section
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)

        # Function 1 input
        func1_layout = QHBoxLayout()
        func1_layout.addWidget(QLabel("Function 1:"))
        self.func1_input = QLineEdit()
        self.func1_input.setPlaceholderText("Enter first function (e.g., 5*x^2 + 2*x)")
        func1_layout.addWidget(self.func1_input)
        input_layout.addLayout(func1_layout)

        # Function 2 input
        func2_layout = QHBoxLayout()
        func2_layout.addWidget(QLabel("Function 2:"))
        self.func2_input = QLineEdit()
        self.func2_input.setPlaceholderText("Enter second function (e.g., x^2 - 3*x)")
        func2_layout.addWidget(self.func2_input)
        input_layout.addLayout(func2_layout)

        # Solve button
        self.solve_button = QPushButton("Solve and Plot")
        self.solve_button.clicked.connect(self.solve_and_plot)
        input_layout.addWidget(self.solve_button)

        # Error message label
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red")
        input_layout.addWidget(self.error_label)

        layout.addWidget(input_widget)

        # Create splitter for plot and table
        splitter = QSplitter()

        # Create plot widget
        plot_widget = QWidget()
        plot_layout = QVBoxLayout(plot_widget)

        # Create matplotlib figure
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)

        # Add navigation toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)
        plot_layout.addWidget(self.toolbar)
        plot_layout.addWidget(self.canvas)

        # Create intersection points table
        table_widget = QWidget()
        table_layout = QVBoxLayout(table_widget)
        table_layout.addWidget(QLabel("Intersection Points:"))
        self.intersection_table = IntersectionTable()
        table_layout.addWidget(self.intersection_table)

        # Add widgets to splitter
        splitter.addWidget(plot_widget)
        splitter.addWidget(table_widget)
        splitter.setStretchFactor(0, 2)  # Plot takes 2/3 of space
        splitter.setStretchFactor(1, 1)  # Table takes 1/3 of space

        layout.addWidget(splitter)

        self.ax = self.figure.add_subplot(111)

    def solve_and_plot(self):
        """Solve the functions and create the plot."""
        self.error_label.setText("")
        self.ax.clear()

        # Get functions from input
        func1_str = self.func1_input.text().strip()
        func2_str = self.func2_input.text().strip()

        # Validate inputs
        parser = FunctionParser()
        valid1, error1 = parser.validate_function(func1_str)
        valid2, error2 = parser.validate_function(func2_str)

        if not valid1:
            self.error_label.setText(f"Function 1: {error1}")
            return
        if not valid2:
            self.error_label.setText(f"Function 2: {error2}")
            return

        try:
            # Create x values for plotting
            x = np.linspace(-10, 10, 1000)

            # Calculate y values
            y1 = [parser.evaluate(func1_str, xi) for xi in x]
            y2 = [parser.evaluate(func2_str, xi) for xi in x]

            # Find intersection points
            intersections_x = []
            intersections_y = []
            for i in range(len(x) - 1):
                if (y1[i] - y2[i]) * (y1[i + 1] - y2[i + 1]) <= 0:
                    # Linear interpolation to find more precise intersection
                    x_intersect = (x[i] + x[i + 1]) / 2
                    y_intersect = (parser.evaluate(func1_str, x_intersect) +
                                   parser.evaluate(func2_str, x_intersect)) / 2
                    intersections_x.append(x_intersect)
                    intersections_y.append(y_intersect)

            # Plot functions
            self.ax.plot(x, y1, label=f"f1(x) = {func1_str}")
            self.ax.plot(x, y2, label=f"f2(x) = {func2_str}")

            # Plot intersection points and update table
            intersection_points = list(zip(intersections_x, intersections_y))
            self.intersection_table.update_points(intersection_points)

            if intersections_x:
                self.ax.scatter(intersections_x, intersections_y, color='red',
                                zorder=5, label='Intersection Points')
                for x_int, y_int in zip(intersections_x, intersections_y):
                    self.ax.annotate(f'({x_int:.2f}, {y_int:.2f})',
                                     (x_int, y_int), xytext=(5, 5),
                                     textcoords='offset points')

            self.ax.grid(True)
            self.ax.legend()
            self.ax.set_xlabel('x')
            self.ax.set_ylabel('y')
            self.canvas.draw()

        except Exception as e:
            self.error_label.setText(f"Error: {str(e)}")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()