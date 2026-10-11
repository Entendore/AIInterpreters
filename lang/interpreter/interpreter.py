"""
Interpreter for the programming language.
Executes the AST and produces results.
"""

from __future__ import annotations
from typing import Any

from .environment import Environment
from .builtins import get_builtins
from .types import Complex, Matrix
from ..parser.ast_nodes import (
    ASTNode, Program, Declaration, Assignment, ReturnStatement,
    ExpressionStatement, Block, IfStatement, FunctionDeclaration,
    Closure, RecursionDef, PatternDef, IntLiteral, FloatLiteral,
    StringLiteral, BoolLiteral, ComplexLiteral, MatrixLiteral,
    Identifier, BinaryExpr, UnaryExpr, FunctionCall, SliceExpr, ParenExpr
)
from ..errors import RuntimeError, ReturnValue


class Function:
    """
    Runtime representation of a named function.
    """
    
    def __init__(self, declaration: FunctionDeclaration, closure: Environment):
        """
        Initialize a function.
        
        Args:
            declaration: The function declaration AST node
            closure: The environment where the function was defined
        """
        self.declaration = declaration
        self.closure = closure
    
    def __call__(self, *args):
        """
        Call the function with arguments.
        
        Args:
            *args: Arguments to pass to the function
            
        Returns:
            The function's return value (None if no return)
        """
        # Create new environment for function body
        env = Environment(self.closure)
        
        # Bind parameters
        for i, param in enumerate(self.declaration.parameters):
            if i < len(args):
                env.define(param, args[i])
            else:
                raise RuntimeError(f"Missing argument: {param}")
        
        # Execute function body
        try:
            interpret_node(self.declaration.body, env)
        except ReturnValue as ret:
            return ret.value
        
        return None
    
    def __repr__(self):
        return f"<function {self.declaration.name}>"


class ClosureFunc:
    """
    Runtime representation of a closure (anonymous function).
    """
    
    def __init__(self, closure_node: Closure, closure_env: Environment, name: str = None):
        """
        Initialize a closure.
        
        Args:
            closure_node: The closure AST node
            closure_env: The environment where the closure was defined
            name: Optional name for recursive closures
        """
        self.closure_node = closure_node
        self.closure_env = closure_env
        self.name = name
    
    def __call__(self, *args):
        """
        Call the closure with arguments.
        
        Args:
            *args: Arguments to pass to the closure
            
        Returns:
            The closure's return value (None if no return)
        """
        env = Environment(self.closure_env)
        
        # For named closures, bind the name for recursion
        if self.name:
            env.define(self.name, self)
        
        # Bind parameters
        for i, param in enumerate(self.closure_node.parameters):
            if i < len(args):
                env.define(param, args[i])
            else:
                raise RuntimeError(f"Missing argument: {param}")
        
        # Execute closure body
        try:
            interpret_node(self.closure_node.body, env)
        except ReturnValue as ret:
            return ret.value
        
        return None
    
    def __repr__(self):
        if self.name:
            return f"<closure {self.name}>"
        return "<anonymous closure>"


def interpret_node(node: Any, env: Environment) -> Any:
    """
    Interpret an AST node in the given environment.
    
    Args:
        node: AST node to interpret
        env: Environment for variable lookup
        
    Returns:
        The result of interpreting the node
        
    Raises:
        RuntimeError: For runtime errors
        ReturnValue: For return statements (control flow)
    """
    # ========================================================================
    # Program
    # ========================================================================
    
    if isinstance(node, Program):
        result = None
        for stmt in node.statements:
            try:
                result = interpret_node(stmt, env)
            except ReturnValue as ret:
                result = ret.value
        return result
    
    # ========================================================================
    # Literals
    # ========================================================================
    
    if isinstance(node, IntLiteral):
        return node.value
    
    if isinstance(node, FloatLiteral):
        return node.value
    
    if isinstance(node, StringLiteral):
        return node.value
    
    if isinstance(node, BoolLiteral):
        return node.value
    
    if isinstance(node, ComplexLiteral):
        return Complex(node.real, node.imag)
    
    if isinstance(node, MatrixLiteral):
        rows = []
        for row in node.rows:
            evaluated_row = [interpret_node(elem, env) for elem in row]
            rows.append(evaluated_row)
        return Matrix(rows)
    
    # ========================================================================
    # Expressions
    # ========================================================================
    
    if isinstance(node, Identifier):
        return env.get(node.name)
    
    if isinstance(node, BinaryExpr):
        left = interpret_node(node.left, env)
        right = interpret_node(node.right, env)
        
        op = node.operator
        if op == '+':
            return left + right
        if op == '-':
            return left - right
        if op == '*':
            return left * right
        if op == '/':
            return left / right
        if op == '&&':
            return bool(left) and bool(right)
        if op == '||':
            return bool(left) or bool(right)
        if op == '==':
            return left == right
        if op == '!=':
            return left != right
        if op == '<':
            return left < right
        if op == '>':
            return left > right
        if op == '<=':
            return left <= right
        if op == '>=':
            return left >= right
        
        raise RuntimeError(f"Unknown operator: {op}")
    
    if isinstance(node, UnaryExpr):
        operand = interpret_node(node.operand, env)
        
        if node.operator == '!':
            return not operand
        if node.operator == '-':
            return -operand
        
        raise RuntimeError(f"Unknown unary operator: {node.operator}")
    
    if isinstance(node, ParenExpr):
        return interpret_node(node.expression, env)
    
    if isinstance(node, FunctionCall):
        func = env.get(node.name)
        args = [interpret_node(arg, env) for arg in node.arguments]
        
        if callable(func):
            return func(*args)
        
        raise RuntimeError(f"'{node.name}' is not callable")
    
    if isinstance(node, SliceExpr):
        value = env.get(node.identifier)
        
        if isinstance(value, (list, str)):
            start = int(interpret_node(node.start, env)) if node.start else None
            end = int(interpret_node(node.end, env)) if node.end else None
            return value[start:end]
        
        raise RuntimeError(f"Cannot slice {type(value).__name__}")
    
    # ========================================================================
    # Statements
    # ========================================================================
    
    if isinstance(node, Declaration):
        value = interpret_node(node.value, env)
        env.define(node.name, value)
        return value
    
    if isinstance(node, Assignment):
        value = interpret_node(node.value, env)
        env.set(node.name, value)
        return value
    
    if isinstance(node, ReturnStatement):
        value = interpret_node(node.value, env)
        raise ReturnValue(value)
    
    if isinstance(node, ExpressionStatement):
        return interpret_node(node.expression, env)
    
    if isinstance(node, Block):
        block_env = Environment(env)
        result = None
        for stmt in node.statements:
            result = interpret_node(stmt, block_env)
        return result
    
    if isinstance(node, IfStatement):
        condition = interpret_node(node.condition, env)
        if condition:
            return interpret_node(node.then_block, env)
        elif node.else_block:
            return interpret_node(node.else_block, env)
        return None
    
    # ========================================================================
    # Function Definitions
    # ========================================================================
    
    if isinstance(node, FunctionDeclaration):
        func = Function(node, env)
        env.define(node.name, func)
        return func
    
    if isinstance(node, Closure):
        return ClosureFunc(node, env, node.name)
    
    if isinstance(node, RecursionDef):
        # Create a closure for the recursive function
        closure_node = Closure(None, node.parameters, node.body)
        return ClosureFunc(closure_node, env, None)
    
    if isinstance(node, PatternDef):
        # Patterns are stored as-is for now
        return node
    
    raise RuntimeError(f"Unknown node type: {type(node).__name__}")


class Interpreter:
    """
    Main interpreter class that manages the global environment
    and provides entry points for execution.
    """
    
    def __init__(self):
        """Initialize the interpreter with a global environment."""
        self.global_env = Environment()
        self._setup_builtins()
    
    def _setup_builtins(self):
        """Set up built-in functions in the global environment."""
        for name, value in get_builtins().items():
            self.global_env.define(name, value)
    
    def run(self, source: str) -> Any:
        """
        Run source code.
        
        Args:
            source: Source code string
            
        Returns:
            Result of the last expression
        """
        from ..lexer import Lexer
        from ..parser import Parser
        
        # Tokenize
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # Parse
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Interpret
        return interpret_node(ast, self.global_env)
    
    def run_file(self, filename: str) -> Any:
        """
        Run a source file.
        
        Args:
            filename: Path to source file
            
        Returns:
            Result of the last expression
        """
        with open(filename, 'r') as f:
            source = f.read()
        return self.run(source)
