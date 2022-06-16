from support import draw_arrow


# Errors
class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name} - {self.details}\n'
        result += f'파일 {self.pos_start.file_name}, {self.pos_start.line + 1}번 라인'
        result += draw_arrow(self.pos_start.file_text, self.pos_start, self.pos_end)
        return result


class InvalidCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, '뭐 이런 그지 문자가 다 있어?', details)


class ExpectedCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, '있어야 할 게 없잖아 임마!', details)


class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, '너 지금 뭐라고 했니?', details)


class RTError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, '인 방송 중에는!', details)
        self.context = context

    def as_string(self):
        result = self.generate_traceback()
        result += f'{self.error_name}: {self.details}'
        result += draw_arrow(self.pos_start.file_text, self.pos_start, self.pos_end)
        return result

    def generate_traceback(self):
        result = ''
        pos = self.pos_start
        ctx = self.context

        while ctx:
            result = f'  파일 {pos.file_name}, {str(pos.line + 1)}번 라인, "{ctx.name}"에서\n{result}'

            pos = ctx.entry_pos
            ctx = ctx.parent

        return f'스택택님 트레이스 (최근 호출이 마지막):\n{result}'
