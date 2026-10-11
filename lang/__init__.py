"""
Programming Language Interpreter
================================

A complete interpreter for a custom programming language with support for:
- Variables and types (int, float, string, bool, complex, matrix, var)
- Functions and closures
- Recursion with special keywords (rec, recurse, r)
- Complex numbers and matrices
- Pattern matching
- Array slicing

Usage:
    from lang import Interpreter
    
    interpreter = Interpreter()
    result = interpreter.run('int x = 10')
    
    # Or use the REPL
    from lang.repl import REPL
    REPL().start()
"""

__version__ = '1.0.0'
__author__ = 'Language Developer'

# Import main components
from .lexer import Lexer, Token, TokenType
from .parser import Parser, ASTNode, Program
from .interpreter import Interpreter, interpret_node
from .errors import LangError, LexerError, ParseError, RuntimeError

__all__ = [
    # Version
    '__version__',
    '__author__',
    
    # Lexer
    'Lexer',
    'Token',
    'TokenType',
    
    # Parser
    'Parser',
    'ASTNode',
    'Program',
    
    # Interpreter
    'Interpreter',
    'interpret_node',
    
    # Errors
    'LangError',
    'LexerError',
    'ParseError',
    'RuntimeError',
]
