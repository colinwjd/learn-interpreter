#!/usr/bin/env python3

INTEGER, PLUS, EOF = 'INTEGER', 'PLUS', 'EOF'

class Token(object):
    
    def __init__(self, token_type, token_value):
        # token type: INTEGER, PLUS, EOF
        self.token_type = token_type
        # token value: 0~9 and '+' or None
        self.token_value = token_value

    def __str__(self):
        '''
        String representation of the class instance.
        Example:
            Token(PLUS, '+')
            Token(INTEGER, 7)
        '''
        return 'Token({token_type}, {token_value})'.format(
            token_type = self.token_type,
            token_value = repr(self.token_value)
        )

class Interperter(object):
    
    def __init__(self, text):
        # string input. e.g. "6+7"
        self.text = text
        # pointer index to self.text
        self.pos = 0
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input string')

    def get_next_token(self):
        text = self.text
        if self.pos == len(text):
            return Token(EOF, None)

        current_char = text[self.pos]
        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token
        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token
        # cannot parsing input string
        self.error()

    def walk(self, token_type):
        if self.current_token.token_type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def calc_expr(self):
        '''
        expression: INTEGER PLUS INTEGER
        '''
        self.current_token = self.get_next_token()

        left = self.current_token
        self.walk(INTEGER)

        operator = self.current_token
        self.walk(PLUS)

        right = self.current_token
        self.walk(INTEGER)

        result = left.token_value + right.token_value
        return result

def main():
    while True:
        try:
            text = input('calc>>>')
        except EOFError:
            break

        if text:
            interperter = Interperter(text)
            result = interperter.calc_expr()
            print(result)

if __name__ == '__main__':
    main()

