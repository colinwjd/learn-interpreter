#!/usr/bin/env python3
from parser import NodeVisitor
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

    # Number node visit logic
    def visit_Number(self, node):
        return node.value
        

def main():
    while True:
        try:
            text = input('calc>>>')
        except EOFError:
            break

        if text:
            parser = Parser(text)
            interperter = Interperter(parser)

if __name__ == '__main__':
    main()
