from tokens import *
from expr import *


class ParseError(Exception):
    pass


class Lexer:
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
                    Token(Op(Operator.from_s(curr)), range(self.idx, self.idx + 1)))
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


class ShuntingYard:
    def __init__(self, tokens: [Token]):
        self.tokens = tokens
        self.operator_stack = []
        self.ast_stack = []

    def into_ast(self) -> Expr:
        last_was_operator = True
        for token in self.tokens:
            if isinstance(token.kind, Num):
                last_was_operator = False
                self.ast_stack.append(Literal(token.kind.value))
            elif isinstance(token.kind, Op):
                if last_was_operator:
                    if token.kind.op == Operator.ADD:
                        token.kind = Operator.POS
                    elif token.kind.op == Operator.SUB:
                        token.kind.op = Operator.NEG
                    else:
                        raise ParseError(
                            f"Expected expression at pos: {token.pos}")
                last_was_operator = True
                while (self.operator_stack and not isinstance(self.operator_stack[-1], Paren)
                       and (self.operator_stack[-1].prec() > token.kind.op.prec() or (self.operator_stack[-1].prec() >= token.kind.op.prec()
                                                                                      and token.kind.op.is_left_assoc()))):
                    self.push_operation()
                self.operator_stack.append(token.kind.op)
            elif isinstance(token.kind, Paren):
                if token.kind.is_left:
                    last_was_operator = True
                    self.operator_stack.append(token.kind)
                else:
                    last_was_operator = False
                    while self.operator_stack:
                        last_op = self.operator_stack[-1]
                        if isinstance(last_op, Paren):
                            self.operator_stack.pop()
                            break
                        else:
                            self.push_operation()
                    else:
                        raise ParseError(
                            f"Mismatched parenthesis at range {token.pos}")
        for op in self.operator_stack[::-1]:
            if isinstance(op, Paren):
                raise ParseError(f"Unclosed parenthesis")
            self.push_operation(op)
        assert len(self.ast_stack) == 1
        return self.ast_stack[0]

    def push_operation(self, op=None):
        if op == None:
            op = self.operator_stack.pop()
        if op.is_binary():
            rhs = self.ast_stack.pop()
            lhs = self.ast_stack.pop()
            self.ast_stack.append(
                BinOp(op, lhs, rhs))
        else:
            value = self.ast_stack.pop()
            self.ast_stack.append(UnOp(op, value))


CODE = "--1 + (-2 * 3)"


def main():
    lexer = Lexer(CODE)
    tokens = lexer.tokenize()
    print(tokens)
    ast = ShuntingYard(tokens).into_ast()
    print(ast)
    print(ast.eval())


if __name__ == "__main__":
    main()
