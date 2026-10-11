"""
Built-in functions for the language interpreter.
"""

import math
from typing import Any, Callable


def get_builtins() -> dict:
    """
    Get all built-in functions and values.
    
    Returns:
        Dictionary mapping names to built-in functions/values
    """
    builtins = {}
    
    # ========================================================================
    # I/O Functions
    # ========================================================================
    
    def builtin_print(*args):
        """Print values to stdout."""
        print(*args)
        return None
    
    builtins['print'] = builtin_print
    
    # ========================================================================
    # Mathematical Functions
    # ========================================================================
    
    builtins['sqrt'] = lambda x: math.sqrt(x)
    builtins['abs'] = lambda x: abs(x)
    builtins['sin'] = lambda x: math.sin(x)
    builtins['cos'] = lambda x: math.cos(x)
    builtins['tan'] = lambda x: math.tan(x)
    builtins['asin'] = lambda x: math.asin(x)
    builtins['acos'] = lambda x: math.acos(x)
    builtins['atan'] = lambda x: math.atan(x)
    builtins['log'] = lambda x: math.log(x)
    builtins['log10'] = lambda x: math.log10(x)
    builtins['log2'] = lambda x: math.log2(x)
    builtins['exp'] = lambda x: math.exp(x)
    builtins['pow'] = lambda x, y: math.pow(x, y)
    builtins['floor'] = lambda x: math.floor(x)
    builtins['ceil'] = lambda x: math.ceil(x)
    builtins['round'] = lambda x: round(x)
    
    # ========================================================================
    # Aggregate Functions
    # ========================================================================
    
    builtins['min'] = lambda *args: min(args)
    builtins['max'] = lambda *args: max(args)
    builtins['sum'] = lambda *args: sum(args)
    
    # ========================================================================
    # Type Functions
    # ========================================================================
    
    builtins['int'] = lambda x: int(x)
    builtins['float'] = lambda x: float(x)
    builtins['str'] = lambda x: str(x)
    builtins['bool'] = lambda x: bool(x)
    builtins['type'] = lambda x: type(x).__name__
    
    # ========================================================================
    # Collection Functions
    # ========================================================================
    
    builtins['len'] = lambda x: len(x)
    builtins['range'] = lambda n: list(range(n))
    
    # ========================================================================
    # Constants
    # ========================================================================
    
    builtins['PI'] = math.pi
    builtins['E'] = math.e
    builtins['INF'] = float('inf')
    
    return builtins
