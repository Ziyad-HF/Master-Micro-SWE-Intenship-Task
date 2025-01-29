# Master-Micro-SWE-Internship-Task

# Mathematical Function Solver and Plotter

A Python GUI application that allows users to input, solve, and visualize mathematical functions. The application is built using PySide2 for the GUI interface and Matplotlib for function plotting.

![Function Solver Demo](path_to_gif)

## Features

### Core Functionality
- Input and plot two mathematical functions simultaneously
- Interactive plot with zoom, pan, and save capabilities
- Automatic detection and visualization of intersections
- Domain restriction handling for special functions
- Clear error messages for invalid inputs

### Supported Operations
- Basic arithmetic: `+`, `-`, `*`, `/`
- Power operation: `^`
- Special functions: 
  - `sqrt()` - Square root
  - `log10()` - Base-10 logarithm

### Intersection Detection
- Detects single point intersections
- Identifies continuous intersection intervals
- Displays intersection data in an organized table
- Different visualization for points vs. intervals:
  - Points: Black dots with coordinates
  - Intervals: Green highlighted regions

### Plot Navigation
- Zoom in/out functionality
- Pan/Move the plot
- Reset view option
- Save plot as image
- Dynamic axis scaling

### Domain Handling
- Automatic detection of invalid domains (e.g., negative values in sqrt)
- User prompt for domain restriction handling
- Option to plot only valid domains
- Clear visualization of function discontinuities

### User Interface
- Clean and intuitive design
- Split view with plot and intersection table
- Adjustable panel sizes
- Informative error messages
- Function input validation
- Responsive layout

## Usage

1. **Enter Functions**
   - Type your functions in the input fields
   - Use supported operators and functions
   - Example: `5*x^2 + 2*x`, `sqrt(x)`, `log10(x)`

2. **Plot and Analyze**
   - Click "Solve and Plot" button
   - View the graphical representation
   - Check intersection points/intervals in the table

3. **Navigate Plot**
   - Use toolbar buttons for zoom/pan
   - Reset view as needed
   - Save plot images for later use

4. **Handle Domain Restrictions**
   - Respond to domain validation prompts
   - Choose to plot valid domains only
   - View clear visual representation of valid regions

## Implementation Details

### Technologies Used
- **PySide2**: GUI framework
- **Matplotlib**: Plotting library
- **NumPy**: Numerical computations
- **Python**: Core programming language

### Code Organization
- Modular design with separate classes for:
  - Function parsing and evaluation
  - Intersection detection
  - GUI components
  - Plot management

### Testing
- Comprehensive test suite using pytest
- End-to-end testing of main features
- Input validation tests
- Function evaluation tests
- Intersection detection tests

## Examples

### Basic Functions
```python
f1(x) = 2*x + 1
f2(x) = x^2
```

### Special Functions
```python
f1(x) = sqrt(x^2 - 4)
f2(x) = log10(x)
```

### Complex Examples
```python
f1(x) = 5*x^3 + 2*x
f2(x) = sqrt(x^2 + 1) + log10(x+10)
```