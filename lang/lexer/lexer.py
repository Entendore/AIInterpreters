"""
Lexer for the programming language.
Converts source code into a stream of tokens.
"""

from typing import List, Optional
from .tokens import Token, TokenType, KEYWORDS
from ..errors import LexerError


class Lexer:
    """
    Tokenizer for the programming language.
    
    Converts source code text into a list of Token objects.
    Handles comments, string literals, number literals, identifiers,
    keywords, and all operators/delimiters.
    """
    
    def __init__(self, source: str):
        """
        Initialize the lexer with source code.
        
        Args:
            source: The source code string to tokenize
        """
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def current_char(self) -> Optional[str]:
        """Get the current character without advancing."""
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def peek_char(self, offset: int = 1) -> Optional[str]:
        """Look ahead at a character without advancing."""
        pos = self.pos + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self) -> Optional[str]:
        """Advance position and return the current character."""
        char = self.current_char()
        self.pos += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char
    
    def skip_whitespace(self):
        """Skip whitespace characters including newlines."""
        while self.current_char() and self.current_char() in ' \t\r\n':
            self.advance()
    
    def skip_comment(self) -> bool:
        """
        Skip a comment if present.
        
        Returns:
            True if a comment was skipped, False otherwise
        """
        if self.current_char() == '/' and self.peek_char() == '/':
            # Single-line comment
            self.advance()
            self.advance()
            while self.current_char() and self.current_char() != '\n':
                self.advance()
            return True
        
        elif self.current_char() == '/' and self.peek_char() == '*':
            # Multi-line comment
            self.advance()
            self.advance()
            while True:
                if self.current_char() is None:
                    raise LexerError(
                        "Unterminated multi-line comment",
                        self.line,
                        self.column
                    )
                if self.current_char() == '*' and self.peek_char() == '/':
                    self.advance()
                    self.advance()
                    break
                self.advance()
            return True
        
        return False
    
    def read_string(self) -> str:
        """
        Read a string literal.
        
        Returns:
            The string value (without quotes)
        """
        self.advance()  # Skip opening quote
        result = ""
        
        while self.current_char() and self.current_char() != '"':
            if self.current_char() == '\\':
                self.advance()
                escape_char = self.advance()
                escape_map = {'n': '\n', 't': '\t', '"': '"', '\\': '\\'}
                result += escape_map.get(escape_char, escape_char)
            else:
                result += self.advance()
        
        if self.current_char() != '"':
            raise LexerError(
                "Unterminated string literal",
                self.line,
                self.column
            )
        
        self.advance()  # Skip closing quote
        return result
    
    def read_number(self) -> Token:
        """
        Read a numeric literal (int, float, or complex).
        
        Returns:
            Token with appropriate type
        """
        start_line = self.line
        start_column = self.column
        result = ""
        
        # Read integer part
        while self.current_char() and self.current_char().isdigit():
            result += self.advance()
        
        # Check for float
        if self.current_char() == '.' and self.peek_char() and self.peek_char().isdigit():
            result += self.advance()  # Consume dot
            while self.current_char() and self.current_char().isdigit():
                result += self.advance()
            
            # Check for complex number
            if self.current_char() and self.current_char() in '+-' and self.peek_char():
                # Look ahead for complex number pattern
                saved_pos = self.pos
                saved_line = self.line
                saved_column = self.column
                op = self.advance()
                
                # Read imaginary part
                imag_part = ""
                while self.current_char() and self.current_char().isdigit():
                    imag_part += self.advance()
                
                if self.current_char() == '.' and self.peek_char() and self.peek_char().isdigit():
                    imag_part += self.advance()
                    while self.current_char() and self.current_char().isdigit():
                        imag_part += self.advance()
                
                if self.current_char() == 'i' and imag_part:
                    self.advance()
                    return Token(
                        TokenType.COMPLEX_LITERAL,
                        (float(result), float(op + imag_part)),
                        start_line,
                        start_column
                    )
                else:
                    # Not complex, restore position
                    self.pos = saved_pos
                    self.line = saved_line
                    self.column = saved_column
            
            return Token(TokenType.FLOAT_LITERAL, float(result), start_line, start_column)
        
        return Token(TokenType.INT_LITERAL, int(result), start_line, start_column)
    
    def read_identifier(self) -> Token:
        """
        Read an identifier or keyword.
        
        Returns:
            Token for identifier or keyword
        """
        start_line = self.line
        start_column = self.column
        result = ""
        
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            result += self.advance()
        
        # Check for keywords
        token_type = KEYWORDS.get(result, TokenType.IDENTIFIER)
        
        # Handle boolean literals
        if token_type == TokenType.TRUE:
            return Token(TokenType.BOOL_LITERAL, True, start_line, start_column)
        elif token_type == TokenType.FALSE:
            return Token(TokenType.BOOL_LITERAL, False, start_line, start_column)
        
        return Token(token_type, result, start_line, start_column)
    
    def tokenize(self) -> List[Token]:
        """
        Tokenize the source code.
        
        Returns:
            List of Token objects ending with EOF token
        """
        while self.current_char():
            # Skip whitespace
            self.skip_whitespace()
            
            if self.current_char() is None:
                break
            
            # Skip comments
            if self.skip_comment():
                continue
            
            start_line = self.line
            start_column = self.column
            char = self.current_char()
            
            # String literals
            if char == '"':
                value = self.read_string()
                self.tokens.append(Token(TokenType.STRING_LITERAL, value, start_line, start_column))
            
            # Numbers
            elif char.isdigit():
                self.tokens.append(self.read_number())
            
            # Identifiers and keywords
            elif char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())
            
            # Two-character operators
            elif char == '&' and self.peek_char() == '&':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.AND, '&&', start_line, start_column))
            
            elif char == '|' and self.peek_char() == '|':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.OR, '||', start_line, start_column))
            
            elif char == '=' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.EQ, '==', start_line, start_column))
            
            elif char == '!' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.NEQ, '!=', start_line, start_column))
            
            elif char == '=' and self.peek_char() == '>':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.FAT_ARROW, '=>', start_line, start_column))
            
            elif char == '-' and self.peek_char() == '>':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.ARROW, '->', start_line, start_column))
            
            elif char == '<' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.LTE, '<=', start_line, start_column))
            
            elif char == '>' and self.peek_char() == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.GTE, '>=', start_line, start_column))
            
            # Single-character operators and delimiters
            elif char == '+':
                self.advance()
                self.tokens.append(Token(TokenType.PLUS, '+', start_line, start_column))
            
            elif char == '-':
                self.advance()
                self.tokens.append(Token(TokenType.MINUS, '-', start_line, start_column))
            
            elif char == '*':
                self.advance()
                self.tokens.append(Token(TokenType.STAR, '*', start_line, start_column))
            
            elif char == '/':
                self.advance()
                self.tokens.append(Token(TokenType.SLASH, '/', start_line, start_column))
            
            elif char == '<':
                self.advance()
                self.tokens.append(Token(TokenType.LT, '<', start_line, start_column))
            
            elif char == '>':
                self.advance()
                self.tokens.append(Token(TokenType.GT, '>', start_line, start_column))
            
            elif char == '!':
                self.advance()
                self.tokens.append(Token(TokenType.NOT, '!', start_line, start_column))
            
            elif char == '=':
                self.advance()
                self.tokens.append(Token(TokenType.ASSIGN, '=', start_line, start_column))
            
            elif char == '(':
                self.advance()
                self.tokens.append(Token(TokenType.LPAREN, '(', start_line, start_column))
            
            elif char == ')':
                self.advance()
                self.tokens.append(Token(TokenType.RPAREN, ')', start_line, start_column))
            
            elif char == '{':
                self.advance()
                self.tokens.append(Token(TokenType.LBRACE, '{', start_line, start_column))
            
            elif char == '}':
                self.advance()
                self.tokens.append(Token(TokenType.RBRACE, '}', start_line, start_column))
            
            elif char == '[':
                self.advance()
                self.tokens.append(Token(TokenType.LBRACKET, '[', start_line, start_column))
            
            elif char == ']':
                self.advance()
                self.tokens.append(Token(TokenType.RBRACKET, ']', start_line, start_column))
            
            elif char == ',':
                self.advance()
                self.tokens.append(Token(TokenType.COMMA, ',', start_line, start_column))
            
            elif char == ':':
                self.advance()
                self.tokens.append(Token(TokenType.COLON, ':', start_line, start_column))
            
            else:
                raise LexerError(f"Unexpected character: {char!r}", start_line, start_column)
        
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens
