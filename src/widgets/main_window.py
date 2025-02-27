from PySide2.QtWidgets import (QSplitter, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLineEdit, QPushButton, QLabel, QApplication)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from widgets.intersection_table import IntersectionTable
from widgets.plot_settings import PlotSettings
from function_parser import FunctionParser
from utils import show_domain_restriction_dialog, evaluate_function, find_intersections


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("mainWindow")
        self.setWindowTitle("Function Solver")
        self.setMinimumSize(1000, 800)

        # Create main widget and layout
        main_widget = QWidget()
        main_widget.setObjectName("mainWidget")
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Create input section
        input_widget = QWidget()
        input_widget.setObjectName("inputWidget")
        input_layout = QVBoxLayout(input_widget)

        # Function 1 input
        func1_layout = QHBoxLayout()
        func1_label = QLabel("Function 1:")
        func1_label.setObjectName("functionLabel")
        func1_layout.addWidget(func1_label)
        self.func1_input = QLineEdit()
        self.func1_input.setObjectName("functionInput")
        self.func1_input.setPlaceholderText("Enter first function (e.g., 5*x^2 + 2*x)")
        func1_layout.addWidget(self.func1_input)
        input_layout.addLayout(func1_layout)

        # Function 2 input
        func2_layout = QHBoxLayout()
        func2_label = QLabel("Function 2:")
        func2_label.setObjectName("functionLabel")
        func2_layout.addWidget(func2_label)
        self.func2_input = QLineEdit()
        self.func2_input.setObjectName("functionInput")
        self.func2_input.setPlaceholderText("Enter second function (e.g., x^2 - 3*x)")
        func2_layout.addWidget(self.func2_input)
        input_layout.addLayout(func2_layout)

        # plot settings
        self.plot_settings = PlotSettings()
        input_layout.addWidget(self.plot_settings)

        # Solve button
        self.solve_button = QPushButton("Solve and Plot")
        self.solve_button.setObjectName("solveButton")
        self.solve_button.clicked.connect(self.solve_and_plot)
        input_layout.addWidget(self.solve_button)

        # Error message label
        self.error_label = QLabel()
        self.error_label.setObjectName("errorLabel")
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
        table_layout.addWidget(QLabel("Intersections:"))
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

        # Get plot settings
        domain_start = self.plot_settings.domain_start.value()
        domain_end = self.plot_settings.domain_end.value()
        num_points = self.plot_settings.num_points.value()
        precision = self.plot_settings.precision.value()

        # Check if both functions are provided
        if not func1_str or not func2_str:
            self.error_label.setText("Please enter both functions")
            return

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
            x = np.linspace(domain_start, domain_end, num_points)

            # Check for domain restrictions
            domain_restricted = False
            plot_valid_domain = True
            for xi in x:
                is_valid1, restriction1 = parser.check_domain_restrictions(func1_str, xi)
                is_valid2, restriction2 = parser.check_domain_restrictions(func2_str, xi)

                if (not is_valid1 and restriction1) or (not is_valid2 and restriction2):
                    domain_restricted = True
                    restriction_type = restriction1 if not is_valid1 else restriction2
                    plot_valid_domain = show_domain_restriction_dialog(restriction_type)
                    break

            # Calculate y values with domain handling
            y1 = []
            y2 = []
            valid_x = []

            for xi in x:
                val1 = evaluate_function(parser, func1_str, xi)
                val2 = evaluate_function(parser, func2_str, xi)

                if plot_valid_domain if domain_restricted else True:
                    if val1 is not None and val2 is not None:
                        valid_x.append(xi)
                        y1.append(val1)
                        y2.append(val2)
                else:
                    y1.append(val1 if val1 is not None else np.nan)
                    y2.append(val2 if val2 is not None else np.nan)

            # Plot functions
            if domain_restricted and plot_valid_domain:
                plot_x = valid_x
                plot_y1 = y1
                plot_y2 = y2
            else:
                plot_x = x
                plot_y1 = y1
                plot_y2 = y2

            # Find intersections
            points, intervals = find_intersections(
                np.array(plot_x),
                np.array(plot_y1),
                np.array(plot_y2)
            )

            # Round intersection points and intervals based on precision
            points = [(round(x, precision), round(y, precision)) for x, y in points]
            intervals = [((round(sx, precision), round(sy, precision)),
                          (round(ex, precision), round(ey, precision)))
                         for (sx, sy), (ex, ey) in intervals]

            # Update intersection table
            self.intersection_table.update_intersections(points, intervals, precision)

            # Format for annotations
            format_str = f"{{:.{precision}f}}"

            # Plot regular parts of functions
            self.ax.plot(plot_x, plot_y1, label=f"f1(x) = {func1_str}", color='blue')
            self.ax.plot(plot_x, plot_y2, label=f"f2(x) = {func2_str}", color='red')

            # Plot intersection points and intervals
            if points:
                x_points, y_points = zip(*points)
                self.ax.scatter(x_points, y_points, color='black',
                                zorder=5, label='Intersection Points')
                for x_int, y_int in points:
                    self.ax.annotate(f'({format_str.format(x_int)}, {format_str.format(y_int)})',
                                     (x_int, y_int), xytext=(5, 5),
                                     textcoords='offset points'
                                     )

            # Highlight intersection intervals
            for (start_x, start_y), (end_x, end_y) in intervals:
                # Create x values for the interval
                interval_x = np.linspace(start_x, end_x, 100)
                # Calculate y values using one of the functions
                interval_y = [evaluate_function(parser, func1_str, xi) for xi in interval_x]
                # Plot the interval in green
                self.ax.plot(interval_x, interval_y, color='green', linewidth=2,
                             label='Intersection Interval' if interval_x[0] == intervals[0][0][0] else "")

            self.ax.grid(True)
            self.ax.legend()
            self.ax.set_xlabel('x')
            self.ax.set_ylabel('y')
            self.canvas.draw()

        except Exception as e:
            self.error_label.setText(f"Error: {str(e)}")
