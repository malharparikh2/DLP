class RecursiveDescentParser:
    def __init__(self, input_string):
        self.input = input_string
        self.pos = 0

    def current_char(self):
        if self.pos < len(self.input):
            return self.input[self.pos]
        return None

    def eat(self, char):
        """Consume the current character if it matches the expected char."""
        if self.current_char() == char:
            self.pos += 1
        else:
            return False
        return True

    def parse_S(self):
        """S → ( L ) | a"""
        if self.current_char() == '(':
            self.pos += 1
            if not self.parse_L():
                return False
            if not self.eat(')'):
                return False
            return True
        elif self.current_char() == 'a':
            self.pos += 1
            return True
        return False

    def parse_L(self):
        """L → S L'"""
        if not self.parse_S():
            return False
        return self.parse_L_prime()

    def parse_L_prime(self):
        """L' → , S L' | ε"""
        if self.current_char() == ',':
            self.pos += 1
            if not self.parse_S():
                return False
            return self.parse_L_prime()
        return True

    def parse(self):
        """Start parsing the input string"""
        result = self.parse_S()
        # We should consume all the input by the end of the parse.
        if result and self.pos == len(self.input):
            return "Valid string"
        return "Invalid string"


def main():
    input_string = input("Enter the string to validate: ").strip()
    parser = RecursiveDescentParser(input_string)
    result = parser.parse()
    print(result)


if __name__ == "__main__":
    main()
