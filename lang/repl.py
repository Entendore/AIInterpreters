"""
Interactive REPL (Read-Eval-Print Loop) for the language.
"""

from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .errors import LangError


class REPL:
    """
    Interactive REPL for the programming language.
    
    Provides a command-line interface for interactively
    writing and executing code.
    """
    
    def __init__(self):
        """Initialize the REPL with a new interpreter."""
        self.interpreter = Interpreter()
        self.running = True
    
    def start(self):
        """Start the REPL loop."""
        self._print_welcome()
        
        while self.running:
            try:
                line = input(">>> ")
                self._handle_input(line)
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
            except EOFError:
                print("\nGoodbye!")
                break
    
    def _print_welcome(self):
        """Print welcome message."""
        print("=" * 50)
        print("  Programming Language Interpreter v1.0")
        print("  Interactive REPL")
        print("=" * 50)
        print()
        print("Commands:")
        print("  exit    - Exit the REPL")
        print("  help    - Show help message")
        print("  vars    - Show defined variables")
        print("  clear   - Clear all variables")
        print()
    
    def _handle_input(self, line: str):
        """
        Handle a line of input.
        
        Args:
            line: Input line from user
        """
        line = line.strip()
        
        if not line:
            return
        
        # Handle commands
        if line == 'exit':
            print("Goodbye!")
            self.running = False
            return
        
        if line == 'help':
            self._print_help()
            return
        
        if line == 'vars':
            self._print_variables()
            return
        
        if line == 'clear':
            self._clear_variables()
            return
        
        # Execute code
        try:
            result = self.interpreter.run(line)
            if result is not None:
                print(result)
        except LangError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")
    
    def _print_help(self):
        """Print help message."""
        print()
        print("Language Features:")
        print("-" * 40)
        print("  Variables:")
        print("    int x = 10")
        print("    float pi = 3.14")
        print("    string s = \"hello\"")
        print("    bool flag = true")
        print("    var auto = 42        # type inference")
        print()
        print("  Functions:")
        print("    function add(a, b) { return a + b }")
        print()
        print("  Closures:")
        print("    var square = function(x) { return x * x }")
        print()
        print("  Recursion:")
        print("    var fact = rec(n) => int {")
        print("      if (n <= 1) { return 1 }")
        print("      return n * fact(n - 1)")
        print("    }")
        print()
        print("  Complex Numbers:")
        print("    complex z = 1.0+2.0i")
        print()
        print("  Matrices:")
        print("    matrix m = {{1, 2}, {3, 4}}")
        print()
        print("Built-in Functions:")
        print("  print, sqrt, abs, sin, cos, tan, log, exp,")
        print("  pow, min, max, len, int, float, str")
        print()
    
    def _print_variables(self):
        """Print all defined variables."""
        print()
        print("Defined Variables:")
        print("-" * 40)
        
        variables = self.interpreter.global_env.all_variables()
        
        # Filter out built-ins
        builtins = set(get_builtins().keys())
        user_vars = {k: v for k, v in variables.items() if k not in builtins}
        
        if user_vars:
            for name, value in sorted(user_vars.items()):
                print(f"  {name} = {value}")
        else:
            print("  (no user-defined variables)")
        
        print()
    
    def _clear_variables(self):
        """Clear all user-defined variables."""
        self.interpreter = Interpreter()
        print("All variables cleared.")


def get_builtins():
    """Import get_builtins to avoid circular import."""
    from .interpreter.builtins import get_builtins as _get_builtins
    return _get_builtins()


def main():
    """Main entry point for the REPL."""
    repl = REPL()
    repl.start()


if __name__ == '__main__':
    main()
