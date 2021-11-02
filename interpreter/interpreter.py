from .tokens import TokenType, Token
from .lexer import Lexer


class InterpreterException(Exception):
    pass


class Interpreter:

    def __init__(self):
        self._current_token: Token = None
        self._lexer = Lexer()

    def __call__(self, text: str):
        self.interpret(text)

    def _check_token_type(self, type_: TokenType):
        if self._current_token.type_ == type_:
            self._current_token = self._lexer.next_token()
        else:
            raise InterpreterException('invalid token order')

    def _expr(self) -> float:
        self._current_token = self._lexer.next_token()
        left = self._current_token
        if left.type_ == TokenType.FLOAT:
            self._check_token_type(TokenType.FLOAT)
        else:
            self._check_token_type(TokenType.FLOAT)

        op = self._current_token
        if op.type_ == TokenType.PLUS:
            self._check_token_type(TokenType.PLUS)
        else:
            self._check_token_type(TokenType.MINUS)
        right = self._current_token
        if right.type_ == TokenType.FLOAT:
            self._check_token_type(TokenType.FLOAT)
        else:
            self._check_token_type(TokenType.FLOAT)

        if op.type_ == TokenType.PLUS:
            return float(left.value) + float(right.value)
        elif op.type_ == TokenType.MINUS:
            return float(left.value) - float(right.value)

        raise InterpreterException('bad operation')

    def interpret(self, text: str):
        self._lexer.init(text)
        return self._expr()

