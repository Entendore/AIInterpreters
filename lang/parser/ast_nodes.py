"""
Abstract Syntax Tree (AST) node definitions.
All nodes are defined as dataclasses for immutability and clear representation.
"""

from dataclasses import dataclass
from typing import Any, List, Optional, Tuple


@dataclass
class ASTNode:
    """Base class for all AST nodes."""
    pass


# ============================================================================
# Program Structure
# ============================================================================

@dataclass
class Program(ASTNode):
    """Root node representing a complete program."""
    statements: List[ASTNode]


# ============================================================================
# Literals
# ============================================================================

@dataclass
class IntLiteral(ASTNode):
    """Integer literal (e.g., 42)."""
    value: int


@dataclass
class FloatLiteral(ASTNode):
    """Floating-point literal (e.g., 3.14)."""
    value: float


@dataclass
class StringLiteral(ASTNode):
    """String literal (e.g., "hello")."""
    value: str


@dataclass
class BoolLiteral(ASTNode):
    """Boolean literal (true or false)."""
    value: bool


@dataclass
class ComplexLiteral(ASTNode):
    """Complex number literal (e.g., 1.0+2.0i)."""
    real: float
    imag: float


@dataclass
class MatrixLiteral(ASTNode):
    """Matrix literal (e.g., {{1, 2}, {3, 4}})."""
    rows: List[List[ASTNode]]


# ============================================================================
# Expressions
# ============================================================================

@dataclass
class Identifier(ASTNode):
    """Variable or function name."""
    name: str


@dataclass
class BinaryExpr(ASTNode):
    """Binary operation (e.g., a + b)."""
    left: ASTNode
    operator: str
    right: ASTNode


@dataclass
class UnaryExpr(ASTNode):
    """Unary operation (e.g., -x, !flag)."""
    operator: str
    operand: ASTNode


@dataclass
class FunctionCall(ASTNode):
    """Function call expression (e.g., func(a, b))."""
    name: str
    arguments: List[ASTNode]


@dataclass
class SliceExpr(ASTNode):
    """Array slice expression (e.g., arr[0:5])."""
    identifier: str
    start: Optional[ASTNode]
    end: Optional[ASTNode]


@dataclass
class ParenExpr(ASTNode):
    """Parenthesized expression for grouping."""
    expression: ASTNode


# ============================================================================
# Statements
# ============================================================================

@dataclass
class Declaration(ASTNode):
    """Variable declaration with initialization."""
    var_type: str
    name: str
    value: ASTNode


@dataclass
class Assignment(ASTNode):
    """Variable assignment."""
    name: str
    value: ASTNode


@dataclass
class ReturnStatement(ASTNode):
    """Return statement."""
    value: ASTNode


@dataclass
class ExpressionStatement(ASTNode):
    """Expression used as a statement."""
    expression: ASTNode


@dataclass
class Block(ASTNode):
    """Block of statements enclosed in braces."""
    statements: List[ASTNode]


@dataclass
class IfStatement(ASTNode):
    """Conditional if statement with optional else."""
    condition: ASTNode
    then_block: ASTNode
    else_block: Optional[ASTNode] = None


# ============================================================================
# Function Definitions
# ============================================================================

@dataclass
class FunctionDeclaration(ASTNode):
    """Named function declaration."""
    name: str
    parameters: List[str]
    body: ASTNode


@dataclass
class Closure(ASTNode):
    """Anonymous function (lambda) or named closure."""
    name: Optional[str]
    parameters: List[str]
    body: ASTNode


@dataclass
class RecursionDef(ASTNode):
    """Recursive function using rec/recurse/r keywords."""
    keyword: str
    parameters: List[str]
    return_type: str
    body: ASTNode


@dataclass
class PatternDef(ASTNode):
    """Pattern matching definition."""
    parameters: List[Tuple[str, str]]  # (type, name) pairs
    expression: ASTNode
    statement: ASTNode
