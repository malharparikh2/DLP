import sys

class LexicalAnalyzer:
    def __init__(self):
        self.keywords = {
            'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
            'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if',
            'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof', 'static',
            'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while'
        }
        
        self.operators = {
            '+', '-', '*', '/', '%', '=', '<', '>', '!', '&', '|', '^', '~',
            '+=', '-=', '*=', '/=', '%=', '==', '<=', '>=', '!=', '&&', '||',
            '>>=', '<<=', '++', '--'
        }
        
        self.punctuation = {'(', ')', '{', '}', '[', ']', ',', ';', '.'}  # Added '.' here
        self.symbol_table = set()
        self.lexical_errors = []
        self.current_pos = 0
        self.tokens = []  # Store all tokens for look-ahead
        self.line_no = 1

    def is_whitespace(self, char):
        return char in ' \t\n\r'
    
    def is_letter(self, char):
        return 'a' <= char.lower() <= 'z'
    
    def is_digit(self, char):
        return '0' <= char <= '9'
    
    def peek_next_non_whitespace(self, code):
        pos = self.current_pos + 1
        while pos < len(code) and self.is_whitespace(code[pos]):
            pos += 1
        return code[pos] if pos < len(code) else None

    def read_lexeme(self, code):
        lexeme = ''
        start_pos = self.current_pos
        
        # Read the entire lexeme
        while self.current_pos < len(code) and not self.is_whitespace(code[self.current_pos]) and \
              code[self.current_pos] not in self.operators and \
              code[self.current_pos] not in self.punctuation:
            lexeme += code[self.current_pos]
            self.current_pos += 1
        
        self.current_pos -= 1  # Move back one position as the main loop will increment
        
        # Check if it's a keyword
        if lexeme in self.keywords:
            return ('Keyword', lexeme)
        
        # Handle identifiers and invalid lexemes
        if lexeme:
            # Check if first character is letter or underscore
            if self.is_letter(lexeme[0]) or lexeme[0] == '_':
                # Check if all other characters are valid
                if all(self.is_letter(c) or self.is_digit(c) or c == '_' for c in lexeme[1:]):
                    # Check if it's followed by ( to identify function
                    next_char = self.peek_next_non_whitespace(code)
                    if next_char != '(':  # If not a function, add to symbol table
                        self.symbol_table.add(lexeme)
                    return ('Identifier', lexeme)
            
            # If starts with digit
            if self.is_digit(lexeme[0]):
                try:
                    float(lexeme)  # Check if it's a valid number
                    return ('Constant', lexeme)
                except ValueError:
                    pass
            
            # Invalid lexeme
            self.lexical_errors.append(lexeme)
            return None

        return None

    def read_character(self, code):
        char = "'"
        self.current_pos += 1  # Skip the opening quote
        
        while self.current_pos < len(code):
            current_char = code[self.current_pos]
            char += current_char
            
            if current_char == "'":
                break
            self.current_pos += 1
        
        return ('String', char)

    def read_string(self, code):
        string = '"'
        self.current_pos += 1  # Skip the opening quote
        
        while self.current_pos < len(code):
            char = code[self.current_pos]
            string += char
            
            if char == '"':
                break
            self.current_pos += 1
        
        return ('String', string)

    def read_operator(self, code):
        operator = code[self.current_pos]
        next_pos = self.current_pos + 1
        
        if next_pos < len(code):
            potential_operator = operator + code[next_pos]
            if potential_operator in self.operators:
                self.current_pos += 1
                return ('Operator', potential_operator)
        
        return ('Operator', operator)

    def skip_comment(self, code):
        if code[self.current_pos:self.current_pos + 2] == '//':
            while self.current_pos < len(code) and code[self.current_pos] != '\n':
                self.current_pos += 1
        elif code[self.current_pos:self.current_pos + 2] == '/*':
            self.current_pos += 2
            while self.current_pos < len(code) - 1:
                if code[self.current_pos:self.current_pos + 2] == '*/':
                    self.current_pos += 1
                    break
                if code[self.current_pos] == '\n':
                    self.line_no += 1
                self.current_pos += 1

    def tokenize(self, code):
        self.tokens = []  # Reset tokens
        self.current_pos = 0
        
        while self.current_pos < len(code):
            char = code[self.current_pos]
            
            # Handle whitespace
            if self.is_whitespace(char):
                if char == '\n':
                    self.line_no += 1
                self.current_pos += 1
                continue
            
            # Handle comments
            if (char == '/' and self.current_pos + 1 < len(code) and 
                code[self.current_pos + 1] in '/*'):
                self.skip_comment(code)
                self.current_pos += 1
                continue
            
            # Handle identifiers, keywords, and invalid lexemes
            if self.is_letter(char) or char == '_' or self.is_digit(char):
                token = self.read_lexeme(code)
                if token:
                    self.tokens.append(token)
            
            # Handle strings
            elif char == '"':
                token = self.read_string(code)
                self.tokens.append(token)
            
            # Handle character literals
            elif char == "'":
                token = self.read_character(code)
                self.tokens.append(token)
            
            # Handle operators
            elif char in self.operators:
                token = self.read_operator(code)
                self.tokens.append(token)
            
            # Handle punctuation (including dot operator)
            elif char in self.punctuation:
                self.tokens.append(('Punctuation', char))
            
            self.current_pos += 1
        
        return self.tokens

    def analyze(self, filename):
        try:
            with open(filename, 'r') as file:
                code = file.read()
            
            tokens = self.tokenize(code)
            
            # Print tokens
            print("TOKENS")
            for token_type, token_value in tokens:
                print(f"{token_type}: {token_value}")
            
            # Print lexical errors
            if self.lexical_errors:
                print("\nLEXICAL ERRORS")
                for error in self.lexical_errors:
                    print(f"{error} invalid lexeme")
            
            # Print symbol table
            print("\nSYMBOL TABLE ENTRIES")
            for idx, identifier in enumerate(sorted(self.symbol_table), 1):
                print(f"{idx}) {identifier}")
            
        except FileNotFoundError:
            print(f"Error: Could not open file '{filename}'")
            sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: python lexical_analyzer.py <input_file>")
        sys.exit(1)
    
    file = f"/workspaces/DLP-PRACTICALS/practical_3/testcases/{sys.argv[1]}"
    analyzer = LexicalAnalyzer()
    analyzer.analyze(file)

if __name__ == "__main__":
    main()
