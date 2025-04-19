import re

class ConstantFolder:
    def __init__(self):
        pass
    
    def is_constant(self, token):
        """Check if a token is a constant (number)"""
        return re.match(r'^-?\d+\.?\d*$', token) is not None
    
    def evaluate(self, op, left, right):
        """Evaluate a constant expression"""
        left = float(left) if '.' in left else int(left)
        right = float(right) if '.' in right else int(right)
        
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right
        else:
            raise ValueError(f"Unknown operator: {op}")
    
    def fold_constants(self, expression):
        """Main function to perform constant folding"""
        # Tokenize the expression
        tokens = re.findall(r'([a-zA-Z_]\w*|-?\d+\.?\d*|[\+\-\*/\(\)])', expression)
        
        i = 0
        while i < len(tokens) - 2:
            left, op, right = tokens[i], tokens[i+1], tokens[i+2]
            
            # Check if we have a constant expression
            if (op in '+-*/' and 
                self.is_constant(left) and 
                self.is_constant(right) and
                not (i > 0 and tokens[i-1] == '(') and
                not (i+3 < len(tokens) and tokens[i+3] == ')')):
                
                try:
                    # Evaluate the constant expression
                    result = self.evaluate(op, left, right)
                    # Replace the three tokens with the result
                    tokens[i:i+3] = [str(result)]
                    # Move back in case we can fold more constants
                    i = max(0, i - 2)
                except:
                    i += 1
            else:
                i += 1
        
        # Reconstruct the optimized expression
        optimized = ''.join(tokens)
        return optimized

def optimize_expression(expression):
    folder = ConstantFolder()
    optimized = folder.fold_constants(expression)
    return optimized

# Test the optimizer
if __name__ == "__main__":
    expression = input("Enter an arithmetic expression: ")
    optimized = optimize_expression(expression)
    print("Optimized expression:", optimized)
