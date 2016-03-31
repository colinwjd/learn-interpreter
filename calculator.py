#!/usr/bin/env python3
from parser import INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF
from parser import Lexer
from parser import Parser

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
        if token.token_type == INTEGER:
            self.walk(INTEGER)
            return token.token_value
        elif token.token_type == LPAREN:
            self.walk(LPAREN)
            middle_result = self.expr()
            self.walk(RPAREN)
            return middle_result

    def term(self):
        result = self.factor()

        while self.current_token.token_type in (MUL, DIV):
            if self.current_token.token_type == MUL:
                self.walk(MUL)
                result *= self.factor()
            elif self.current_token.token_type == DIV:
                self.walk(DIV)
                result /= self.factor()
        return result

    def expr(self):
        result = self.term()
        while self.current_token.token_type in (PLUS, MINUS):
            if self.current_token.token_type == PLUS:
                self.walk(PLUS)
                result += self.term()
            elif self.current_token.token_type == MINUS:
                self.walk(MINUS)
                result -= self.term()
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
            result = interperter.expr()
            print(result)

if __name__ == '__main__':
    main()
