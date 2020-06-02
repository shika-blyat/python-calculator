from abc import ABC
from tokens import Operator


class Expr(ABC):
    def __repr__(self):
        return str(self)


class Literal(Expr):
    def __init__(self, value: int,):
        self.value = value

    def eval(self):
        return self.value

    def __str__(self):
        return str(self.value)


class BinOp(Expr):

    def __init__(self, op: Operator, lhs: Expr, rhs: Expr):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def eval(self):
        return self.op.as_func()(self.lhs.eval(), self.rhs.eval())

    def __str__(self):
        return f"({self.lhs} {self.op} {self.rhs})"


class UnOp(Expr):

    def __init__(self, op: Operator, value: Expr):
        self.op = op
        self.value = value

    def eval(self):
        return self.op.as_func()(self.value.eval())

    def __str__(self):
        return f"({self.op} {self.value})"
