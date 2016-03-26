#!/usr/bin/env python3

INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(type = self.type, value = repr(self.value))

class Interperter(object):
    def __init__(self, text):
        self.text = text
        self.current_token = None
        self.index = 0
        self.current_char = self.text[self.index]

    def error(self):
        raise Exception('Syntax Error.')
        

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
        text = self.text
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
            self.error()
        return Token(EOF, None)
            
    def walk(self, type):
        token = self.current_token
        if token.type == type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def term(self):
        token = self.current_token
        self.walk(INTEGER)
        return token.value

    def calc_expr(self):
        # init the first token
        self.current_token = self.get_next_token()
        result = self.term()
        while self.current_token.type in (PLUS, MINUS):
            if self.current_token.type == PLUS:
                self.walk(PLUS)
                result = result + self.term()
            if self.current_token.type == MINUS:
                self.walk(MINUS)
                result = result - self.term()
        return result

def main():
    while True:
        try:
            # 获取输入
            text = input('calc>>>')
        except EOFError:
            break

        if text:
            # 解释text
            interperter = Interperter(text)
            result = interperter.calc_expr()
            print(result)

if __name__ == '__main__':
    main()
