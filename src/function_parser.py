import re
from math import sqrt, log10


class FunctionParser:
    """Parse and evaluate mathematical functions."""

    @staticmethod
    def validate_function(func_str):
        """
        Validate function string format.
        Returns (bool, str) tuple - (is_valid, error_message)
        """
        # Check for invalid characters
        allowed = set('x0123456789+-*/^().log sqrt')
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
    def check_domain_restrictions(func_str, x_val):
        """
        Check domain restrictions for sqrt and log10.
        Returns (bool, str) tuple - (is_valid, restriction_type)
        """
        expr = func_str.lower()

        # Extract arguments of sqrt and log10 functions
        sqrt_matches = re.finditer(r'sqrt\(([^)]+)\)', expr)
        log_matches = re.finditer(r'log10\(([^)]+)\)', expr)

        # Check sqrt arguments
        for match in sqrt_matches:
            arg = match.group(1)
            try:
                value = eval(arg.replace('x', str(x_val)), {"__builtins__": {}}, {'sqrt': sqrt, 'log10': log10})
                if value < 0:
                    return False, 'sqrt'
            except:
                continue

        # Check log10 arguments
        for match in log_matches:
            arg = match.group(1)
            try:
                value = eval(arg.replace('x', str(x_val)), {"__builtins__": {}}, {'sqrt': sqrt, 'log10': log10})
                if value <= 0:
                    return False, 'log'
            except:
                continue

        return True, None

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
