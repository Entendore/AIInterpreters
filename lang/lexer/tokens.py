"""
Token definitions for the language lexer.
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Any


class TokenType(Enum):
    """All token types in the language."""
    
    # Literals
    INT_LITERAL = auto()
    FLOAT_LITERAL = auto()
    STRING_LITERAL = auto()
    BOOL_LITERAL = auto()
    COMPLEX_LITERAL = auto()
    
    # Identifiers and Keywords
    IDENTIFIER = auto()
    
    # Type Keywords
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    BOOL = auto()
    COMPLEX = auto()
    MATRIX = auto()
    VAR = auto()
    
    # Control Keywords
    FUNCTION = auto()
    RETURN = auto()
    IF = auto()
    ELSE = auto()
    TRUE = auto()
    FALSE = auto()
    
    # Recursion Keywords
    REC = auto()
    RECURSE = auto()
    R = auto()
    
    # Pattern Keyword
    PATTERN = auto()
    
    # Arithmetic Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    
    # Comparison Operators
    EQ = auto()
    NEQ = auto()
    LT = auto()
    GT = auto()
    LTE = auto()
    GTE = auto()
    
    # Logical Operators
    AND = auto()
    OR = auto()
    NOT = auto()
    
    # Assignment and Arrows
    ASSIGN = auto()
    ARROW = auto()       # ->
    FAT_ARROW = auto()   # =>
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    COLON = auto()
    
    # Special
    EOF = auto()
    NEWLINE = auto()


@dataclass
class Token:
    """Represents a lexical token with position information."""
    
    type: TokenType
    value: Any
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, L{self.line}:C{self.column})"


# Keywords mapping
KEYWORDS = {
    'function': TokenType.FUNCTION,
    'return': TokenType.RETURN,
    'int': TokenType.INT,
    'float': TokenType.FLOAT,
    'string': TokenType.STRING,
    'bool': TokenType.BOOL,
    'complex': TokenType.COMPLEX,
    'matrix': TokenType.MATRIX,
    'var': TokenType.VAR,
    'true': TokenType.TRUE,
    'false': TokenType.FALSE,
    'rec': TokenType.REC,
    'recurse': TokenType.RECURSE,
    'r': TokenType.R,
    'pattern': TokenType.PATTERN,
    'if': TokenType.IF,
    'else': TokenType.ELSE,
}

# Type tokens for quick checking
TYPE_TOKENS = {
    TokenType.INT,
    TokenType.FLOAT,
    TokenType.STRING,
    TokenType.BOOL,
    TokenType.COMPLEX,
    TokenType.MATRIX,
    TokenType.VAR,
}
