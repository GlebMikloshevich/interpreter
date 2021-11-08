from enum import Enum, auto


class TokenType(Enum):
    INTEGER = auto()
    FLOAT = auto()
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    EOS = auto()
    POW = auto()

    LPAREN = auto()
    RPAREN = auto()


class Token:

    def __init__(self, type_: TokenType, value: str):
        self.type_ = type_
        self.value = value

    def __str__(self):
        return f"Token({self.type_}, {self.value})"

    def __repr__(self):
        return str(self)


if __name__ == "__main__":
    print(list(TokenType))
    t = Token(TokenType.INTEGER, "2")
    print(t)
    print([t])
