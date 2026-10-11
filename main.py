#!/usr/bin/env python3
"""
Main entry point for the Programming Language Interpreter.

Usage:
    python main.py              # Start REPL
    python main.py <file>       # Run a file
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lang.lexer import Lexer
from lang.parser import Parser
from lang.interpreter import Interpreter
from lang.errors import LangError


def run_file(filename: str):
    """
    Run a source file.
    
    Args:
        filename: Path to the source file
    """
    interpreter = Interpreter()
    
    try:
        result = interpreter.run_file(filename)
        return result
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    except LangError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def start_repl():
    """Start the interactive REPL."""
    from lang.repl import REPL
    repl = REPL()
    repl.start()


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        # Run file
        filename = sys.argv[1]
        run_file(filename)
    else:
        # Start REPL
        start_repl()


if __name__ == '__main__':
    main()
