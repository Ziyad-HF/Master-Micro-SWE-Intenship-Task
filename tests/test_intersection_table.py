import pytest
from PySide2.QtWidgets import QApplication
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from widgets.intersection_table import IntersectionTable

def test_intersection_table_creation(qapp):
    table = IntersectionTable()
    assert table.columnCount() == 3
    assert table.horizontalHeader().count() == 3

def test_update_intersections(qapp):
    table = IntersectionTable()
    points = [(1.0, 1.0), (2.0, 4.0)]
    intervals = [((3.0, 9.0), (4.0, 16.0))]
    precision = 2
    
    table.update_intersections(points, intervals, precision)
    
    assert table.rowCount() == 3
    assert table.item(0, 0).text() == "Point"
    assert table.item(0, 1).text() == "(1.00, 1.00)"
    assert table.item(2, 0).text() == "Interval"
    assert table.item(2, 1).text() == "(3.00, 9.00)"
    assert table.item(2, 2).text() == "(4.00, 16.00)"
