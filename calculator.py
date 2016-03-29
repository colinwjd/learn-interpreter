#!/usr/bin/env python3

INTEGER, PLUS, MINUS, MUL, DIV, EOF = 'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'EOF'


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
            token_type=self.token_type,
            token_value=repr(self.token_value)
        )


class Lexer(object):

    def __init__(self, text):
        self.text = text
        self.current_token = None
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1
        if self.pos == len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def generate_number(self):
        number_queue = []
        while self.current_char is not None and self.current_char.isdigit():
            number_queue.append(self.current_char)
            self.advance()
        return int(''.join(number_queue))

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                number = self.generate_number()
                return Token(INTEGER, number)
            if self.current_char == '+':
                current_char = self.current_char
                self.advance()
                return Token(PLUS, current_char)
            if self.current_char == '-':
                current_char = self.current_char
                self.advance()
                return Token(MINUS, current_char)
            if self.current_char == '*':
                current_char = self.current_char
                self.advance()
                return Token(MUL, current_char)
            if self.current_char == '/':
                current_char = self.current_char
                self.advance()
                return Token(DIV, current_char)
            # cannot parsing input string
            self.error()
        return Token(EOF, None)


class Interperter(object):

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def walk(self, token_type):
        if self.current_token.token_type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        self.walk(INTEGER)
        return token.token_value

    def calc_expr(self):
        result = self.factor()

        while self.current_token.token_type in (MUL, DIV):
            if self.current_token.token_type == MUL:
                self.walk(MUL)
                result *= self.factor()
            elif self.current_token.token_type == DIV:
                self.walk(DIV)
                result /= self.factor()
            else:
                self.error()
        return result


def main():
    while True:
        try:
            text = input('calc>>>')
        except EOFError:
            break

        if text:
            lexer = Lexer(text)
            interperter = Interperter(lexer)
            result = interperter.calc_expr()
            print(result)

if __name__ == '__main__':
    main()
