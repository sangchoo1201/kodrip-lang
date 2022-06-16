from constant import *
from error import *
from position import Position


class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end.copy()

    def matches(self, type_, value):
        return self.type == type_ and self.value == value

    def __repr__(self):
        return f'{self.type}:{self.value}' if self.value else f'{self.type}'


# Lexer
class Lexer:
    def __init__(self, file_name, text):
        self.file_name = file_name
        self.text = text
        self.pos = Position(-1, 0, -1, self.file_name, self.text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None

    def make_tokens(self):
        tokens = []

        functions = {
            "+": self.plus, "-": self.minus,
            "*": self.mul, "/": self.div,
            "%": self.mod, ",": self.comma,
            "(": self.lparen, ")": self.rparen,
            "=": self.ee, "!": self.ne,
            "<": self.lt, ">": self.gt,
            "?": self.question, "~": self.wave,
            "\n": self.newline,
        }

        while self.current_char is not None:
            if self.current_char in functions:
                token, error = functions[self.current_char]()
                if error:
                    return [], error
                tokens.append(token)
            elif self.current_char.isdigit():
                tokens.append(self.number())
            elif self.current_char.isalpha():
                tokens.append(self.identifier())
            elif self.current_char not in ' \t':
                pos_start = self.pos.copy()
                invalid_char = self.current_char
                self.advance()
                pos_end = self.pos.copy()
                return [], InvalidCharError(pos_start, pos_end, f"'{invalid_char}'")
            else:
                self.advance()

        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    def newline(self):
        token = Token(TT_NEWLINE, pos_start=self.pos)
        self.advance()
        return token, None

    def question(self):
        token = Token(TT_QUESTION, pos_start=self.pos)
        self.advance()
        return token, None

    def wave(self):
        token = Token(TT_WAVE, pos_start=self.pos)
        self.advance()
        return token, None

    def number(self):
        pos_start = self.pos.copy()
        digits = self.current_char
        self.advance()

        while self.current_char is not None and self.current_char.isdigit():
            digits += self.current_char
            self.advance()

        return Token(TT_INT, int(digits), pos_start, self.pos)

    def identifier(self):
        pos_start = self.pos.copy()
        id_text = self.current_char
        self.advance()

        while self.current_char is not None and self.current_char.isalnum():
            id_text += self.current_char
            self.advance()

        token_type = TT_KEYWORD if id_text in KEYWORDS else TT_IDENTIFIER
        return Token(token_type, id_text, pos_start, self.pos)

    def plus(self):
        token = Token(TT_PLUS, pos_start=self.pos)
        self.advance()
        return token, None

    def minus(self):
        token = Token(TT_MINUS, pos_start=self.pos)
        self.advance()
        return token, None

    def mul(self):
        token = Token(TT_MUL, pos_start=self.pos)
        self.advance()
        return token, None

    def div(self):
        token = Token(TT_DIV, pos_start=self.pos)
        self.advance()
        return token, None

    def mod(self):
        token = Token(TT_MOD, pos_start=self.pos)
        self.advance()
        return token, None

    def lparen(self):
        token = Token(TT_LPAREN, pos_start=self.pos)
        self.advance()
        return token, None

    def rparen(self):
        token = Token(TT_RPAREN, pos_start=self.pos)
        self.advance()
        return token, None

    def comma(self):
        token = Token(TT_COMMA, pos_start=self.pos)
        self.advance()
        return token, None

    def ee(self):
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            return Token(TT_EE, pos_start=pos_start, pos_end=self.pos), None

        return None, ExpectedCharError(pos_start, self.pos, "다음 문자가 있어야 합니다: '=' ('=' 뒤에)")

    def ne(self):
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            return Token(TT_NE, pos_start=pos_start, pos_end=self.pos), None

        return Token(TT_BANG, pos_start=pos_start, pos_end=self.pos), None

    def lt(self):
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            return Token(TT_LTE, pos_start=pos_start, pos_end=self.pos), None

        return Token(TT_LT, pos_start=pos_start, pos_end=self.pos), None

    def gt(self):
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            return Token(TT_GTE, pos_start=pos_start, pos_end=self.pos), None

        return Token(TT_GT, pos_start=pos_start, pos_end=self.pos), None