import pytest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from widgets.plot_settings import PlotSettings

def test_plot_settings_default_values(qapp):
    settings = PlotSettings()
    
    assert settings.domain_start.value() == -10
    assert settings.domain_end.value() == 10
    assert settings.num_points.value() == 1000
    assert settings.precision.value() == 2

def test_plot_settings_ranges(qapp):
    settings = PlotSettings()
    
    assert settings.domain_start.minimum() == -1000
    assert settings.domain_start.maximum() == 1000
    assert settings.num_points.minimum() == 100
    assert settings.num_points.maximum() == 10000
    assert settings.precision.minimum() == 0
    assert settings.precision.maximum() == 10