#!/usr/bin/env python3

import logging;logging.basicConfig(level=logging.DEBUG)

INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF = ('INTEGER', 'PLUS', 'MINUS', 
        'MUL', 'DIV', 'LPAREN', 'RPAREN', 'EOF')

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


class Lexer(object):
    '''
    Get each token one by one from the input text.
    If there are characters not allowed, it shoud raise lexer exception.
    '''

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
            if self.current_char == '(':
                current_char = self.current_char
                self.advance()
                return Token(LPAREN, '(')
            if self.current_char == ')':
                current_char = self.current_char
                self.advance()
                return Token(RPAREN, ')')
            # cannot parsing input string
            self.error()
        return Token(EOF, None)


# Represent for a AST node
class AbstractSyntaxTree(object):
    pass


# Represent for a binary operator e.g. 1+2, 3-1, 3*3, 8/2
class BinaryOperator(AbstractSyntaxTree):

    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class UnaryOperator(AbstractSyntaxTree):

    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class Number(AbstractSyntaxTree):
    
    def __init__(self, token):
        self.token = token
        self.value = token.token_value


# A recursive-descent parser is a top-down parser that uses 
# a set of recursive procedures to process the input.
# Top-down reflects the fact that the parser begins by 
# constructing the top node of the parse tree and then gradually constructs lower nodes.
class Parser(object):
    '''
    I think it's actually a procedure for constructing an abstract syntax tree.
    If something is wrong, it shoud raise an syntax exception.
    '''

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def error(self):
        raise Exception('Invalid syntax')

    # Check token type, if passed, set the current token to next token
    # if not pass, throw an error
    def walk(self, token_type):
        token = self.current_token
        logging.info(token)
        if token.token_type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()       

    def factor(self):
        '''
        factor: (PLUS | MINUS) factor | INTEGER | LPAREN expr RPAREN
        '''
        token = self.current_token
        if token.token_type == PLUS:
            self.walk(PLUS)
            node = UnaryOperator(token, self.factor())
            return node
        elif token.token_type == MINUS:
            self.walk(MINUS)
            node = UnaryOperator(token, self.factor())
            return node
        elif token.token_type == INTEGER:
            self.walk(INTEGER)
            return Number(token)
        elif token.token_type == LPAREN:
            self.walk(LPAREN)
            node = self.expr()
            self.walk(RPAREN)
            return node

    def term(self):
        '''
        term: factor ((MUL | DIV) factor)*
        '''
        node = self.factor()
        while self.current_token.token_type in (MUL, DIV):
            token = self.current_token
            if token.token_type == MUL:
                self.walk(MUL)
            elif token.token_type == DIV:
                self.walk(DIV)
            node = BinaryOperator(left=node, op=token, right=self.factor())
        return node
        
    def expr(self):
        '''
        expr: term ((PLUS | MINUS) term)*
        term: factor ((MUL | DIV) factor)*
        factor: (PLUS | MINUS) factor | INTEGER | LPAREN expr RPAREN
        '''
        node = self.term()
        while self.current_token.token_type in (PLUS, MINUS):
            token = self.current_token
            if token.token_type == PLUS:
                self.walk(PLUS)
            elif token.token_type == MINUS:
                self.walk(MINUS)
            node = BinaryOperator(left=node, op=token, right=self.term())
        return node

    def parse(self):
        return self.expr()


# Visitor pattern, each node has its own visit logic
# Like an Interface in Java
class NodeVisitor(object):
    
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


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

