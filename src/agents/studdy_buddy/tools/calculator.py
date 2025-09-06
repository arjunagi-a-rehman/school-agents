import math
import statistics
from typing import List, Union, Dict, Any
import re
from fractions import Fraction
import cmath
from google.adk.tools import BaseTool


class AdvancedCalculator:
    """
    An advanced calculator tool for the Study Buddy agent.
    Provides comprehensive mathematical operations for students.
    """
    
    def __init__(self):
        self.constants = {
            'pi': math.pi,
            'e': math.e,
            'tau': math.tau,
            'phi': (1 + math.sqrt(5)) / 2,  # Golden ratio
        }
    
    # Basic Arithmetic Operations
    def add(self, a: float, b: float) -> float:
        """Add two numbers."""
        return a + b
    
    def subtract(self, a: float, b: float) -> float:
        """Subtract two numbers."""
        return a - b
    
    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers."""
        return a * b
    
    def divide(self, a: float, b: float) -> float:
        """Divide two numbers."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    def power(self, base: float, exponent: float) -> float:
        """Raise base to the power of exponent."""
        return base ** exponent
    
    def modulo(self, a: float, b: float) -> float:
        """Return the remainder of a divided by b."""
        if b == 0:
            raise ValueError("Cannot modulo by zero")
        return a % b
    
    def square_root(self, x: float) -> float:
        """Calculate square root."""
        if x < 0:
            raise ValueError("Cannot calculate square root of negative number")
        return math.sqrt(x)
    
    def nth_root(self, x: float, n: float) -> float:
        """Calculate nth root of x."""
        return x ** (1/n)
    
    # Trigonometric Functions
    def sin(self, x: float, degrees: bool = False) -> float:
        """Calculate sine (input in radians by default)."""
        if degrees:
            x = math.radians(x)
        return math.sin(x)
    
    def cos(self, x: float, degrees: bool = False) -> float:
        """Calculate cosine (input in radians by default)."""
        if degrees:
            x = math.radians(x)
        return math.cos(x)
    
    def tan(self, x: float, degrees: bool = False) -> float:
        """Calculate tangent (input in radians by default)."""
        if degrees:
            x = math.radians(x)
        return math.tan(x)
    
    def asin(self, x: float, degrees: bool = False) -> float:
        """Calculate arcsine."""
        result = math.asin(x)
        return math.degrees(result) if degrees else result
    
    def acos(self, x: float, degrees: bool = False) -> float:
        """Calculate arccosine."""
        result = math.acos(x)
        return math.degrees(result) if degrees else result
    
    def atan(self, x: float, degrees: bool = False) -> float:
        """Calculate arctangent."""
        result = math.atan(x)
        return math.degrees(result) if degrees else result
    
    # Logarithmic Functions
    def log(self, x: float, base: float = math.e) -> float:
        """Calculate logarithm (natural log by default)."""
        if x <= 0:
            raise ValueError("Logarithm undefined for non-positive numbers")
        return math.log(x, base)
    
    def log10(self, x: float) -> float:
        """Calculate base-10 logarithm."""
        if x <= 0:
            raise ValueError("Logarithm undefined for non-positive numbers")
        return math.log10(x)
    
    def log2(self, x: float) -> float:
        """Calculate base-2 logarithm."""
        if x <= 0:
            raise ValueError("Logarithm undefined for non-positive numbers")
        return math.log2(x)
    
    # Statistical Functions
    def mean(self, numbers: List[float]) -> float:
        """Calculate arithmetic mean."""
        if not numbers:
            raise ValueError("Cannot calculate mean of empty list")
        return statistics.mean(numbers)
    
    def median(self, numbers: List[float]) -> float:
        """Calculate median."""
        if not numbers:
            raise ValueError("Cannot calculate median of empty list")
        return statistics.median(numbers)
    
    def mode(self, numbers: List[float]) -> float:
        """Calculate mode."""
        if not numbers:
            raise ValueError("Cannot calculate mode of empty list")
        try:
            return statistics.mode(numbers)
        except statistics.StatisticsError:
            raise ValueError("No unique mode found")
    
    def standard_deviation(self, numbers: List[float], sample: bool = True) -> float:
        """Calculate standard deviation."""
        if len(numbers) < 2:
            raise ValueError("Need at least 2 numbers for standard deviation")
        return statistics.stdev(numbers) if sample else statistics.pstdev(numbers)
    
    def variance(self, numbers: List[float], sample: bool = True) -> float:
        """Calculate variance."""
        if len(numbers) < 2:
            raise ValueError("Need at least 2 numbers for variance")
        return statistics.variance(numbers) if sample else statistics.pvariance(numbers)
    
    # Advanced Mathematical Functions
    def factorial(self, n: int) -> int:
        """Calculate factorial."""
        if n < 0:
            raise ValueError("Factorial undefined for negative numbers")
        return math.factorial(n)
    
    def gcd(self, a: int, b: int) -> int:
        """Calculate greatest common divisor."""
        return math.gcd(a, b)
    
    def lcm(self, a: int, b: int) -> int:
        """Calculate least common multiple."""
        return abs(a * b) // math.gcd(a, b)
    
    def is_prime(self, n: int) -> bool:
        """Check if a number is prime."""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    # Conversion Functions
    def celsius_to_fahrenheit(self, celsius: float) -> float:
        """Convert Celsius to Fahrenheit."""
        return (celsius * 9/5) + 32
    
    def fahrenheit_to_celsius(self, fahrenheit: float) -> float:
        """Convert Fahrenheit to Celsius."""
        return (fahrenheit - 32) * 5/9
    
    def degrees_to_radians(self, degrees: float) -> float:
        """Convert degrees to radians."""
        return math.radians(degrees)
    
    def radians_to_degrees(self, radians: float) -> float:
        """Convert radians to degrees."""
        return math.degrees(radians)
    
    def decimal_to_binary(self, decimal: int) -> str:
        """Convert decimal to binary."""
        return bin(decimal)[2:]
    
    def binary_to_decimal(self, binary: str) -> int:
        """Convert binary to decimal."""
        return int(binary, 2)
    
    def decimal_to_hex(self, decimal: int) -> str:
        """Convert decimal to hexadecimal."""
        return hex(decimal)[2:].upper()
    
    def hex_to_decimal(self, hex_str: str) -> int:
        """Convert hexadecimal to decimal."""
        return int(hex_str, 16)
    
    # Geometry Functions
    def circle_area(self, radius: float) -> float:
        """Calculate area of a circle."""
        return math.pi * radius ** 2
    
    def circle_circumference(self, radius: float) -> float:
        """Calculate circumference of a circle."""
        return 2 * math.pi * radius
    
    def triangle_area(self, base: float, height: float) -> float:
        """Calculate area of a triangle."""
        return 0.5 * base * height
    
    def rectangle_area(self, length: float, width: float) -> float:
        """Calculate area of a rectangle."""
        return length * width
    
    def sphere_volume(self, radius: float) -> float:
        """Calculate volume of a sphere."""
        return (4/3) * math.pi * radius ** 3
    
    def cylinder_volume(self, radius: float, height: float) -> float:
        """Calculate volume of a cylinder."""
        return math.pi * radius ** 2 * height
    
    # Financial Functions
    def simple_interest(self, principal: float, rate: float, time: float) -> float:
        """Calculate simple interest."""
        return principal * rate * time / 100
    
    def compound_interest(self, principal: float, rate: float, time: float, 
                         compounds_per_year: int = 1) -> float:
        """Calculate compound interest."""
        amount = principal * (1 + rate/100/compounds_per_year) ** (compounds_per_year * time)
        return amount - principal
    
    def percentage(self, part: float, whole: float) -> float:
        """Calculate what percentage part is of whole."""
        if whole == 0:
            raise ValueError("Cannot calculate percentage with zero denominator")
        return (part / whole) * 100
    
    def percentage_change(self, old_value: float, new_value: float) -> float:
        """Calculate percentage change."""
        if old_value == 0:
            raise ValueError("Cannot calculate percentage change from zero")
        return ((new_value - old_value) / old_value) * 100
    
    # Expression Evaluator
    def evaluate_expression(self, expression: str) -> float:
        """
        Safely evaluate mathematical expressions.
        Supports basic operations, functions, and constants.
        """
        # Replace common mathematical constants
        expression = expression.replace('pi', str(math.pi))
        expression = expression.replace('e', str(math.e))
        
        # Convert common mathematical notation to Python syntax
        expression = expression.replace('^', '**')  # Convert ^ to ** for exponentiation
        expression = expression.replace('[', '(')   # Convert [ to ( for grouping
        expression = expression.replace(']', ')')   # Convert ] to ) for grouping
        
        # Replace functions with math module equivalents
        expression = re.sub(r'\bsin\(', 'math.sin(', expression)
        expression = re.sub(r'\bcos\(', 'math.cos(', expression)
        expression = re.sub(r'\btan\(', 'math.tan(', expression)
        expression = re.sub(r'\bsqrt\(', 'math.sqrt(', expression)
        expression = re.sub(r'\blog\(', 'math.log(', expression)
        expression = re.sub(r'\babs\(', 'abs(', expression)
        
        # Safety check - only allow safe operations 
        # Note: [] and ^ are converted above, so they should be () and ** by now
        allowed_chars = set('0123456789+-*/().,abcdefghijklmnopqrstuvwxyz_')
        if not all(c.lower() in allowed_chars or c.isspace() for c in expression):
            raise ValueError(f"Expression contains invalid characters: '{expression}'")
        
        try:
            # Use eval with restricted globals for safety
            safe_dict = {
                "math": math,
                "__builtins__": {},
                "abs": abs,
                "round": round,
                "min": min,
                "max": max,
            }
            result = eval(expression, safe_dict)
            return float(result)
        except Exception as e:
            raise ValueError(f"Invalid expression: {str(e)}")
    
    # Complex Number Operations
    def complex_add(self, z1: complex, z2: complex) -> complex:
        """Add two complex numbers."""
        return z1 + z2
    
    def complex_multiply(self, z1: complex, z2: complex) -> complex:
        """Multiply two complex numbers."""
        return z1 * z2
    
    def complex_magnitude(self, z: complex) -> float:
        """Calculate magnitude of complex number."""
        return abs(z)
    
    def complex_phase(self, z: complex, degrees: bool = False) -> float:
        """Calculate phase of complex number."""
        result = cmath.phase(z)
        return math.degrees(result) if degrees else result
    
    # Matrix Operations (for 2x2 matrices represented as lists)
    def matrix_determinant_2x2(self, matrix: List[List[float]]) -> float:
        """Calculate determinant of 2x2 matrix."""
        if len(matrix) != 2 or len(matrix[0]) != 2 or len(matrix[1]) != 2:
            raise ValueError("Matrix must be 2x2")
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    def matrix_add_2x2(self, m1: List[List[float]], m2: List[List[float]]) -> List[List[float]]:
        """Add two 2x2 matrices."""
        if len(m1) != 2 or len(m2) != 2:
            raise ValueError("Matrices must be 2x2")
        result = [[0, 0], [0, 0]]
        for i in range(2):
            for j in range(2):
                result[i][j] = m1[i][j] + m2[i][j]
        return result
    
    # Utility Functions
    def round_to_decimals(self, number: float, decimals: int) -> float:
        """Round number to specified decimal places."""
        return round(number, decimals)
    
    def format_result(self, result: Union[float, int, complex], decimals: int = 4) -> str:
        """Format result for display."""
        if isinstance(result, complex):
            if result.imag == 0:
                return f"{result.real:.{decimals}f}"
            elif result.real == 0:
                return f"{result.imag:.{decimals}f}i"
            else:
                sign = "+" if result.imag >= 0 else "-"
                return f"{result.real:.{decimals}f} {sign} {abs(result.imag):.{decimals}f}i"
        elif isinstance(result, float):
            if result.is_integer():
                return str(int(result))
            return f"{result:.{decimals}f}"
        else:
            return str(result)
    
    # Calculus Approximations (simple numerical methods)
    def derivative_approximation(self, func_str: str, x: float, h: float = 1e-7) -> float:
        """
        Approximate derivative using finite differences.
        func_str should be a simple function like 'x**2' or 'sin(x)'
        """
        def evaluate_at(val):
            expression = func_str.replace('x', str(val))
            return self.evaluate_expression(expression)
        
        return (evaluate_at(x + h) - evaluate_at(x - h)) / (2 * h)
    
    def integral_approximation(self, func_str: str, a: float, b: float, n: int = 1000) -> float:
        """
        Approximate definite integral using trapezoidal rule.
        func_str should be a simple function like 'x**2' or 'sin(x)'
        """
        def evaluate_at(val):
            expression = func_str.replace('x', str(val))
            return self.evaluate_expression(expression)
        
        h = (b - a) / n
        result = (evaluate_at(a) + evaluate_at(b)) / 2
        
        for i in range(1, n):
            x = a + i * h
            result += evaluate_at(x)
        
        return result * h
    
    # Equation Solving (simple cases)
    def solve_quadratic(self, a: float, b: float, c: float) -> Dict[str, Any]:
        """
        Solve quadratic equation ax² + bx + c = 0
        Returns dictionary with solutions and discriminant info.
        """
        if a == 0:
            if b == 0:
                return {"type": "no_solution" if c != 0 else "infinite_solutions"}
            return {"type": "linear", "solution": -c/b}
        
        discriminant = b**2 - 4*a*c
        
        if discriminant > 0:
            x1 = (-b + math.sqrt(discriminant)) / (2*a)
            x2 = (-b - math.sqrt(discriminant)) / (2*a)
            return {
                "type": "two_real_solutions",
                "solutions": [x1, x2],
                "discriminant": discriminant
            }
        elif discriminant == 0:
            x = -b / (2*a)
            return {
                "type": "one_real_solution",
                "solution": x,
                "discriminant": discriminant
            }
        else:
            real_part = -b / (2*a)
            imaginary_part = math.sqrt(-discriminant) / (2*a)
            return {
                "type": "complex_solutions",
                "solutions": [
                    complex(real_part, imaginary_part),
                    complex(real_part, -imaginary_part)
                ],
                "discriminant": discriminant
            }
    
    # Number Theory Functions
    def prime_factors(self, n: int) -> List[int]:
        """Find prime factors of a number."""
        if n <= 1:
            return []
        
        factors = []
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors.append(d)
                n //= d
            d += 1
        if n > 1:
            factors.append(n)
        return factors
    
    def fibonacci(self, n: int) -> int:
        """Calculate nth Fibonacci number."""
        if n < 0:
            raise ValueError("Fibonacci sequence undefined for negative numbers")
        if n <= 1:
            return n
        
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
    
    # Unit Conversions
    def convert_length(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert between length units."""
        # Convert to meters first
        to_meters = {
            'mm': 0.001, 'cm': 0.01, 'm': 1, 'km': 1000,
            'in': 0.0254, 'ft': 0.3048, 'yd': 0.9144, 'mi': 1609.34
        }
        
        if from_unit not in to_meters or to_unit not in to_meters:
            raise ValueError("Unsupported unit")
        
        meters = value * to_meters[from_unit]
        return meters / to_meters[to_unit]
    
    def convert_weight(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert between weight units."""
        # Convert to grams first
        to_grams = {
            'mg': 0.001, 'g': 1, 'kg': 1000,
            'oz': 28.3495, 'lb': 453.592
        }
        
        if from_unit not in to_grams or to_unit not in to_grams:
            raise ValueError("Unsupported unit")
        
        grams = value * to_grams[from_unit]
        return grams / to_grams[to_unit]
    
    # Fraction Operations
    def add_fractions(self, frac1: str, frac2: str) -> str:
        """Add two fractions given as strings like '1/2'."""
        f1 = Fraction(frac1)
        f2 = Fraction(frac2)
        result = f1 + f2
        return str(result)
    
    def multiply_fractions(self, frac1: str, frac2: str) -> str:
        """Multiply two fractions given as strings like '1/2'."""
        f1 = Fraction(frac1)
        f2 = Fraction(frac2)
        result = f1 * f2
        return str(result)
    
    def simplify_fraction(self, numerator: int, denominator: int) -> str:
        """Simplify a fraction."""
        if denominator == 0:
            raise ValueError("Denominator cannot be zero")
        frac = Fraction(numerator, denominator)
        return str(frac)


# Create a global instance for easy access
calculator = AdvancedCalculator()


# Helper functions for common operations
def calculate(expression: str) -> str:
    """
    Main calculation function that can handle various types of mathematical expressions.
    This is the primary interface for the agent to use.
    """
    try:
        result = calculator.evaluate_expression(expression)
        return calculator.format_result(result)
    except Exception as e:
        return f"Error: {str(e)}"


def get_calculator_help() -> str:
    """Return help text for calculator functions."""
    return """
Available Calculator Functions:
- Basic: +, -, *, /, %, ** (power), sqrt()
- Trigonometric: sin(), cos(), tan(), asin(), acos(), atan()
- Logarithmic: log(), log10(), log2()
- Statistical: mean, median, mode, standard deviation
- Advanced: factorial, prime check, GCD, LCM
- Conversions: temperature, length, weight, number bases
- Geometry: area and volume calculations
- Financial: simple/compound interest, percentages

Examples:
- Basic: "2 + 3 * 4"
- Trigonometric: "sin(pi/2)" or "cos(45)" (degrees)
- Complex: "sqrt(16) + log(e)"
"""


class CalculatorTool(BaseTool):
    """Calculator tool that integrates with Google ADK agents."""
    
    def __init__(self):
        super().__init__(
            name="calculator",
            description="Advanced mathematical calculator for performing calculations including arithmetic, trigonometry, statistics, geometry, algebra, and more."
        )
        self.calc = AdvancedCalculator()
    
    def call(self, expression: str) -> str:
        """Execute a mathematical calculation."""
        try:
            # Log the input for debugging
            print(f"Calculator tool called with: {expression}")
            result = self.calc.evaluate_expression(expression)
            formatted_result = self.calc.format_result(result)
            print(f"Calculator result: {formatted_result}")
            return formatted_result
        except Exception as e:
            error_msg = f"Calculator error with '{expression}': {str(e)}"
            print(error_msg)
            return error_msg


class CalculatorHelpTool(BaseTool):
    """Tool to provide calculator help information."""
    
    def __init__(self):
        super().__init__(
            name="calculator_help",
            description="Get help and examples for using the calculator tool."
        )
    
    def call(self) -> str:
        """Return help information for the calculator."""
        return get_calculator_help()


# Create tool instances for easy import
calculator_tool = CalculatorTool()
calculator_help_tool = CalculatorHelpTool()


if __name__ == "__main__":
    # Test the calculator
    calc = AdvancedCalculator()
    print("Calculator Test:")
    print(f"2 + 3 = {calc.add(2, 3)}")
    print(f"sqrt(16) = {calc.square_root(16)}")
    print(f"sin(pi/2) = {calc.sin(math.pi/2)}")
    print(f"Quadratic 1x² + 0x - 4 = 0: {calc.solve_quadratic(1, 0, -4)}")
