import re

class QuadrupleGenerator:
    def __init__(self):
        self.quadruples = []
        self.temp_count = 0
    
    def new_temp(self):
        temp = f't{self.temp_count}'
        self.temp_count += 1
        return temp
    
    def add_quadruple(self, op, arg1, arg2=None, result=None):
        self.quadruples.append({
            'operator': op,
            'operand1': arg1,
            'operand2': arg2,
            'result': result
        })
        return result
    
    def print_quadruples(self):
        print("{:<10} {:<10} {:<10} {:<10}".format(
            'Operator', 'Operand1', 'Operand2', 'Result'))
        for quad in self.quadruples:
            print("{:<10} {:<10} {:<10} {:<10}".format(
                quad['operator'],
                str(quad['operand1']),
                str(quad['operand2']) if quad['operand2'] is not None else '',
                str(quad['result']) if quad['result'] is not None else ''))

class Parser:
    def __init__(self, expression):
        self.tokens = self.tokenize(expression)
        self.current_token = None
        self.token_index = -1
        self.advance()
        self.quad_gen = QuadrupleGenerator()
    
    def tokenize(self, expression):
        # Tokenize the input expression
        token_pattern = r'\d+\.?\d*|[\+\-\*/\(\)]'
        tokens = re.findall(token_pattern, expression)
        return tokens
    
    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None
    
    def eat(self, expected):
        if self.current_token == expected:
            self.advance()
        else:
            raise SyntaxError(f"Expected '{expected}', got '{self.current_token}'")
    
    def factor(self):
        token = self.current_token
        if token == '(':
            self.eat('(')
            result = self.expr()
            self.eat(')')
            return result
        else:
            # It's a number
            self.advance()
            return token
    
    def term(self):
        result = self.factor()
        
        while self.current_token in ('*', '/'):
            op = self.current_token
            self.advance()
            right = self.factor()
            temp = self.quad_gen.new_temp()
            self.quad_gen.add_quadruple(op, result, right, temp)
            result = temp
        
        return result
    
    def expr(self):
        result = self.term()
        
        while self.current_token in ('+', '-'):
            op = self.current_token
            self.advance()
            right = self.term()
            temp = self.quad_gen.new_temp()
            self.quad_gen.add_quadruple(op, result, right, temp)
            result = temp
        
        return result
    
    def parse(self):
        try:
            result = self.expr()
            if self.current_token is not None:
                raise SyntaxError("Unexpected tokens at end of expression")
            # Add final assignment if needed
            if len(self.quad_gen.quadruples) > 0:
                last_quad = self.quad_gen.quadruples[-1]
                if last_quad['result'] == result:
                    # No need for additional assignment
                    pass
            return self.quad_gen
        except SyntaxError as e:
            print(f"Syntax error: {e}")
            return None

def generate_quadruples(expression):
    # Remove all whitespace from the expression
    expression = re.sub(r'\s+', '', expression)
    
    parser = Parser(expression)
    quad_gen = parser.parse()
    
    if quad_gen:
        quad_gen.print_quadruples()
    else:
        print("Invalid expression")

# Test the generator
if __name__ == "__main__":
    expression = input("Enter an arithmetic expression: ")
    generate_quadruples(expression)
