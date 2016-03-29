#!/usr/bin/env python3

import logging;logging.basicConfig(level=logging.DEBUG)

INTEGER, MUL, DIV, EOF = 'INTEGER', 'MUL', 'DIV', 'EOF'

class Token(object):

    def __init__(self, token_type, token_value):
        self.token_type = token_type
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


# 词法分析器
class Lexer(object):

    def __init__(self, text):
        self.text = text
        self.current_token = None
        self.index = 0
        self.current_char = self.text[self.index]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.index += 1
        if self.index == len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.index]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def generate_number(self):
        result = []
        while self.current_char is not None and self.current_char.isdigit():
            result.append(self.current_char)
            self.advance()
        return int(''.join(result))

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                number = self.generate_number()
                return Token(INTEGER, number)
            if self.current_char == '*':
                current_char = self.current_char
                self.advance()
                return Token(MUL, current_char)
            if self.current_char == '/':
                current_char = self.current_char
                self.advance()
                return Token(DIV, current_char)
            self.error()
        return Token(EOF, None)


class Parser(object):

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def error(self):
        raise Exception('Invalid syntax')

    def walk(self, token_type):
        token = self.current_token
        logging.info(token)
        if token.token_type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()       

    def factor(self):
        self.walk(INTEGER)
        
    def expr(self):
        self.factor()
        while self.current_token.token_type in (MUL, DIV):
            if self.current_token.token_type == MUL:
                self.walk(MUL)
                self.factor()
            elif self.current_token.token_type == DIV:
                self.walk(DIV)
                self.factor()
            else:
                self.error()

    def parse(self):
        self.expr()


def main():
    while True:
        try:
            text = input('expr>>>')
        except EOFError:
            break

        if text:
            lexer = Lexer(text)
            parser = Parser(lexer)
            parser.parse()

if __name__ == '__main__':
    main()

