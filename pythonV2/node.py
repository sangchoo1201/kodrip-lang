class NumberNode:
    def __init__(self, token):
        self.token = token

        self.pos_start = token.pos_start
        self.pos_end = token.pos_end

    def __repr__(self):
        return f'Number({self.token.value})'


class VarAccessNode:
    def __init__(self, token):
        self.token = token

        self.pos_start = token.pos_start
        self.pos_end = token.pos_end

    def __repr__(self):
        return f'Access({self.token.value})'


class VarAssignNode:
    def __init__(self, token, value):
        self.token = token
        self.value = value

        self.pos_start = token.pos_start
        self.pos_end = value.pos_end

    def __repr__(self):
        return f'Assign({self.token.value}, {self.value})'


class BinOpNode:
    def __init__(self, left, op_token, right):
        self.left = left
        self.op_token = op_token
        self.right = right

        self.pos_start = left.pos_start
        self.pos_end = right.pos_end

    def __repr__(self):
        return f'BinOp({self.left}, {self.op_token}, {self.right})'


class UnaryOpNode:
    def __init__(self, op_token, node):
        self.op_token = op_token
        self.node = node

        self.pos_start = op_token.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f'UnaryOp({self.op_token}, {self.node})'


class ListNode:
    def __init__(self, elements, pos_start, pos_end):
        self.elements = elements

        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f'Statements{self.elements}'


class IfNode:
    def __init__(self, case, else_case):
        self.case = case
        self.else_case = else_case

        self.pos_start = self.case[0].pos_start
        self.pos_end = (else_case or self.case[0]).pos_end

    def __repr__(self):
        return f'If({self.case[0]}, {self.case[1]}, {self.else_case})'


class ForNode:
    def __init__(self, var_name, end_value, body):
        self.var_name = var_name
        self.end_value = end_value
        self.body = body

        self.pos_start = self.var_name.pos_start
        self.pos_end = self.body.pos_end

    def __repr__(self):
        return f'For({self.var_name.value}, {self.end_value}, {self.body})'


class WhileNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

        self.pos_start = self.condition.pos_start
        self.pos_end = self.body.pos_end

    def __repr__(self):
        return f'While({self.condition}, {self.body})'


class FuncDefNode:
    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = body

        self.pos_start = self.name.pos_start
        self.pos_end = self.body.pos_end

    def __repr__(self):
        return f'FuncDef({self.name.value}, List[{", ".join(map(lambda x: x.value, self.args))}], {self.body})'


class FuncCallNode:
    def __init__(self, name, args):
        self.name = name
        self.args = args

        self.pos_start = self.name.pos_start
        if len(self.args) > 0:
            self.pos_end = self.args[-1].pos_end
        else:
            self.pos_end = self.name.pos_end

    def __repr__(self):
        return f'FuncCall({self.name}, List{self.args})'


class ReturnNode:
    def __init__(self, value, pos_start, pos_end):
        self.value = value

        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f'Return({self.value})'


class PrintNode:
    def __init__(self, value, pos_start, pos_end):
        self.value = value

        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f'Print({self.value})'
