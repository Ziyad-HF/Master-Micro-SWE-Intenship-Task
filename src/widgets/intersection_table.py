from PySide2.QtWidgets import QTableWidget, QTableWidgetItem


class IntersectionTable(QTableWidget):
    """Table widget to display intersection points and intervals."""

    def __init__(self):
        super().__init__()
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(['Type', 'Start (x, y)', 'End (x, y)'])
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setVisible(False)

    def update_intersections(self, points, intervals, precision):
        """Update table with intersection points and intervals."""
        total_rows = len(points) + len(intervals)
        self.setRowCount(total_rows)
        format_str = f"{{:.{precision}f}}"

        row = 0
        # Add points
        for x, y in points:
            self.setItem(row, 0, QTableWidgetItem("Point"))
            self.setItem(row, 1, QTableWidgetItem(
                f"({format_str.format(x)}, {format_str.format(y)})")
                         )
            self.setItem(row, 2, QTableWidgetItem("-"))
            row += 1

        # Add intervals
        for start, end in intervals:
            self.setItem(row, 0, QTableWidgetItem("Interval"))
            self.setItem(row, 1, QTableWidgetItem(
                f"({format_str.format(start[0])}, {format_str.format(start[1])})")
                         )
            self.setItem(row, 2, QTableWidgetItem(
                f"({format_str.format(end[0])}, {format_str.format(end[1])})")
                         )
            row += 1
