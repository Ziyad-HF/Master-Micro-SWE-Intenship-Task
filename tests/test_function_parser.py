import pytest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from function_parser import FunctionParser

def test_validate_function_valid_inputs():
    parser = FunctionParser()
    valid_functions = [
        "x + 1",
        "5*x^2",
        "log10(x)",
        "sqrt(x)",
        "2*x + 3*x^2",
        "log10(x^2 + 1)",
        "sqrt(x^2 + 4)"
    ]
    
    for func in valid_functions:
        is_valid, error = parser.validate_function(func)
        assert is_valid
        assert error == ""

def test_validate_function_invalid_inputs():
    parser = FunctionParser()
    invalid_functions = [
        ("sin(x)", "Invalid characters detected"),
        ("x + )", "Unbalanced parentheses"),
        ("x + $", "Invalid characters detected"),
        ("", "Invalid function format")
    ]
    
    for func, expected_error in invalid_functions:
        is_valid, error = parser.validate_function(func)
        assert not is_valid
        assert expected_error in error

def test_check_domain_restrictions():
    parser = FunctionParser()
    
    # Test sqrt domain restrictions
    is_valid, restriction = parser.check_domain_restrictions("sqrt(x)", -1)
    assert not is_valid
    assert restriction == "sqrt"
    
    is_valid, restriction = parser.check_domain_restrictions("sqrt(x)", 1)
    assert is_valid
    assert restriction is None
    
    # Test log domain restrictions
    is_valid, restriction = parser.check_domain_restrictions("log10(x)", 0)
    assert not is_valid
    assert restriction == "log"
    
    is_valid, restriction = parser.check_domain_restrictions("log10(x)", 1)
    assert is_valid
    assert restriction is None

def test_evaluate_function():
    parser = FunctionParser()
    test_cases = [
        ("x + 1", 2, 3),
        ("x^2", 3, 9),
        ("2*x + 3", 4, 11),
        ("log10(100)", 0, 2),
        ("sqrt(16)", 0, 4)
    ]
    
    for func, x_val, expected in test_cases:
        result = parser.evaluate(func, x_val)
        assert abs(result - expected) < 1e-10

def test_evaluate_invalid_function():
    parser = FunctionParser()
    with pytest.raises(ValueError):
        parser.evaluate("invalid", 1)