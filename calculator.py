#!/usr/bin/env python3

INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'

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

    def error(self):
        raise Exception('Error parsing input string')

    # 词法分析，获取Token
    def get_next_token(self):
        text = self.text
        # 读到最后一个字符结束
        if self.pos == len(text):
            return Token(EOF, None)

        current_char = text[self.pos]

        # 处理表达式内部出现的空格
        if current_char == ' ':
            for current_char in text[self.pos:]:
                if current_char == ' ':
                    self.pos += 1
                else:
                    current_char = text[self.pos]
                    break

        if current_char.isdigit():
            # 支持多位整型数字
            number_queue = []
            for current_char in text[self.pos:]:
                if current_char.isdigit():
                    number_queue.append(current_char)
                    self.pos += 1
                else:
                    break
            number = int(''.join(number_queue))

            token = Token(INTEGER, number)
            return token

        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

        if current_char == '-':
            token = Token(MINUS, current_char)
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
        expression: e.g. INTEGER PLUS INTEGER
        '''
        self.current_token = self.get_next_token()

        left = self.current_token
        self.walk(INTEGER)

        operator = self.current_token
        if operator.token_type == PLUS:
            self.walk(PLUS)
        elif operator.token_type == MINUS:
            self.walk(MINUS)

        right = self.current_token
        self.walk(INTEGER)

        if operator.token_type == PLUS:
            result = left.token_value + right.token_value
        elif operator.token_type == MINUS:
            result = left.token_value - right.token_value
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

