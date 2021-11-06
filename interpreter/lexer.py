from .tokens import TokenType, Token


class LexerException(Exception):
    pass


class Lexer():

    def __init__(self):
        self._pos: int = -1
        self._current_char: str = None
        self._text: str = None

    def next(self) -> Token:
        while self._current_char is not None:
            if self._current_char == ' ':
                self._skip()
                continue

            if self._current_char.isdigit():
                return Token(TokenType.FLOAT, self._number())

            if self._current_char == "+":
                char = self._current_char
                self._forward()
                return Token(TokenType.PLUS, char)

            if self._current_char == "-":
                char = self._current_char
                self._forward()
                return Token(TokenType.MINUS, char)

            if self._current_char == "*":
                char = self._current_char
                self._forward()
                return Token(TokenType.MUL, char)

            if self._current_char == "/":
                char = self._current_char
                self._forward()
                return Token(TokenType.DIV, char)

            if self._current_char == "(":
                char = self._current_char
                self._forward()
                return Token(TokenType.LPAREN, char)

            if self._current_char == ")":
                char = self._current_char
                self._forward()
                return Token(TokenType.RPAREN, char)

            raise LexerException(f'bad token {self._current_char}')
        return Token(TokenType.EOS, None)

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
                raise LexerException('invalid number')

        return ''.join(result)

    def init(self, text: str):
        self._text = text
        self._pos = -1
        self._forward()