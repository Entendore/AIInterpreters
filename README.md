# Programming Language Interpreter

A complete, modular interpreter for a custom programming language with support for variables, functions, closures, recursion, complex numbers, and matrices.

## Features

- **Variables & Types**: `int`, `float`, `string`, `bool`, `complex`, `matrix`, `var` (type inference)
- **Functions**: Named functions with parameters and return values
- **Closures**: Anonymous functions (lambdas) with optional names for recursion
- **Recursion Keywords**: `rec`, `recurse`, `r` for explicit recursive definitions
- **Complex Numbers**: Native support with `real+imag i` syntax
- **Matrices**: 2D arrays with nested brace notation
- **Operators**: Full set of arithmetic, comparison, and logical operators
- **Control Flow**: `if` statements with optional `else` blocks
- **Built-in Functions**: Mathematical and utility functions

## Installation

```bash
# Clone or download the repository
git clone https://github.com/user/lang-interpreter.git
cd lang-interpreter

# Install in development mode
pip install -e .

# Or just run directly
python main.py
```

## Quick Start

### Interactive REPL

```bash
python main.py
```

```
>>> int x = 10
>>> print(x * 5)
50
>>> var square = function(n) { return n * n }
>>> square(7)
49
>>> exit
```

### Run a File

```bash
python main.py examples/basic/09_comprehensive.lang
```

## Project Structure

```
lang-interpreter/
├── lang/                          # Main package
│   ├── __init__.py               # Package exports
│   ├── errors.py                 # Exception definitions
│   ├── repl.py                   # Interactive REPL
│   │
│   ├── lexer/                    # Lexical analysis
│   │   ├── __init__.py
│   │   ├── tokens.py             # Token definitions
│   │   └── lexer.py              # Tokenizer implementation
│   │
│   ├── parser/                   # Syntax analysis
│   │   ├── __init__.py
│   │   ├── ast_nodes.py          # AST node definitions
│   │   └── parser.py             # Recursive descent parser
│   │
│   └── interpreter/              # Execution
│       ├── __init__.py
│       ├── environment.py        # Variable scoping
│       ├── builtins.py           # Built-in functions
│       ├── types.py              # Complex, Matrix types
│       └── interpreter.py        # AST interpreter
│
├── tests/                        # Test suite
│   ├── __init__.py
│   └── test_interpreter.py       # Unit and integration tests
│
├── examples/                     # Example programs
│   ├── basic/                    # Basic examples
│   ├── functions/                # Function examples
│   └── advanced/                 # Advanced examples
│
├── main.py                       # Entry point
├── pyproject.toml               # Package configuration
└── README.md                    # This file
```

## Language Syntax

### Comments

```javascript
// Single-line comment
/* Multi-line
   comment */
```

### Variables

```javascript
int count = 100
float pi = 3.14159
string name = "Alice"
bool active = true
complex z = 1.0+2.0i
matrix m = {{1, 2}, {3, 4}}
var inferred = 42      // Type inference
```

### Functions

```javascript
// Named function
function add(a, b) {
    return a + b
}

// Function call
int result = add(5, 3)
```

### Closures

```javascript
// Anonymous closure
var square = function(x) {
    return x * x
}

// Named closure (recursive)
var factorial = function fact(n) {
    if (n <= 1) { return 1 }
    return n * fact(n - 1)
}
```

### Recursion Keywords

```javascript
// Using 'rec'
var fib = rec(n) => int {
    if (n <= 1) { return n }
    return fib(n - 1) + fib(n - 2)
}

// Using 'recurse'
var sumTo = recurse(n) => int {
    if (n == 0) { return 0 }
    return n + sumTo(n - 1)
}

// Using 'r' (short form)
var powerOfTwo = r(n) => int {
    if (n == 0) { return 1 }
    return 2 * powerOfTwo(n - 1)
}
```

### Operators

```javascript
// Arithmetic
int sum = 10 + 5       // 15
int diff = 20 - 8      // 12
int prod = 6 * 7       // 42
int quot = 100 / 4     // 25.0

// Comparison
bool eq = (10 == 10)   // true
bool ne = (5 != 3)     // true
bool lt = (3 < 5)      // true
bool gt = (7 > 2)      // true
bool le = (5 <= 5)     // true
bool ge = (5 >= 5)     // true

// Logical
bool and = true && false   // false
bool or = true || false    // true
bool not = !true           // false
```

### Conditionals

```javascript
if (x > 10) {
    print("large")
}

if (score >= 90) {
    print("A")
}
if (score >= 80) {
    print("B")
}
```

## Built-in Functions

| Function | Description | Example |
|----------|-------------|---------|
| `print` | Print to stdout | `print("hello")` |
| `sqrt` | Square root | `sqrt(16)` → 4.0 |
| `abs` | Absolute value | `abs(-42)` → 42 |
| `sin`, `cos`, `tan` | Trigonometry | `sin(0)` → 0.0 |
| `log`, `exp` | Logarithm/exponential | `log(1)` → 0.0 |
| `pow` | Power | `pow(2, 10)` → 1024.0 |
| `floor`, `ceil`, `round` | Rounding | `floor(3.7)` → 3 |
| `min`, `max` | Min/max of args | `min(3, 1, 2)` → 1 |
| `len` | Length of collection | `len("hello")` → 5 |
| `int`, `float`, `str` | Type conversion | `int(3.7)` → 3 |

### Constants

```javascript
print(PI)   // 3.141592653589793
print(E)    // 2.718281828459045
print(INF)  // inf
```

## Architecture

The interpreter follows a classic three-phase architecture:

1. **Lexer** (`lang/lexer/`): Tokenizes source code
2. **Parser** (`lang/parser/`): Builds Abstract Syntax Tree
3. **Interpreter** (`lang/interpreter/`): Executes the AST

### Key Design Patterns

- **Visitor Pattern**: AST traversal via `interpret_node()`
- **Environment Chain**: Lexical scoping via linked `Environment` objects
- **Exception-based Control Flow**: `ReturnValue` exception for returns

## Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=lang --cov-report=html

# Run specific test class
python -m pytest tests/test_interpreter.py::TestInterpreter -v
```

## Example Programs

See the `examples/` directory:

- `01_basic_types.lang` - Variable declarations and types
- `02_functions.lang` - Function definitions and calls
- `03_closures.lang` - Anonymous functions and closures
- `04_recursion.lang` - Recursive functions
- `05_complex.lang` - Complex number operations
- `06_matrices.lang` - Matrix operations
- `07_operators.lang` - All operators
- `08_conditionals.lang` - If statements
- `09_comprehensive.lang` - Full feature demonstration

## License

MIT License
