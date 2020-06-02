from abc import ABC
from enum import IntEnum
from operator import add, sub, truediv, mul, neg, pos


class Operator(IntEnum):
    ADD = 0
    SUB = 1
    DIV = 2
    MUL = 3
    POS = 4
    NEG = 5

    def is_binary(self) -> bool:
        return not self in (Operator.POS, Operator.NEG)

    def is_left_assoc(self) -> bool:
        return not self in (Operator.POS, Operator.NEG)

    def prec(self) -> int:
        PRIORITY_MAP = {self.ADD: 5, self.SUB: 5, self.MUL: 10,
                        self.DIV: 10, self.NEG: 15, self.POS: 15}
        return PRIORITY_MAP[self]

    @classmethod
    def from_s(cls, s: str):
        OP_MAP = {"+": Operator.ADD, "-": Operator.SUB,
                  "/": Operator.DIV, "*": Operator.MUL}
        return OP_MAP[s]

    def as_func(self):
        OP_FUN_MAP = {Operator.ADD: add, Operator.SUB: sub,
                      Operator.DIV: truediv, Operator.MUL: mul,
                      Operator.POS: pos, Operator.NEG: neg}
        return OP_FUN_MAP[self]

    def __str__(self):
        OP_MAP = {Operator.ADD: "+", Operator.SUB: "-",
                  Operator.DIV: "/", Operator.MUL: "*", Operator.NEG: "-", Operator.POS: "+"}
        return OP_MAP[self]

    def __repr__(self):
        return str(self)


class TokKind(ABC):
    def __repr__(self):
        return str(self)


class Num(TokKind):
    def __init__(self, value: int):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Paren(TokKind):
    def __init__(self, is_left: bool):
        self.is_left = is_left

    def __str__(self) -> str:
        return "(" if self.is_left else ")"


class Op(TokKind):

    def __init__(self, op: Operator):
        self.op = op

    def __str__(self) -> str:
        return str(self.op)


class Token:
    def __init__(self, kind: TokKind, pos: range):
        self.kind = kind
        self.pos = pos

    def __str__(self):
        return f"(kind: {self.kind}, pos: {self.pos}"

    def __repr__(self):
        return str(self)
