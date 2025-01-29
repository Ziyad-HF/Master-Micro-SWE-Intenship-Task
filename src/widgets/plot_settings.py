from PySide2.QtWidgets import (QWidget, QLabel, QGridLayout, QDoubleSpinBox, QSpinBox)


class PlotSettings(QWidget):
    """Widget for plot settings controls."""

    def __init__(self):
        super().__init__()
        layout = QGridLayout()

        # Domain range controls
        layout.addWidget(QLabel("Domain:"), 0, 0)
        layout.addWidget(QLabel("Start:"), 0, 1)
        self.domain_start = QDoubleSpinBox()
        self.domain_start.setRange(-1000, 1000)
        self.domain_start.setValue(-10)
        self.domain_start.setDecimals(2)
        layout.addWidget(self.domain_start, 0, 2)

        layout.addWidget(QLabel("End:"), 0, 3)
        self.domain_end = QDoubleSpinBox()
        self.domain_end.setRange(-1000, 1000)
        self.domain_end.setValue(10)
        self.domain_end.setDecimals(2)
        layout.addWidget(self.domain_end, 0, 4)

        # Number of points control
        layout.addWidget(QLabel("Number of Points:"), 1, 0)
        self.num_points = QSpinBox()
        self.num_points.setRange(100, 10000)
        self.num_points.setValue(1000)
        self.num_points.setSingleStep(100)
        layout.addWidget(self.num_points, 1, 1, 1, 2)

        # Decimal precision control
        layout.addWidget(QLabel("Decimal Precision:"), 1, 3)
        self.precision = QSpinBox()
        self.precision.setRange(0, 10)
        self.precision.setValue(2)
        layout.addWidget(self.precision, 1, 4)

        self.setLayout(layout)
