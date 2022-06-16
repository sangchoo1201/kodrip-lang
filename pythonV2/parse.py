from node import *
from constant import *
from error import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = -1
        self.advance()

    def advance(self):
        self.token_index += 1
        self.current_token = None
        self.update_current_token()
        return self.current_token

    def reverse(self, amount=1):
        self.token_index -= amount
        self.update_current_token()
        return self.current_token

    def update_current_token(self):
        if 0 <= self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]

    def parse(self):
        res = self.statements()
        if not res.error and self.current_token.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "키워드 뒤에 바로 키워드가 나올 수 없습니다."
            ))
        return res

    def statements(self):
        res = ParseResult()
        pos_start = self.current_token.pos_start.copy()

        while self.current_token.type == TT_NEWLINE:
            res.register_advance()
            self.advance()
        statement = res.register(self.statement())
        if res.error:
            return res
        statements = [statement]

        more_statements = True

        while True:
            newline_count = 0
            while self.current_token.type == TT_NEWLINE:
                res.register_advance()
                self.advance()
                newline_count += 1
            if newline_count == 0:
                more_statements = False

            if not more_statements:
                break
            statement = res.try_register(self.statement())
            if not statement:
                self.reverse(res.reverse_count)
                more_statements = False
                continue
            statements.append(statement)

        return res.success(ListNode(
            statements, pos_start,
            self.current_token.pos_end.copy()
        ))

    def statement(self):
        res = ParseResult()

        if self.current_token.matches(TT_IDENTIFIER, '코'):
            while self.current_token.type != TT_NEWLINE:
                res.register_advance()
                self.advance()
            res.register_advance()
            self.advance()

        pos_start = self.current_token.pos_start.copy()

        if self.current_token.matches(TT_KEYWORD, '지금부터는'):
            res.register_advance()
            self.advance()

            expr = res.try_register(self.expr())
            if not expr:
                self.reverse(res.reverse_count)
            return res.success(ReturnNode(
                expr, pos_start, self.current_token.pos_end.copy()
            ))

        expr = res.register(self.expr())
        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "다음이 필요합니다: '지금부터는', '자~', '얘!', '죽이고싶은', '인', '뭉탱이', 정수, 식별자, '+', '-', '('"
            ))
        return res.success(expr)

    def expr(self):
        res = ParseResult()

        if self.current_token.matches(TT_KEYWORD, '자'):
            res.register_advance()
            self.advance()

            if self.current_token.type != TT_WAVE:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "다음이 필요합니다: '~' ('자' 뒤에)"
                ))

            res.register_advance()
            self.advance()

            if self.current_token.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "다음이 필요합니다: 식별자 ('자~' 뒤에)"
                ))

            var_name = self.current_token
            res.register_advance()
            self.advance()

            if not self.current_token.matches(TT_KEYWORD, '를'):
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "다음이 필요합니다: '를' (변수 이름 뒤에)"
                ))

            res.register_advance()
            self.advance()

            if self.current_token.type != TT_BANG:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "다음이 필요합니다: '!' ('를' 뒤에)"
                ))

            res.register_advance()
            self.advance()

            expr = res.register(self.expr())
            if res.error:
                return res
            return res.success(VarAssignNode(var_name, expr))
        elif self.current_token.matches(TT_KEYWORD, '오옹'):
            pos_start = self.current_token.pos_start.copy()

            res.register_advance()
            self.advance()

            if self.current_token.type != TT_BANG:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "다음이 필요합니다: '!' ('오옹' 뒤에)"
                ))

            res.register_advance()
            self.advance()

            expr = res.register(self.expr())
            if res.error:
                return res
            return res.success(PrintNode(expr, pos_start, self.current_token.pos_end.copy()))

        node = res.register(self.comp_expr())

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "다음이 필요합니다: '자~', '얘!', '죽이고싶은', '인', '뭉탱이', 정수, 식별자, '+', '-', '('"
            ))
        return res.success(node)

    def comp_expr(self):
        res = ParseResult()

        node = res.register(self.bin_op(
            self.arith_expr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE)
        ))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "다음이 필요합니다: '자~', '얘!', '죽이고싶은', '인', '뭉탱이', 정수, 식별자, '+', '-', '('"
            ))
        return res.success(node)

    def arith_expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV, TT_MOD))

    def factor(self):
        res = ParseResult()
        token = self.current_token

        if token.type in (TT_PLUS, TT_MINUS):
            res.register_advance()
            self.advance()
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(token, factor))

        return self.call()

    def call(self):
        res = ParseResult()
        atom = res.register(self.atom())
        if res.error:
            return res

        if self.current_token.type == TT_LPAREN:
            res.register_advance()
            self.advance()
            arg_nodes = []

            if self.current_token.type != TT_RPAREN:
                arg_nodes.append(res.register(self.expr()))
                if res.error:
                    return res.failure(InvalidSyntaxError(
                        self.current_token.pos_start, self.current_token.pos_end,
                        "다음이 필요합니다: ')', ',', '자~', '얘!', '죽이고싶은', '인', '뭉탱이', 정수, 식별자, '+', '-', '('"
                    ))

                while self.current_token.type == TT_COMMA:
                    res.register_advance()
                    self.advance()
                    arg_nodes.append(res.register(self.expr()))
                    if res.error:
                        return res

            if self.current_token.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "다음이 필요합니다: ',', ')'"
                ))

            res.register_advance()
            self.advance()
            return res.success(FuncCallNode(atom, arg_nodes))
        return res.success(atom)

    def atom(self):
        res = ParseResult()
        token = self.current_token

        if token.type == TT_INT:
            res.register_advance()
            self.advance()
            return res.success(NumberNode(token))
        elif token.type == TT_IDENTIFIER:
            res.register_advance()
            self.advance()
            return res.success(VarAccessNode(token))
        elif token.type == TT_LPAREN:
            res.register_advance()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.current_token.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "다음이 필요합니다: ')'"
                ))
            res.register_advance()
            self.advance()
            return res.success(expr)
        elif token.matches(TT_KEYWORD, "얘"):
            if_expr = res.register(self.if_expr())
            if res.error:
                return res
            return res.success(if_expr)
        elif token.matches(TT_KEYWORD, "죽이고싶은"):
            for_expr = res.register(self.for_expr())
            if res.error:
                return res
            return res.success(for_expr)
        elif token.matches(TT_KEYWORD, "인"):
            while_expr = res.register(self.while_expr())
            if res.error:
                return res
            return res.success(while_expr)
        elif token.matches(TT_KEYWORD, "뭉탱이"):
            func_def = res.register(self.func_def())
            if res.error:
                return res
            return res.success(func_def)
        return res.failure(InvalidSyntaxError(
            token.pos_start, token.pos_end,
            "다음이 필요합니다: '얘!', '죽이고싶은', '인', '뭉탱이', 정수, 식별자, '+', '-', '('"
        ))

    def end_helper(self):
        res = ParseResult()

        if not self.current_token.matches(TT_KEYWORD, "에이씨"):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "다음이 필요합니다: '에이씨 나쁜 놈' (제어문 내용 뒤에)"
            ))
        res.register_advance()
        self.advance()
        if not self.current_token.matches(TT_KEYWORD, "나쁜"):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "다음이 필요합니다: '나쁜 놈' ('에이씨' 뒤에)"
            ))
        res.register_advance()
        self.advance()
        if not self.current_token.matches(TT_KEYWORD, "놈"):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "다음이 필요합니다: '놈' ('에이씨 나쁜' 뒤에)"
            ))
        return res.success(None)

    def if_expr(self):
        res = ParseResult()
        else_case = None

        res.register_advance()
        self.advance()
        if self.current_token.type != TT_BANG:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "다음이 필요합니다: '!' ('얘' 뒤에)"
            ))
        res.register_advance()
        self.advance()
        condition = res.register(self.expr())
        if res.error:
            return res
        if not self.current_token.matches(TT_KEYWORD, "하니"):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "다음이 필요합니다: '하니?' (조건 뒤에)"
            ))
        res.register_advance()
        self.advance()
        if self.current_token.type != TT_QUESTION:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "다음이 필요합니다: '?' ('하니' 뒤에)"
            ))
        res.register_advance()
        self.advance()

        if self.current_token.type != TT_NEWLINE:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "다음이 필요합니다: 줄바꿈 ('하니?' 뒤에)"
            ))

        res.register_advance()
        self.advance()

        statements = res.register(self.statements())
        if res.error:
            return res
        case = (condition, statements)

        if self.current_token.matches(TT_KEYWORD, "안하니"):
            res.register_advance()
            self.advance()
            if self.current_token.type != TT_QUESTION:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "다음이 필요합니다: '?' ('안하니' 뒤에)"
                ))
            res.register_advance()
            self.advance()
            if self.current_token.type != TT_NEWLINE:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "다음이 필요합니다: 줄바꿈 ('안하니?' 뒤에)"
                ))
            res.register_advance()
            self.advance()
            statements = res.register(self.statements())
            if res.error:
                return res
            else_case = statements

        res.register(self.end_helper())
        if res.error:
            return res

        res.register_advance()
        self.advance()

        return res.success(IfNode(case, else_case))

    def for_expr(self):
        res = ParseResult()

        res.register_advance()
        self.advance()

        if self.current_token.type != TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "다음이 필요합니다: 변수 이름 ('죽이고싶은' 뒤에)"
            ))
        var_name = self.current_token
        res.register_advance()
        self.advance()

        if not self.current_token.matches(TT_KEYWORD, "와의"):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "다음이 필요합니다: '와의' (변수 이름 뒤에)"
            ))

        res.register_advance()
        self.advance()

        end_value = res.register(self.expr())
        if res.error:
            return res

        if not self.current_token.matches(TT_KEYWORD, "선"):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "다음이 필요합니다: '선' (반복 횟수 뒤에)"
            ))

        res.register_advance()
        self.advance()

        if self.current_token.type != TT_NEWLINE:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "다음이 필요합니다: 줄바꿈 ('선' 뒤에)"
            ))

        res.register_advance()
        self.advance()

        statements = res.register(self.statements())
        if res.error:
            return res

        res.register(self.end_helper())
        if res.error:
            return res

        res.register_advance()
        self.advance()

        return res.success(ForNode(var_name, end_value, statements))

    def while_expr(self):
        res = ParseResult()

        res.register_advance()
        self.advance()

        condition = res.register(self.expr())
        if res.error:
            return res

        if not self.current_token.matches(TT_KEYWORD, "중에는"):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "다음이 필요합니다: '중에는!' (조건 뒤에)"
            ))

        res.register_advance()
        self.advance()

        if self.current_token.type != TT_BANG:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "다음이 필요합니다: '!' ('중에는' 뒤에)"
            ))

        res.register_advance()
        self.advance()

        if self.current_token.type != TT_NEWLINE:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "다음이 필요합니다: 줄바꿈 ('중에는!' 뒤에)"
            ))

        res.register_advance()
        self.advance()

        statements = res.register(self.statements())
        if res.error:
            return res

        res.register(self.end_helper())
        if res.error:
            return res

        res.register_advance()
        self.advance()

        return res.success(WhileNode(condition, statements))

    def func_def(self):
        res = ParseResult()

        res.register_advance()
        self.advance()

        if self.current_token.type != TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "다음이 필요합니다: 함수 이름 ('뭉탱이' 뒤에)"
            ))

        func_name_token = self.current_token
        res.register_advance()
        self.advance()

        if self.current_token.type != TT_LPAREN:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "다음이 필요합니다: '(' (함수 이름 뒤에)"
            ))

        res.register_advance()
        self.advance()

        arg_name_tokens = []

        if self.current_token.type == TT_IDENTIFIER:
            arg_name_tokens = [self.current_token]
            res.register_advance()
            self.advance()
            while self.current_token.type == TT_COMMA:
                res.register_advance()
                self.advance()
                if self.current_token.type != TT_IDENTIFIER:
                    return res.failure(InvalidSyntaxError(
                        self.current_token.pos_start, self.current_token.pos_end,
                        "다음이 필요합니다: 매개변수 이름 (',' 뒤에)"
                    ))
                arg_name_tokens.append(self.current_token)
                res.register_advance()
                self.advance()
            if self.current_token.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "다음이 필요합니다: ',', ')' (매개변수 이름 뒤에)"
                ))
        elif self.current_token.type != TT_RPAREN:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "다음이 필요합니다: 매개변수 이름, ')' ('(' 뒤에)"
            ))
        res.register_advance()
        self.advance()

        if self.current_token.type != TT_NEWLINE:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "다음이 필요합니다: 줄바꿈 (함수 선언 뒤에)"
            ))

        res.register_advance()
        self.advance()

        body = res.register(self.statements())
        if res.error:
            return res

        if not (self.current_token.matches(TT_KEYWORD, "유링게슝") or
                self.current_token.matches(TT_KEYWORD, "유리게슝")):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "다음이 필요합니다: '유링게슝', '유리게슝' (함수 본문 뒤에)"
            ))

        res.register_advance()
        self.advance()

        return res.success(FuncDefNode(
            func_name_token, arg_name_tokens, body
        ))

    def bin_op(self, func_a, ops, func_b=None):
        if func_b is None:
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a())
        if res.error:
            return res

        while self.current_token.type in ops or (self.current_token.type, self.current_token.value) in ops:
            op_token = self.current_token
            res.register_advance()
            self.advance()
            right = res.register(func_b())
            if res.error:
                return res
            left = BinOpNode(left, op_token, right)
        return res.success(left)


class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.last_advance_count = 0
        self.advance_count = 0
        self.reverse_count = 0

    def register_advance(self):
        self.last_advance_count = 1
        self.advance_count += 1

    def register(self, res):
        self.last_advance_count = res.advance_count
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        return res.node

    def try_register(self, res):
        if res.error:
            self.reverse_count = res.advance_count
            return None
        return self.register(res)

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.last_advance_count == 0:
            self.error = error
        return self
