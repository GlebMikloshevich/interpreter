from .tokens import TokenType, Token
from .lexer import Lexer
from .node import BinOp, Node, Number, UnaryOp


class ParserException(Exception):
    pass


class Parser():
    def __init__(self):
        self._current_token: Token = None
        self._lexer = Lexer()

    def __call__(self, text: str) -> Node:
        return self.parse(text)

    def parse(self, text: str) -> Node:
        self._lexer.init(text)
        self._current_token = self._lexer.next()
        return self._expr()

    def _check_token_type(self, type_: TokenType):
        if self._current_token.type_ == type_:
            self._current_token = self._lexer.next()
        else:
            raise ParserException('invalid token order')

    # def _pow(self) -> Node:
    #     result = self._factor()
    #     ops = [TokenType.POW]
    #
    #     while self._current_token.type_ in ops:
    #         token = self._current_token
    #         if token.type_ == TokenType.POW:
    #             self._check_token_type(TokenType.POW)
    #         result = BinOp(result, token, self._factor())
    #     return result

    def _factor(self) -> Node:
        token = self._current_token

        if token.type_ == TokenType.FLOAT:
            self._check_token_type(TokenType.FLOAT)
            return Number(token)
        elif token.type_ == TokenType.LPAREN:
            self._check_token_type(TokenType.LPAREN)
            result = self._expr()
            self._check_token_type(TokenType.RPAREN)
            return result
        elif token.type_ == TokenType.MINUS:
            self._check_token_type(TokenType.MINUS)
            return UnaryOp(token, self._factor())
        elif token.type_ == TokenType.PLUS:
            self._check_token_type(TokenType.PLUS)
            return UnaryOp(token, self._factor())
        else:
            raise ParserException(f"Invalid factor - {token.type_}")

    def _term(self) -> Node:
        result = self._factor()
        ops = [TokenType.MUL, TokenType.DIV, TokenType.POW]

        while self._current_token.type_ in ops:
            token = self._current_token
            if token.type_ == TokenType.POW:
                self._check_token_type(TokenType.POW)
            elif token.type_ == TokenType.DIV:
                self._check_token_type(TokenType.DIV)
            else:
                self._check_token_type(TokenType.MUL)
            result = BinOp(result, token, self._factor())
        return result

    def _expr(self) -> Node:

        ops = [TokenType.PLUS, TokenType.MINUS]
        result = self._term()
        while self._current_token.type_ in ops:
            token = self._current_token
            if token.type_ == TokenType.PLUS:
                self._check_token_type(TokenType.PLUS)
            else:
                self._check_token_type(TokenType.MINUS)
            result = BinOp(result, token, self._term())
        return result
