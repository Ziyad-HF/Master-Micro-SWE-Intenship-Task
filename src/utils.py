from PySide2.QtWidgets import QMessageBox
from PySide2.QtCore import QFile
import numpy as np


def show_domain_restriction_dialog(restriction_type):
    """Show dialog for domain restriction handling."""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Question)

    if restriction_type == 'sqrt':
        msg.setText("The function contains square root of negative values.")
    else:  # log
        msg.setText("The function contains logarithm of non-positive values.")

    msg.setInformativeText("Do you want to plot only the valid domain?")
    msg.setWindowTitle("Domain Restriction")
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

    return msg.exec_() == QMessageBox.Yes


def evaluate_function(parser, func_str, x_val):
    """Evaluate function with domain checking."""
    is_valid, restriction = parser.check_domain_restrictions(func_str, x_val)
    if not is_valid:
        return None
    try:
        return parser.evaluate(func_str, x_val)
    except:
        return None


def find_intersections(x_array, y1_array, y2_array, tolerance=1e-6):
    """Find both point intersections and intersection intervals."""
    points = []
    intervals = []

    i = 0
    while i < len(x_array) - 1:
        if np.isnan(y1_array[i]) or np.isnan(y2_array[i]):
            i += 1
            continue

        diff = abs(y1_array[i] - y2_array[i])

        if diff <= tolerance:
            # Found potential interval start
            start_x = x_array[i]
            start_y = y1_array[i]

            # Look for interval end
            j = i + 1
            while (j < len(x_array) and
                   not np.isnan(y1_array[j]) and
                   not np.isnan(y2_array[j]) and
                   abs(y1_array[j] - y2_array[j]) <= tolerance):
                j += 1

            if j - i > 2:  # Consider it an interval if more than 2 points
                end_x = x_array[j - 1]
                end_y = y1_array[j - 1]
                intervals.append(((start_x, start_y), (end_x, end_y)))
                i = j
            else:
                # Single point intersection
                points.append((x_array[i], y1_array[i]))
                i += 1
        else:
            # Check for zero crossing
            if (i < len(x_array) - 1 and
                    not np.isnan(y1_array[i + 1]) and
                    not np.isnan(y2_array[i + 1])):
                if (y1_array[i] - y2_array[i]) * (y1_array[i + 1] - y2_array[i + 1]) < 0:
                    # Linear interpolation
                    x_int = (x_array[i] + x_array[i + 1]) / 2
                    y_int = (y1_array[i] + y2_array[i]) / 2
                    points.append((x_int, y_int))
            i += 1

    return points, intervals


def load_stylesheet(file_path):
    """Load QSS stylesheet from file."""
    file_path = file_path.replace('/', '\\')
    qss_file = QFile(file_path)
    if qss_file.exists():
        qss_file.open(QFile.ReadOnly)
        stylesheet = str(qss_file.readAll(), encoding='utf-8')
        return stylesheet
    return ""
