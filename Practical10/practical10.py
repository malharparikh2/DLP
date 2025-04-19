import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
    
    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None
    
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def number(self):
        result = ''
        decimal_found = False
        
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if decimal_found:
                    raise Exception("Invalid number with multiple decimal points")
                decimal_found = True
            result += self.current_char
            self.advance()
        
        if decimal_found and len(result.split('.')[1]) == 0:
            raise Exception("Invalid number ending with decimal point")
            
        return float(result) if decimal_found else int(result)
    
    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char.isdigit() or self.current_char == '.':
                return Token('NUMBER', self.number())
            
            if self.current_char == '+':
                self.advance()
                return Token('PLUS', '+')
            
            if self.current_char == '-':
                self.advance()
                return Token('MINUS', '-')
            
            if self.current_char == '*':
                self.advance()
                return Token('MUL', '*')
            
            if self.current_char == '/':
                self.advance()
                return Token('DIV', '/')
            
            if self.current_char == '^':
                self.advance()
                return Token('POW', '^')
            
            if self.current_char == '(':
                self.advance()
                return Token('LPAREN', '(')
            
            if self.current_char == ')':
                self.advance()
                return Token('RPAREN', ')')
            
            raise Exception(f"Invalid character: {self.current_char}")
        
        return Token('EOF', None)

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception(f"Syntax error: expected {token_type}, got {self.current_token.type}")
    
    def factor(self):
        token = self.current_token
        
        if token.type == 'LPAREN':
            self.eat('LPAREN')
            result = self.expr()
            self.eat('RPAREN')
            return result
        elif token.type == 'NUMBER':
            self.eat('NUMBER')
            return token.value
        else:
            raise Exception("Invalid syntax in factor")
    
    def term(self):
        result = self.factor()
        
        while self.current_token.type in ('MUL', 'DIV'):
            token = self.current_token
            if token.type == 'MUL':
                self.eat('MUL')
                result *= self.factor()
            elif token.type == 'DIV':
                self.eat('DIV')
                denominator = self.factor()
                if denominator == 0:
                    raise Exception("Division by zero")
                result /= denominator
        
        return result
    
    def expr(self):
        result = self.term()
        
        while self.current_token.type in ('PLUS', 'MINUS'):
            token = self.current_token
            if token.type == 'PLUS':
                self.eat('PLUS')
                result += self.term()
            elif token.type == 'MINUS':
                self.eat('MINUS')
                result -= self.term()
        
        return result
    
    def power(self):
        result = self.factor()
        
        while self.current_token.type == 'POW':
            self.eat('POW')
            result **= self.factor()
        
        return result
    
    def parse(self):
        # We need to handle operator precedence properly
        # The original grammar had exponentiation at higher precedence than * and /
        # So we'll modify the parsing approach to match that
        
        # First parse all expressions with + and -
        result = self.expr()
        
        # Check if we've consumed all tokens
        if self.current_token.type != 'EOF':
            raise Exception("Unexpected tokens at end of expression")
        
        return result

def evaluate_expression(expression):
    try:
        # Clean the input string
        expression = expression.strip()
        if not expression:
            return "Invalid expression"
        
        # Validate the expression contains only allowed characters
        if not re.match(r'^[\d\s+\-*/^().]+$', expression):
            return "Invalid expression"
        
        lexer = Lexer(expression)
        parser = Parser(lexer)
        result = parser.parse()
        return result
    except Exception as e:
        return "Invalid expression"

# Test the evaluator
if __name__ == "__main__":
    expression = input("Enter an arithmetic expression: ")
    result = evaluate_expression(expression)
    print(result)
