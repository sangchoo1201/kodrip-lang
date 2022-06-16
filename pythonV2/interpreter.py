from constant import *
from value import *
from structure import *
from lexer import Lexer
from parse import Parser


class Interpreter:
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        # noinspection PyArgumentList
        return method(node, context)

    def no_visit_method(self, node, context):
        # sourcery skip: raise-specific-error
        raise Exception(f'No visit_{type(node).__name__} method defined')

    @staticmethod
    def visit_NumberNode(node, context):
        return RTResult().success(
            Number(node.token.value)
            .set_context(context)
            .set_pos(node.pos_start, node.pos_end)
        )

    def visit_ListNode(self, node, context):
        res = RTResult()
        elements = []

        for element_node in node.elements:
            elements.append(res.register(self.visit(element_node, context)))
            if res.should_return():
                return res

        return res.success(
            List(elements).set_context(context)
                .set_pos(node.pos_start, node.pos_end)
        )

    @staticmethod
    def visit_VarAccessNode(node, context):
        res = RTResult()
        var_name = node.token.value
        value = context.symbol_table.get(var_name)

        if var_name == "뽈롱":
            temp = ""
            while not (temp.isdigit() or (temp and temp[0] == "-" and temp[1:].isdigit())):
                temp = input("숫자를 입력하세요: ")
            value = Number(int(temp))\
                .set_context(context)\
                .set_pos(node.pos_start, node.pos_end)
            return res.success(value)

        if value is None:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                f'{var_name}는 선언되지 않았습니다',
                context
            ))

        value = value.copy()\
            .set_pos(node.pos_start, node.pos_end)\
            .set_context(context)
        return res.success(value)

    def visit_VarAssignNode(self, node, context):
        res = RTResult()
        var_name = node.token.value
        value = res.register(self.visit(node.value, context))
        if res.should_return():
            return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_BinOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left, context))
        if res.should_return():
            return res
        right = res.register(self.visit(node.right, context))
        if res.should_return():
            return res

        result, error = None, None

        if node.op_token.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_token.type == TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_token.type == TT_MUL:
            result, error = left.multed_by(right)
        elif node.op_token.type == TT_DIV:
            result, error = left.dived_by(right)
        elif node.op_token.type == TT_MOD:
            result, error = left.moded_by(right)
        elif node.op_token.type == TT_EE:
            result, error = left.get_comparison_eq(right)
        elif node.op_token.type == TT_NE:
            result, error = left.get_comparison_ne(right)
        elif node.op_token.type == TT_LT:
            result, error = left.get_comparison_lt(right)
        elif node.op_token.type == TT_GT:
            result, error = left.get_comparison_gt(right)
        elif node.op_token.type == TT_LTE:
            result, error = left.get_comparison_lte(right)
        elif node.op_token.type == TT_GTE:
            result, error = left.get_comparison_gte(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.should_return():
            return res

        error = None

        if node.op_token.type == TT_MINUS:
            number, error = number.multed_by(Number(-1))

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))

    def visit_IfNode(self, node, context):
        res = RTResult()
        condition_value = res.register(self.visit(node.case[0], context))
        if res.should_return():
            return res

        if condition_value.is_true():
            res.register(self.visit(node.case[1], context))
        elif node.else_case:
            res.register(self.visit(node.else_case, context))

        if res.should_return():
            return res
        return res.success(None)

    def visit_ForNode(self, node, context):
        res = RTResult()

        end_value = res.register(self.visit(node.end_value, context))
        if res.should_return():
            return res

        i = 0

        while i < end_value.value:
            context.symbol_table.set(node.var_name.value, Number(i))
            res.register(self.visit(node.body, context))
            if res.should_return():
                return res

            i += 1

        return res.success(None)

    def visit_WhileNode(self, node, context):
        res = RTResult()
        condition_value = res.register(self.visit(node.condition, context))
        if res.should_return():
            return res

        while condition_value.is_true():
            res.register(self.visit(node.body, context))
            if res.should_return():
                return res

            condition_value = res.register(self.visit(node.condition, context))
            if res.should_return():
                return res

        return res.success(None)

    @staticmethod
    def visit_FuncDefNode(node, context):
        res = RTResult()
        func_name = node.name.value
        body_node = node.body
        arg_names = [arg_node.value for arg_node in node.args]
        func_value = Function(func_name, body_node, arg_names)\
            .set_context(context)\
            .set_pos(node.pos_start, node.pos_end)
        context.symbol_table.set(func_name, func_value)
        return res.success(func_value)

    def visit_FuncCallNode(self, node, context):
        res = RTResult()
        args = []
        value_to_call = res.register(self.visit(node.name, context))
        if res.should_return():
            return res
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

        for arg_node in node.args:
            args.append(res.register(self.visit(arg_node, context)))
            if res.should_return():
                return res

        return_value = res.register(value_to_call.execute(args))
        if res.should_return():
            return res
        return_value = return_value.copy()\
            .set_pos(node.pos_start, node.pos_end)\
            .set_context(context)
        return res.success(return_value)

    def visit_ReturnNode(self, node, context):
        res = RTResult()

        if node.value:
            value = res.register(self.visit(node.value, context))
            if res.should_return():
                return res
        else:
            value = Number(0)

        return res.success_return(value)

    def visit_PrintNode(self, node, context):
        res = RTResult()

        value = res.register(self.visit(node.value, context))
        if res.should_return():
            return res

        if output_file:
            with open(output_file, "a", encoding="utf-8") as f:
                f.write(str(value.value))
                f.write("\n")
        else:
            print(value.value)

        return res.success(None)


global_symbol_table = SymbolTable()
global_symbol_table.set("ㅖ", Number(0))
global_symbol_table.set("언", Number(1))
global_symbol_table.set("코", Number(-3000))


output_file = ""


def run(file_name, text, stdout=""):
    global output_file
    output_file = stdout
    if stdout:
        with open(stdout, "w") as f:
            f.write("")

    lexer = Lexer(file_name, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error

    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error

    interpreter = Interpreter()
    context = Context("<program>")
    context.symbol_table = global_symbol_table
    print(ast.node)
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
