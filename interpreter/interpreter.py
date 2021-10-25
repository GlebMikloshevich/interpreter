from .tokens import TokenType, Token


class InterpreterException(Exception):
    pass


class Interpreter:

    def __init__(self):
        self._pos: int = 0
        self._current_token: Token = None
        self._current_char: str = None
        self._text: str = None

    def _next_token(self) -> Token:
        if self._pos >= len(self._text):
            return Token(TokenType.EOS, None)  # ToDo fix None
        current_char: str = self._text[self._pos]
        if current_char.isdigit():
            self._pos += 1
            return Token(TokenType.INTEGER, current_char)

        if current_char == '+':
            self._pos += 1
            return Token(TokenType.PLUS, current_char)
        if current_char == '-':
            self._pos += 1
            return Token(TokenType.MINUS, current_char)
        raise InterpreterException(f"Bad token: {current_char}")

    def _check_token_type(self, type_: TokenType):
        if self._current_token.type_ == type_:
            self._current_token = self._next_token()
        else:
            raise InterpreterException(f"Invalid token order")

    def _expr(self):
        self._current_token = self._next_token()
        left = self._current_token
        self._check_token_type(TokenType.INTEGER)
        op = self._current_token

        if op.type_ == TokenType.PLUS:
            self._check_token_type(TokenType.PLUS)
        else:
            self._check_token_type(TokenType.MINUS)

        right = self._current_token


        self._check_token_type(TokenType.INTEGER)
        if op.type_ == TokenType.PLUS:
            return int(left.value) + int(right.value)

        if op.type_ == TokenType.MINUS:
            return int(left.value) - int(right.value)

        raise InterpreterException("bad operation")

    def __call__(self, text: str) -> int:
        return self.interpret(str)

    def interpret(self, text: str) -> int:
        self._text = text
        self._pos = 0
        return self._expr()

    def _forward(self):
        self._pos += 1
        if self._pos >= len(self._text):
            self._current_char = None
        else:
            self._current_char = self._text[self._pos]
