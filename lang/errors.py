"""
Custom exceptions for the language interpreter.
"""


class LangError(Exception):
    """Base exception for all language errors."""
    
    def __init__(self, message: str, line: int = None, column: int = None):
        self.message = message
        self.line = line
        self.column = column
        
        location = ""
        if line is not None:
            location = f" at line {line}"
            if column is not None:
                location += f", column {column}"
        
        super().__init__(f"{self.__class__.__name__}{location}: {message}")


class LexerError(LangError):
    """Error during lexical analysis (tokenization)."""
    pass


class ParseError(LangError):
    """Error during parsing (syntax analysis)."""
    pass


class RuntimeError(LangError):
    """Error during interpretation/execution."""
    pass


class ReturnValue(Exception):
    """
    Special exception used to implement return statements.
    Not an error - it's a control flow mechanism.
    """
    
    def __init__(self, value):
        self.value = value
        super().__init__()
