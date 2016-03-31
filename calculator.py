#!/usr/bin/env python3

from parser import PLUS, MINUS, MUL, DIV
from parser import NodeVisitor
from parser import Lexer
from parser import Parser

class Interperter(NodeVisitor):

    def __init__(self, parser):
        self.parser = parser

    # BinaryOperator node visit logic
    def visit_BinaryOperator(self, node):
        if node.op.token_type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.token_type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.token_type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.token_type == DIV:
            return self.visit(node.left) / self.visit(node.right)

    # UnaryOperator node visit logic
    def visit_UnaryOperator(self, node):
        if node.op.token_type == PLUS:
            return self.visit(node.expr)
        elif node.op.token_type == MINUS:
            return -self.visit(node.expr)

    # Number node visit logic
    def visit_Number(self, node):
        return node.value

    def interpret(self):
        tree_root = self.parser.parse()
        return self.visit(tree_root)
        

def main():

    while True:
        try:
            text = input('calc>>>')
        except EOFError:
            break

        if text:
            lexer = Lexer(text)
            parser = Parser(lexer)
            interperter = Interperter(parser)
            result = interperter.interpret()
            print(result)

if __name__ == '__main__':
    main()
