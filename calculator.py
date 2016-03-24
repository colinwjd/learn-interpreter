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
            token_type = self.token_type,
            token_value = repr(self.token_value)
        )

class Interperter(object):
    
    def __init__(self, text):
        # string input. e.g. "6+7"
        self.text = text.strip()
        # pointer index to self.text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Error parsing input string')

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

    # 词法分析，获取Token
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
                self.advance()
                return Token(PLUS, self.current_char)
            if self.current_char == '-':
                self.advance()
                return Token(MINUS, self.current_char)
            if self.current_char == '*':
                self.advance()
                return Token(MUL, self.current_char)
            if self.current_char == '/':
                self.advance()
                return Token(DIV, self.current_char)
            # cannot parsing input string
            self.error()
        return Token(EOF, None)

    def walk(self, token_type):
        if self.current_token.token_type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def calc_expr(self):
        '''
        expression: e.g. INTEGER PLUS INTEGER
        '''
        # 语法分析parsing，识别Token流中的短语
        self.current_token = self.get_next_token()

        left = self.current_token
        self.walk(INTEGER)

        operator = self.current_token
        if operator.token_type == PLUS:
            self.walk(PLUS)
        elif operator.token_type == MINUS:
            self.walk(MINUS)
        elif operator.token_type == MUL:
            self.walk(MUL)
        elif operator.token_type == DIV:
            self.walk(DIV)
        else:
            self.error()

        right = self.current_token
        self.walk(INTEGER)

        # 解释interpreting，完成语法分析后进行解释
        if operator.token_type == PLUS:
            result = left.token_value + right.token_value
        elif operator.token_type == MINUS:
            result = left.token_value - right.token_value
        elif operator.token_type == MUL:
            result = left.token_value * right.token_value
        elif operator.token_type == DIV:
            result = left.token_value / right.token_value
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

