from abc import ABC
from enum import IntEnum


class Operator(IntEnum):
    ADD = 0
    SUB = 1
    DIV = 2
    MUL = 3


class TokKind(ABC):
    def __repr__(self):
        return self.__str__()


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
    OP_MAP = {Operator.ADD: "+", Operator.SUB: "-",
              Operator.DIV: "/", Operator.MUL: "*"}

    def __init__(self, op: Operator):
        self.op = op

    def __str__(self) -> str:
        return self.OP_MAP[self.op]


class Token:
    def __init__(self, kind: TokKind, pos: range):
        self.kind = kind
        self.pos = pos

    def __str__(self):
        return f"(kind: {self.kind}, pos: {self.pos}"

    def __repr__(self):
        return self.__str__()
