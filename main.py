from tokens import *
from expr import *


class ParseError(Exception):
    pass


class Lexer:
    OP_MAP = {"+": Operator.ADD, "-": Operator.SUB,
              "/": Operator.DIV, "*": Operator.MUL}

    def __init__(self, code):
        self.code = code
        self.idx = 0

    def tokenize(self) -> [Token]:
        result_tokens = []
        while not self.is_at_end():
            curr = self.curr()
            if curr.isdigit():
                num = []
                while not self.is_at_end() and curr.isdigit():
                    num.append(curr)
                    try:
                        curr = self.next()
                    except IndexError:
                        break
                idx = self.idx
                result_tokens.append(
                    Token(Num(int("".join(num))), range(idx - len(num), idx)))
            elif curr in ("(", ")"):
                result_tokens.append(
                    Token(Paren(curr == "("), range(self.idx, self.idx + 1)))
                self.advance()
            elif curr in ("+", "-", "*", "/"):
                result_tokens.append(
                    Token(Op(self.OP_MAP[curr]), range(self.idx, self.idx + 1)))
                self.advance()
            elif curr.isspace():
                self.advance()
                pass
            else:
                raise ParseError(f"Unknown char {curr}")
        return result_tokens

    def next(self) -> str:
        self.advance()
        return self.curr()

    def advance(self):
        self.idx += 1

    def curr(self) -> str:
        return self.code[self.idx]

    def is_at_end(self) -> bool:
        return self.idx >= len(self.code)

#  1 + 2 * 3


PRIORITY_MAP = {Operator.ADD: 5, Operator.SUB: 5,
                Operator.MUL: 10, Operator.DIV: 10}


def shunting_yard(tokens: [Token]) -> Expr:
    operator_stack = []
    ast_stack = []
    for token in tokens:
        if isinstance(token.kind, Num):
            ast_stack.append(Literal(token.kind.value))
        elif isinstance(token.kind, Op):
            while operator_stack:
                if not(operator_stack[-1], Paren) and PRIORITY_MAP[operator_stack[-1]] >= PRIORITY_MAP[token.kind.op]:
                    rhs = ast_stack.pop()
                    lhs = ast_stack.pop()
                    ast_stack.append(BinOp(operator_stack.pop(), lhs, rhs))
                else:
                    break
            operator_stack.append(token.kind.op)
        elif isinstance(token.kind, Paren):
            if token.kind.is_left:
                operator_stack.append(token.kind)
            else:
                while operator_stack:
                    last_op = operator_stack.pop()
                    if isinstance(last_op, Paren) and last_op.is_left:
                        break
                    else:
                        rhs = ast_stack.pop()
                        lhs = ast_stack.pop()
                        ast_stack.append(BinOp(last_op, lhs, rhs))
                else:
                    raise ParseError(
                        f"Mismatched parenthesis at range {token.pos}")

    for op in operator_stack[::-1]:
        if isinstance(op, Paren):
            raise ParseError(f"Unclosed parenthesis")
        rhs = ast_stack.pop()
        lhs = ast_stack.pop()
        ast_stack.append(BinOp(op, lhs, rhs))
    return ast_stack[0]


CODE = "1 + 2) * 3"


def main():
    lexer = Lexer(CODE)
    tokens = lexer.tokenize()
    print(tokens)
    ast = shunting_yard(tokens)
    print(ast)
    print(ast.eval())


if __name__ == "__main__":
    main()
