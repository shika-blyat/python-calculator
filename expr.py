from abc import ABC
from tokens import Operator
from operator import add, sub, truediv, mul


class Expr(ABC):
    def __repr__(self):
        return self.__str__()


class Literal(Expr):
    def __init__(self, value: int,):
        self.value = value

    def eval(self):
        return self.value

    def __str__(self):
        return str(self.value)


class BinOp(Expr):
    OP_MAP = {Operator.ADD: "+", Operator.SUB: "-",
              Operator.DIV: "/", Operator.MUL: "*"}
    OP_FUN_MAP = {Operator.ADD: add, Operator.SUB: sub,
                  Operator.DIV: truediv, Operator.MUL: mul}

    def __init__(self, op: Operator, lhs: Expr, rhs: Expr):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def eval(self):
        return self.OP_FUN_MAP[self.op](self.lhs.eval(), self.rhs.eval())

    def __str__(self):
        return f"({self.lhs} {self.OP_MAP[self.op]} {self.rhs})"

# BinOp(Operator.ADD, Literal(1), BinOp(Operator.MUL, Literal(2), Literal(3)))


"""
1 + (2 * 3)
1 2 3 * +
(1 + (2 * 3))

(+, 1, (*, 2, 3))

    +
   / \
  1   *
     / \
    2   3
"""
