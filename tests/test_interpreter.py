"""
Test suite for the language interpreter.
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lang.lexer import Lexer, Token, TokenType
from lang.parser import Parser
from lang.interpreter import Interpreter
from lang.errors import LexerError, ParseError, RuntimeError


class TestLexer(unittest.TestCase):
    """Test cases for the lexer."""
    
    def test_int_literals(self):
        """Test integer literal tokenization."""
        lexer = Lexer("42 0 123456")
        tokens = lexer.tokenize()
        
        self.assertEqual(tokens[0].type, TokenType.INT_LITERAL)
        self.assertEqual(tokens[0].value, 42)
        self.assertEqual(tokens[1].type, TokenType.INT_LITERAL)
        self.assertEqual(tokens[1].value, 0)
        self.assertEqual(tokens[2].type, TokenType.INT_LITERAL)
        self.assertEqual(tokens[2].value, 123456)
    
    def test_float_literals(self):
        """Test float literal tokenization."""
        lexer = Lexer("3.14 0.5 123.456")
        tokens = lexer.tokenize()
        
        self.assertEqual(tokens[0].type, TokenType.FLOAT_LITERAL)
        self.assertAlmostEqual(tokens[0].value, 3.14)
    
    def test_string_literals(self):
        """Test string literal tokenization."""
        lexer = Lexer('"hello" "world"')
        tokens = lexer.tokenize()
        
        self.assertEqual(tokens[0].type, TokenType.STRING_LITERAL)
        self.assertEqual(tokens[0].value, "hello")
    
    def test_bool_literals(self):
        """Test boolean literal tokenization."""
        lexer = Lexer("true false")
        tokens = lexer.tokenize()
        
        self.assertEqual(tokens[0].type, TokenType.BOOL_LITERAL)
        self.assertTrue(tokens[0].value)
        self.assertEqual(tokens[1].type, TokenType.BOOL_LITERAL)
        self.assertFalse(tokens[1].value)
    
    def test_complex_literals(self):
        """Test complex number literal tokenization."""
        lexer = Lexer("1.0+2.0i 3.14-1.59i")
        tokens = lexer.tokenize()
        
        self.assertEqual(tokens[0].type, TokenType.COMPLEX_LITERAL)
        self.assertEqual(tokens[0].value, (1.0, 2.0))
        self.assertEqual(tokens[1].type, TokenType.COMPLEX_LITERAL)
        self.assertEqual(tokens[1].value, (3.14, -1.59))
    
    def test_keywords(self):
        """Test keyword tokenization."""
        lexer = Lexer("int float string bool function return")
        tokens = lexer.tokenize()
        
        self.assertEqual(tokens[0].type, TokenType.INT)
        self.assertEqual(tokens[1].type, TokenType.FLOAT)
        self.assertEqual(tokens[2].type, TokenType.STRING)
        self.assertEqual(tokens[3].type, TokenType.BOOL)
        self.assertEqual(tokens[4].type, TokenType.FUNCTION)
        self.assertEqual(tokens[5].type, TokenType.RETURN)
    
    def test_operators(self):
        """Test operator tokenization."""
        lexer = Lexer("+ - * / == != < > <= >=")
        tokens = lexer.tokenize()
        
        self.assertEqual(tokens[0].type, TokenType.PLUS)
        self.assertEqual(tokens[4].type, TokenType.EQ)
        self.assertEqual(tokens[5].type, TokenType.NEQ)
        self.assertEqual(tokens[8].type, TokenType.LTE)
        self.assertEqual(tokens[9].type, TokenType.GTE)
    
    def test_comments(self):
        """Test comment handling."""
        lexer = Lexer("// comment\n42 /* multi\nline */ 10")
        tokens = lexer.tokenize()
        
        # Comments should be skipped
        self.assertEqual(tokens[0].type, TokenType.INT_LITERAL)
        self.assertEqual(tokens[0].value, 42)
        self.assertEqual(tokens[1].type, TokenType.INT_LITERAL)
        self.assertEqual(tokens[1].value, 10)
    
    def test_unterminated_string(self):
        """Test error on unterminated string."""
        lexer = Lexer('"hello')
        with self.assertRaises(LexerError):
            lexer.tokenize()
    
    def test_unterminated_comment(self):
        """Test error on unterminated comment."""
        lexer = Lexer('/* comment')
        with self.assertRaises(LexerError):
            lexer.tokenize()


class TestParser(unittest.TestCase):
    """Test cases for the parser."""
    
    def parse(self, source):
        """Helper to parse source code."""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        return parser.parse()
    
    def test_declaration(self):
        """Test variable declaration parsing."""
        ast = self.parse("int x = 10")
        self.assertEqual(len(ast.statements), 1)
        self.assertEqual(ast.statements[0].var_type, "int")
        self.assertEqual(ast.statements[0].name, "x")
    
    def test_function_declaration(self):
        """Test function declaration parsing."""
        ast = self.parse("function add(a, b) { return a }")
        self.assertEqual(len(ast.statements), 1)
        self.assertEqual(ast.statements[0].name, "add")
        self.assertEqual(ast.statements[0].parameters, ["a", "b"])
    
    def test_binary_expression(self):
        """Test binary expression parsing."""
        ast = self.parse("int x = 1 + 2 * 3")
        # Should respect precedence: 1 + (2 * 3)
        decl = ast.statements[0]
        self.assertEqual(decl.value.operator, "+")
    
    def test_if_statement(self):
        """Test if statement parsing."""
        ast = self.parse("if (true) { return 1 }")
        self.assertEqual(len(ast.statements), 1)
        self.assertIsNotNone(ast.statements[0].then_block)
        self.assertIsNone(ast.statements[0].else_block)
    
    def test_closure(self):
        """Test closure parsing."""
        ast = self.parse("var f = function(x) { return x }")
        self.assertEqual(len(ast.statements), 1)
        decl = ast.statements[0]
        self.assertEqual(decl.var_type, "var")
        self.assertIsNone(decl.value.name)
    
    def test_recursion(self):
        """Test recursion definition parsing."""
        ast = self.parse("var f = rec(n) => int { return n }")
        self.assertEqual(len(ast.statements), 1)
        decl = ast.statements[0]
        self.assertEqual(decl.value.keyword, "rec")
        self.assertEqual(decl.value.return_type, "int")


class TestInterpreter(unittest.TestCase):
    """Test cases for the interpreter."""
    
    def setUp(self):
        """Set up interpreter for each test."""
        self.interpreter = Interpreter()
    
    def test_int_declaration(self):
        """Test integer declaration."""
        result = self.interpreter.run("int x = 42")
        self.assertEqual(result, 42)
    
    def test_float_declaration(self):
        """Test float declaration."""
        result = self.interpreter.run("float pi = 3.14")
        self.assertAlmostEqual(result, 3.14)
    
    def test_string_declaration(self):
        """Test string declaration."""
        result = self.interpreter.run('string s = "hello"')
        self.assertEqual(result, "hello")
    
    def test_bool_declaration(self):
        """Test boolean declaration."""
        result = self.interpreter.run("bool b = true")
        self.assertTrue(result)
    
    def test_arithmetic(self):
        """Test arithmetic operations."""
        self.assertEqual(self.interpreter.run("int x = 10 + 5"), 15)
        self.assertEqual(self.interpreter.run("int x = 10 - 5"), 5)
        self.assertEqual(self.interpreter.run("int x = 10 * 5"), 50)
        self.assertEqual(self.interpreter.run("int x = 10 / 5"), 2.0)
    
    def test_comparison(self):
        """Test comparison operations."""
        self.assertTrue(self.interpreter.run("bool x = 10 == 10"))
        self.assertTrue(self.interpreter.run("bool x = 5 != 3"))
        self.assertTrue(self.interpreter.run("bool x = 3 < 5"))
        self.assertTrue(self.interpreter.run("bool x = 7 > 2"))
        self.assertTrue(self.interpreter.run("bool x = 5 <= 5"))
        self.assertTrue(self.interpreter.run("bool x = 5 >= 5"))
    
    def test_logical(self):
        """Test logical operations."""
        self.assertFalse(self.interpreter.run("bool x = true && false"))
        self.assertTrue(self.interpreter.run("bool x = true || false"))
        self.assertFalse(self.interpreter.run("bool x = !true"))
    
    def test_function_call(self):
        """Test function definition and call."""
        self.interpreter.run("function add(a, b) { return a + b }")
        result = self.interpreter.run("add(3, 4)")
        self.assertEqual(result, 7)
    
    def test_closure(self):
        """Test closure creation and call."""
        self.interpreter.run("var square = function(x) { return x * x }")
        result = self.interpreter.run("square(5)")
        self.assertEqual(result, 25)
    
    def test_recursive_closure(self):
        """Test recursive closure."""
        self.interpreter.run("""
            var factorial = function fact(n) {
                if (n <= 1) { return 1 }
                return n * fact(n - 1)
            }
        """)
        result = self.interpreter.run("factorial(5)")
        self.assertEqual(result, 120)
    
    def test_recursion_keyword(self):
        """Test recursion with rec keyword."""
        self.interpreter.run("""
            var fib = rec(n) => int {
                if (n <= 1) { return n }
                return fib(n - 1) + fib(n - 2)
            }
        """)
        result = self.interpreter.run("fib(10)")
        self.assertEqual(result, 55)
    
    def test_if_statement(self):
        """Test if statement execution."""
        result = self.interpreter.run("""
            if (5 > 3) {
                return "yes"
            }
        """)
        self.assertEqual(result, "yes")
    
    def test_complex_numbers(self):
        """Test complex number creation."""
        from lang.interpreter.types import Complex
        result = self.interpreter.run("complex z = 1.0+2.0i")
        self.assertIsInstance(result, Complex)
        self.assertEqual(result.real, 1.0)
        self.assertEqual(result.imag, 2.0)
    
    def test_matrices(self):
        """Test matrix creation."""
        from lang.interpreter.types import Matrix
        result = self.interpreter.run("matrix m = {{1, 2}, {3, 4}}")
        self.assertIsInstance(result, Matrix)
        self.assertEqual(result.num_rows, 2)
        self.assertEqual(result.num_cols, 2)
    
    def test_type_inference(self):
        """Test var type inference."""
        self.interpreter.run("var x = 42")
        self.interpreter.run("var y = 3.14")
        self.interpreter.run('var z = "hello"')
        
        # Check types via operations
        self.assertEqual(self.interpreter.run("x + 8"), 50)
        self.assertAlmostEqual(self.interpreter.run("y * 2"), 6.28)
    
    def test_builtin_functions(self):
        """Test built-in functions."""
        self.assertEqual(self.interpreter.run("sqrt(16)"), 4.0)
        self.assertEqual(self.interpreter.run("abs(-42)"), 42)
        self.assertEqual(self.interpreter.run("min(3, 1, 2)"), 1)
        self.assertEqual(self.interpreter.run("max(3, 1, 2)"), 3)
    
    def test_undefined_variable(self):
        """Test error on undefined variable."""
        with self.assertRaises(NameError):
            self.interpreter.run("x + 1")


class TestIntegration(unittest.TestCase):
    """Integration tests for complete programs."""
    
    def setUp(self):
        """Set up interpreter for each test."""
        self.interpreter = Interpreter()
    
    def test_factorial_program(self):
        """Test factorial program."""
        program = """
            function factorial(n) {
                if (n <= 1) { return 1 }
                return n * factorial(n - 1)
            }
            
            factorial(6)
        """
        result = self.interpreter.run(program)
        self.assertEqual(result, 720)
    
    def test_fibonacci_program(self):
        """Test Fibonacci program."""
        program = """
            var fib = rec(n) => int {
                if (n <= 1) { return n }
                return fib(n - 1) + fib(n - 2)
            }
            
            fib(12)
        """
        result = self.interpreter.run(program)
        self.assertEqual(result, 144)
    
    def test_higher_order_function(self):
        """Test higher-order function."""
        program = """
            function applyTwice(f, x) {
                return f(f(x))
            }
            
            var double = function(x) { return x * 2 }
            applyTwice(double, 3)
        """
        result = self.interpreter.run(program)
        self.assertEqual(result, 12)


if __name__ == '__main__':
    unittest.main()
