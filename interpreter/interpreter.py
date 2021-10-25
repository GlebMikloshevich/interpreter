from .tokens import TokenType, Token


class InterpreterException(Exception):
    pass


class Interpreter:

    def __init__(self):
        self._pos: int = -1
        self._current_token: Token = None
        self._current_char: str = None
        self._text: str = None

    def __call__(self, text: str):
        self.interpret(text)

    def interpret(self, text: str):
        self._text = text
        self._pos = -1
        self._forward()
        return self._expr()

    def _forward(self):
        self._pos += 1
        if self._pos >= len(self._text):
            self._current_char = None
        else:
            self._current_char = self._text[self._pos]

    def _skip(self):
        while self._current_char and self._current_char == ' ':
            self._forward()

    def _number(self):
        result: list = []
        while self._current_char and self._current_char.isdigit():
            result.append(self._current_char)
            self._forward()

        if self._current_char and self._current_char == '.':
            result.append('.')
            self._forward()
            if self._current_char and self._current_char.isdigit():
                while self._current_char and self._current_char.isdigit():
                    result.append(self._current_char)
                    self._forward()
            else:
                raise InterpreterException('invalid number')

        return ''.join(result)

    def _next_token(self) -> Token:
        while self._current_char is not None:
            if self._current_char == ' ':
                self._skip()
                continue

            if self._current_char.isdigit():
                char = self._current_char
                return Token(TokenType.INTEGER, self._number())

            if self._current_char == "+":
                char = self._current_char
                self._forward()
                return Token(TokenType.PLUS, char)

            if self._current_char == "-":
                char = self._current_char
                self._forward()
                return Token(TokenType.MINUS, char)

            raise InterpreterException(f'bad token {self._current_char}')
        return Token(TokenType.EOS, None)

    def _check_token_type(self, type_: TokenType):
        if self._current_token.type_ == type_:
            self._current_token = self._next_token()
        else:
            raise InterpreterException('invalid token order')

    def _expr(self) -> float:
        self._current_token = self._next_token()
        left = self._current_token
        if left.type_ == TokenType.INTEGER:
            self._check_token_type(TokenType.INTEGER)
        else:
            self._check_token_type(TokenType.FLOAT)

        op = self._current_token
        if op.type_ == TokenType.PLUS:
            self._check_token_type(TokenType.PLUS)
        else:
            self._check_token_type(TokenType.MINUS)
        right = self._current_token
        if right.type_ == TokenType.INTEGER:
            self._check_token_type(TokenType.INTEGER)
        else:
            self._check_token_type(TokenType.FLOAT)

        if op.type_ == TokenType.PLUS:
            return float(left.value) + float(right.value)
        elif op.type_ == TokenType.MINUS:
            return float(left.value) - float(right.value)

        raise InterpreterException('bad operation')
