from .tokens import TokenType, Token

class Node():

    def __str__(self):
        return f"{self.__class__.__name__}"


class Number(Node):
    def __init__(self, token: Token) -> None:
        super().__init__()
        self.token = token

    def __str__(self) -> str:
        return f"{super().__str__()}(<{self.token.type_}, {self.token.value}>)"


class BinOp(Node):

    def __init__(self, left: Node, op: Token, right: Node):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return f"BinOp{self.op.value}({self.left}, {self.right})"


class UnaryOp(Node):
    def __init__(self, op: Token, node: Node) -> None:
        super().__init__()
        self.op = op
        self.node = node

    def __str__(self) -> str:
        return f"UnaryOp{self.op.value}({self.node})"
