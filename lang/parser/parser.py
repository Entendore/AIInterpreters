"""
Recursive descent parser for the programming language.
Converts a stream of tokens into an Abstract Syntax Tree (AST).
"""

from __future__ import annotations
from typing import List, Optional, Tuple, TYPE_CHECKING

from .ast_nodes import (
    ASTNode, Program, Declaration, Assignment, ReturnStatement,
    ExpressionStatement, Block, IfStatement, FunctionDeclaration,
    Closure, RecursionDef, PatternDef, IntLiteral, FloatLiteral,
    StringLiteral, BoolLiteral, ComplexLiteral, MatrixLiteral,
    Identifier, BinaryExpr, UnaryExpr, FunctionCall, SliceExpr, ParenExpr
)
from ..lexer.tokens import Token, TokenType, TYPE_TOKENS
from ..errors import ParseError


class Parser:
    """
    Recursive descent parser for the language.
    
    Parses a list of tokens into an AST. Implements proper operator
    precedence for expressions and handles all language constructs.
    """
    
    def __init__(self, tokens: List[Token]):
        """
        Initialize parser with token stream.
        
        Args:
            tokens: List of Token objects from the lexer
        """
        self.tokens = tokens
        self.pos = 0
    
    # ========================================================================
    # Token Navigation
    # ========================================================================
    
    def current_token(self) -> Token:
        """Get the current token."""
        return self.tokens[self.pos]
    
    def peek_token(self, offset: int = 1) -> Token:
        """Look ahead at a future token."""
        pos = self.pos + offset
        if pos >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[pos]
    
    def advance(self) -> Token:
        """Advance to next token and return the current one."""
        token = self.current_token()
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token
    
    def expect(self, token_type: TokenType, message: str = None) -> Token:
        """
        Expect a specific token type, raise error if not found.
        
        Args:
            token_type: Expected token type
            message: Optional custom error message
            
        Returns:
            The matched token
            
        Raises:
            ParseError if current token doesn't match
        """
        if self.current_token().type != token_type:
            msg = message or f"Expected {token_type.name}, got {self.current_token().type.name}"
            raise ParseError(msg, self.current_token().line, self.current_token().column)
        return self.advance()
    
    def match(self, *types: TokenType) -> bool:
        """Check if current token matches any of the given types."""
        return self.current_token().type in types
    
    # ========================================================================
    # Main Parse Methods
    # ========================================================================
    
    def parse(self) -> Program:
        """
        Parse the token stream into a Program AST.
        
        Returns:
            Program node containing all statements
        """
        statements = []
        while not self.match(TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return Program(statements)
    
    def parse_statement(self) -> Optional[ASTNode]:
        """
        Parse a single statement.
        
        Returns:
            AST node for the statement
        """
        # Variable declaration
        if self.match(*TYPE_TOKENS):
            return self.parse_declaration()
        
        # Function declaration
        if self.match(TokenType.FUNCTION):
            return self.parse_function_declaration()
        
        # Recursion definition (at statement level)
        if self.match(TokenType.REC, TokenType.RECURSE, TokenType.R):
            return self.parse_recursion()
        
        # Pattern definition
        if self.match(TokenType.PATTERN):
            return self.parse_pattern()
        
        # Return statement
        if self.match(TokenType.RETURN):
            return self.parse_return()
        
        # If statement
        if self.match(TokenType.IF):
            return self.parse_if()
        
        # Block
        if self.match(TokenType.LBRACE):
            return self.parse_block()
        
        # Expression statement or assignment
        return self.parse_expression_statement()
    
    # ========================================================================
    # Declarations and Assignments
    # ========================================================================
    
    def parse_type(self) -> str:
        """Parse a type keyword and return its name."""
        if self.match(*TYPE_TOKENS):
            return self.advance().value
        raise ParseError(
            "Expected type keyword",
            self.current_token().line,
            self.current_token().column
        )
    
    def parse_declaration(self) -> Declaration:
        """Parse a variable declaration."""
        var_type = self.parse_type()
        name_token = self.expect(TokenType.IDENTIFIER, "Expected identifier after type")
        self.expect(TokenType.ASSIGN, "Expected '=' in declaration")
        value = self.parse_expression()
        return Declaration(var_type, name_token.value, value)
    
    def parse_expression_statement(self) -> ASTNode:
        """Parse an expression statement or assignment."""
        # Check for assignment: <identifier> = <expression>
        if self.match(TokenType.IDENTIFIER) and self.peek_token().type == TokenType.ASSIGN:
            name = self.advance().value
            self.advance()  # Consume '='
            value = self.parse_expression()
            return Assignment(name, value)
        
        # Expression statement
        expr = self.parse_expression()
        return ExpressionStatement(expr)
    
    # ========================================================================
    # Function Definitions
    # ========================================================================
    
    def parse_function_declaration(self) -> FunctionDeclaration:
        """Parse a named function declaration."""
        self.expect(TokenType.FUNCTION)
        name_token = self.expect(TokenType.IDENTIFIER, "Expected function name")
        self.expect(TokenType.LPAREN, "Expected '(' after function name")
        parameters = self.parse_parameter_list()
        self.expect(TokenType.RPAREN, "Expected ')' after parameters")
        body = self.parse_block()
        return FunctionDeclaration(name_token.value, parameters, body)
    
    def parse_parameter_list(self) -> List[str]:
        """Parse a list of function parameters."""
        parameters = []
        
        if not self.match(TokenType.RPAREN):
            # Handle typed parameters (for patterns)
            if self.match(*TYPE_TOKENS):
                self.advance()  # Skip type
                if self.match(TokenType.IDENTIFIER):
                    parameters.append(self.advance().value)
                while self.match(TokenType.COMMA):
                    self.advance()
                    if self.match(*TYPE_TOKENS):
                        self.advance()
                    if self.match(TokenType.IDENTIFIER):
                        parameters.append(self.advance().value)
            else:
                # Untyped parameters
                if self.match(TokenType.IDENTIFIER):
                    parameters.append(self.advance().value)
                while self.match(TokenType.COMMA):
                    self.advance()
                    if self.match(TokenType.IDENTIFIER):
                        parameters.append(self.advance().value)
        
        return parameters
    
    def parse_closure(self) -> Closure:
        """Parse a closure (anonymous or named)."""
        self.expect(TokenType.FUNCTION)
        
        name = None
        if self.match(TokenType.IDENTIFIER):
            name = self.advance().value
        
        self.expect(TokenType.LPAREN, "Expected '(' in closure")
        parameters = self.parse_parameter_list()
        self.expect(TokenType.RPAREN, "Expected ')' after closure parameters")
        body = self.parse_block()
        
        return Closure(name, parameters, body)
    
    def parse_recursion(self) -> RecursionDef:
        """Parse a recursion definition at statement level."""
        keyword = self.advance().value
        self.expect(TokenType.LPAREN, "Expected '(' after recursion keyword")
        parameters = self.parse_parameter_list()
        self.expect(TokenType.RPAREN, "Expected ')' after parameters")
        self.expect(TokenType.FAT_ARROW, "Expected '=>' after parameters")
        return_type = self.parse_type()
        body = self.parse_block()
        return RecursionDef(keyword, parameters, return_type, body)
    
    def parse_recursion_expr(self) -> RecursionDef:
        """Parse a recursion definition in expression context."""
        return self.parse_recursion()
    
    def parse_pattern(self) -> PatternDef:
        """Parse a pattern definition."""
        self.expect(TokenType.PATTERN)
        
        # Parse typed parameters
        parameters = []
        while self.match(*TYPE_TOKENS):
            param_type = self.advance().value
            if self.match(TokenType.IDENTIFIER):
                param_name = self.advance().value
                parameters.append((param_type, param_name))
            if self.match(TokenType.COMMA):
                self.advance()
        
        self.expect(TokenType.ARROW, "Expected '->' in pattern")
        expression = self.parse_expression()
        self.expect(TokenType.ASSIGN, "Expected '=' in pattern")
        statement = self.parse_statement()
        
        return PatternDef(parameters, expression, statement)
    
    # ========================================================================
    # Control Flow
    # ========================================================================
    
    def parse_return(self) -> ReturnStatement:
        """Parse a return statement."""
        self.expect(TokenType.RETURN)
        value = self.parse_expression()
        return ReturnStatement(value)
    
    def parse_if(self) -> IfStatement:
        """Parse an if statement with optional else."""
        self.expect(TokenType.IF)
        condition = self.parse_expression()
        then_block = self.parse_block()
        
        else_block = None
        if self.match(TokenType.ELSE):
            self.advance()
            else_block = self.parse_block()
        
        return IfStatement(condition, then_block, else_block)
    
    def parse_block(self) -> Block:
        """Parse a block of statements."""
        self.expect(TokenType.LBRACE, "Expected '{' to start block")
        
        statements = []
        while not self.match(TokenType.RBRACE, TokenType.EOF):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        
        self.expect(TokenType.RBRACE, "Expected '}' to end block")
        return Block(statements)
    
    # ========================================================================
    # Expressions (Operator Precedence Parsing)
    # ========================================================================
    
    def parse_expression(self) -> ASTNode:
        """Parse an expression (entry point)."""
        return self.parse_or()
    
    def parse_or(self) -> ASTNode:
        """Parse logical OR expressions (lowest precedence)."""
        left = self.parse_and()
        while self.match(TokenType.OR):
            op = self.advance().value
            right = self.parse_and()
            left = BinaryExpr(left, op, right)
        return left
    
    def parse_and(self) -> ASTNode:
        """Parse logical AND expressions."""
        left = self.parse_equality()
        while self.match(TokenType.AND):
            op = self.advance().value
            right = self.parse_equality()
            left = BinaryExpr(left, op, right)
        return left
    
    def parse_equality(self) -> ASTNode:
        """Parse equality expressions (== and !=)."""
        left = self.parse_comparison()
        while self.match(TokenType.EQ, TokenType.NEQ):
            op = self.advance().value
            right = self.parse_comparison()
            left = BinaryExpr(left, op, right)
        return left
    
    def parse_comparison(self) -> ASTNode:
        """Parse comparison expressions (<, >, <=, >=)."""
        left = self.parse_additive()
        while self.match(TokenType.LT, TokenType.GT, TokenType.LTE, TokenType.GTE):
            op = self.advance().value
            right = self.parse_additive()
            left = BinaryExpr(left, op, right)
        return left
    
    def parse_additive(self) -> ASTNode:
        """Parse additive expressions (+ and -)."""
        left = self.parse_multiplicative()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.advance().value
            right = self.parse_multiplicative()
            left = BinaryExpr(left, op, right)
        return left
    
    def parse_multiplicative(self) -> ASTNode:
        """Parse multiplicative expressions (* and /)."""
        left = self.parse_unary()
        while self.match(TokenType.STAR, TokenType.SLASH):
            op = self.advance().value
            right = self.parse_unary()
            left = BinaryExpr(left, op, right)
        return left
    
    def parse_unary(self) -> ASTNode:
        """Parse unary expressions (! and -)."""
        if self.match(TokenType.NOT, TokenType.MINUS):
            op = self.advance().value
            operand = self.parse_unary()
            return UnaryExpr(op, operand)
        return self.parse_primary()
    
    def parse_primary(self) -> ASTNode:
        """Parse primary expressions (literals, identifiers, calls)."""
        # Literals
        if self.match(TokenType.INT_LITERAL):
            return IntLiteral(self.advance().value)
        
        if self.match(TokenType.FLOAT_LITERAL):
            return FloatLiteral(self.advance().value)
        
        if self.match(TokenType.STRING_LITERAL):
            return StringLiteral(self.advance().value)
        
        if self.match(TokenType.BOOL_LITERAL):
            return BoolLiteral(self.advance().value)
        
        if self.match(TokenType.COMPLEX_LITERAL):
            value = self.advance().value
            return ComplexLiteral(value[0], value[1])
        
        # Matrix literal or block
        if self.match(TokenType.LBRACE):
            return self.parse_matrix_or_block()
        
        # Parenthesized expression
        if self.match(TokenType.LPAREN):
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN, "Expected ')' after expression")
            return ParenExpr(expr)
        
        # Identifier, function call, or slice
        if self.match(TokenType.IDENTIFIER):
            return self.parse_identifier_expr()
        
        # Closure
        if self.match(TokenType.FUNCTION):
            return self.parse_closure()
        
        # Recursion expression
        if self.match(TokenType.REC, TokenType.RECURSE, TokenType.R):
            return self.parse_recursion_expr()
        
        raise ParseError(
            f"Unexpected token: {self.current_token().type.name}",
            self.current_token().line,
            self.current_token().column
        )
    
    def parse_identifier_expr(self) -> ASTNode:
        """Parse identifier, function call, or slice."""
        name = self.advance().value
        
        # Function call
        if self.match(TokenType.LPAREN):
            self.advance()
            args = self.parse_argument_list()
            self.expect(TokenType.RPAREN, "Expected ')' after arguments")
            return FunctionCall(name, args)
        
        # Slice
        if self.match(TokenType.LBRACKET):
            self.advance()
            start = None
            end = None
            
            if self.match(TokenType.COLON):
                self.advance()
                if not self.match(TokenType.RBRACKET):
                    end = self.parse_expression()
            else:
                start = self.parse_expression()
                if self.match(TokenType.COLON):
                    self.advance()
                    if not self.match(TokenType.RBRACKET):
                        end = self.parse_expression()
            
            self.expect(TokenType.RBRACKET, "Expected ']' after slice")
            return SliceExpr(name, start, end)
        
        return Identifier(name)
    
    def parse_matrix_or_block(self) -> ASTNode:
        """Distinguish between matrix literal and block."""
        self.expect(TokenType.LBRACE)
        
        if self.match(TokenType.LBRACE):
            return self.parse_matrix_literal()
        else:
            statements = []
            while not self.match(TokenType.RBRACE, TokenType.EOF):
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)
            self.expect(TokenType.RBRACE, "Expected '}' to end block")
            return Block(statements)
    
    def parse_matrix_literal(self) -> MatrixLiteral:
        """Parse a matrix literal."""
        rows = []
        
        while self.match(TokenType.LBRACE):
            self.advance()
            row = []
            
            if not self.match(TokenType.RBRACE):
                row.append(self.parse_expression())
                while self.match(TokenType.COMMA):
                    self.advance()
                    row.append(self.parse_expression())
            
            self.expect(TokenType.RBRACE, "Expected '}' to end row")
            rows.append(row)
            
            if self.match(TokenType.COMMA):
                self.advance()
        
        self.expect(TokenType.RBRACE, "Expected '}' to end matrix")
        return MatrixLiteral(rows)
    
    def parse_argument_list(self) -> List[ASTNode]:
        """Parse a list of function arguments."""
        arguments = []
        
        if not self.match(TokenType.RPAREN):
            arguments.append(self.parse_expression())
            while self.match(TokenType.COMMA):
                self.advance()
                arguments.append(self.parse_expression())
        
        return arguments
