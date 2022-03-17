import os.path
from typing import Optional, Tuple, Union, Any, List
import sys

print = print

def end_letter(word: str, yes: Optional[str] = "은", no: Optional[str] = "는") -> str:
    last_word = word[-1]
    while last_word == "_":
        word = word[:-1]
        if not word:
            return yes
        last_word = word[-1]

    if ord("ㄱ") <= ord(last_word) <= ord("ㅎ"):
        return yes
    elif ord("ㅏ") <= ord(last_word) <= ord("ㅣ"):
        return no

    if last_word.lower() in "aeiouwy":
        return no
    elif last_word.lower() in "bcdfghjklmnpqrstvxz":
        return yes

    if last_word in "2459":
        return no
    elif last_word in "013678":
        return yes

    if (ord(last_word) - ord("가")) % 28:
        return yes
    else:
        return no


def width(value: str):
    cnt = 0
    for i in value:
        if ord("가") <= ord(i) <= ord("힣"):
            cnt += 2
        elif ord("ㄱ") <= ord(i) <= ord("ㅎ"):
            cnt += 2
        elif ord("ㅏ") <= ord(i) <= ord("ㅣ"):
            cnt += 2
        else:
            cnt += 1
    return cnt


def calc_split(line: str) -> List[str]:
    cnt = 0
    positions = []
    for i, text in enumerate(line):
        if text == "(":
            cnt += 1
        elif text == ")":
            cnt -= 1
        if not cnt and text in "+-*/%":
            positions.append(i)
    parts = []
    for s, e in zip([-1]+positions, positions+[len(line)]):
        if line[s+1:e].strip():
            parts.append(line[s+1:e].strip())
        if e != len(line):
            parts.append(line[e])
    return parts

class func:
    def __init__(self, name: str, start: int, param: dict):
        self.name: str = name
        self.cnt: int = start
        self.var: dict = param
        self.calling: Union[Tuple[int, int], Tuple] = ()
        self.control: list = []
        self.jump: dict = {}


class control:
    def __init__(self, type_: str, start: int):
        self.type: str = type_
        self.start: int = start


class compiler:
    def __init__(self):
        self.version: str = "v1.1.2"
        self.keywords: tuple = (
            "안녕하세요", "저는", "죄송합니다",
            "코", "자~", "를!", "뽈롱", "오옹!",
            "얘!", "하니?", "안하니?",
            "죽이고싶은", "와의", "선",
            "인", "중에는!", "왔어...", "갔어...",
            "에이씨", "나쁜", "놈",
            "뭉탱이", "유리게슝", "유링게슝", "지금부터는"
        )
        self.exec: tuple = (
            self.start, None, self.end,
            None, self.assign, None, None, self.print,
            self.if_, None, self.else_,
            self.for_, None, None,
            self.while_, None, self.set, self.jump,
            self.break_, None, None,
            self.assign_func, self.end_func, self.end_func, self.return_
        )
        self.stack: list = [func("__본방__", 1, {})]
        self.lines: List[str] = []
        self.stdin: str = ""
        self.stdout: str = ""
        self.funcs: dict = {}
        self.return_value = 0

    def write_file(self, *args: Any, end: Optional[str] = "\n", sep: Optional[str] = " "):
        with open(self.stdout, "a") as f:
            f.write(sep.join(map(str, args)) + end)

    @staticmethod
    def start(line: str) -> None:
        _ = line
        return

    @staticmethod
    def end(line: str) -> None:
        _ = line
        sys.exit()

    def error(self, state: str) -> None:
        print("이거나드셔: 스택택님 트레이스")
        for i in self.stack:
            print("    ", end="")
            if self.stdin:
                print(f"파일 \"{self.stdin}\", ", end="")
            print(f"{i.cnt}번 줄, 함수 {i.name}:")
            line = self.lines[i.cnt-1]
            print(f"      {line}")
            if i.calling:
                print("      " + " "*width(line[:i.calling[0]]) + "^"*width(line[i.calling[0]:i.calling[1]]))
        print(state)
        sys.exit(1)

    def check_name(self, name: str) -> None:
        if not name:
            self.error("아무 것도 없잖아 임마!(변수 이름이 없음)")
        if name in self.keywords:
            self.error(f"키워드는 안돼 임마!('{name}'{end_letter(name)} 키워드임)")
        if name[0].isnumeric():
            self.error(f"숫자는 안돼 임마!('{name}'{end_letter(name)} 숫자로 시작함)")
        for i in "+-*/%()<>=.,?!~ ":
            if i in name:
                self.error(f"기호는 안돼 임마!('{name}'{end_letter(name)} 기호를 포함함)")

    @staticmethod
    def input() -> int:
        value = input("입력: ")
        while not (value.isnumeric() or (value[0] == "-" and value[1:].isnumeric())):
            print("정수 내놔 정수!")
            value = input("입력: ")
        return int(value)

    def calc(self, value: str) -> int:
        if not value:
            self.error("아무 것도 없잖아 임마!(연산 식에서 중간이 빔)")

        parts = calc_split(value)

        was_operator = False
        for i, part in enumerate(parts):
            if part in "+-*/%":
                if was_operator:
                    self.error("뭐 이런 그지 값이 다 있어?(둘 이상의 연산자가 붙어있음)")
                was_operator = True
                continue
            else:
                was_operator = False
            if part.startswith("(") and part.startswith(")"):
                parts[i] = str(self.calc(part))
            elif "(" in part:
                pos = part.index("(")
                line = self.lines[self.stack[-1].cnt-1]
                parts[i] = str(self.call(part[:pos], part[pos:], line.index(part)))
            elif part in self.stack[-1].var:
                parts[i] = str(self.stack[-1].var[part])
            elif part == "코":
                parts[i] = "-3000"
            elif part.count("ㅖ") == len(part) != 0:
                parts[i] = str(len(part))
            elif part.count("언") == len(part) != 0:
                parts[i] = str(-len(part))
            elif part == "뽈롱":
                parts[i] = str(self.input())
            elif not part.isnumeric():
                self.error(f"뭐 이런 그지 값이 다 있어?('{part}'{end_letter(part)} 없는 변수임)")
        value = "".join(parts)
        value = value.replace("/", "//")
        return eval(value)

    def comp(self, value: str) -> bool:
        comp = ""
        for i in ("==", ">=", "<=", "!=", ">", "<"):
            if i in value:
                a, b = map(lambda x: str(self.calc(x)), value.split(i))
                comp = i
                break
        else:
            self.error("뭐 이런 그지 값이 다 있어?(비교 연산자가 없음)")
        return eval(a + comp + b)

    def call(self, name: str, line: str, start: Optional[int] = 0) -> int:
        if name not in self.funcs:
            self.error(f"뭉탱이로 유링게슝('{name}'{end_letter(name)} 있는 함수가 아님)")
        self.stack[-1].calling = (start, start+len(line)+len(name))
        line = line[1:-1]
        cnt = 0
        comma = []
        for i, char in enumerate(line):
            if char == "(":
                cnt += 1
            elif char == ")":
                cnt -= 1
                if cnt < 0:
                    self.error("음 주겨벌랑(실행 가능한 구문이 아님)")
            elif cnt == 0 and char == ",":
                comma.append(i)
        if cnt:
            self.error("음 주겨벌랑(실행 가능한 구문이 아님)")
        param = [
            line[i+1:j].strip()
            for i, j
            in zip([-1]+comma, comma+[len(line)])
        ]
        if len(param) != 1 or param[0]:
            param = list(map(self.calc, param))
        else:
            param = []
        if len(param) != len(self.funcs[name]["params"]):
            self.error(f"뭉탱이로 유링게슝({len(self.funcs[name]['params'])}개의 인자가 필요한데, {len(param)}개가 주어짐)")
        self.stack.append(func(name, self.funcs[name]["start"]+1, dict(zip(self.funcs[name]["params"], param))))
        self.run_func()
        return self.return_value

    def run_func(self) -> None:
        self.return_value = None
        while self.return_value is None:
            if self.stack[-1].cnt > len(self.lines):
                self.lines.append("")
                self.error("자~숙하자~(방송이 '죄송합니다'로 끝나지 않음)")
            self.execute_line(self.lines[self.stack[-1].cnt-1].strip())
            self.stack[-1].cnt += 1

    def assign(self, line: str) -> None:
        if "를!" not in line:
            self.error("뭐 이런 그지 값이 다 있어?('를!'이 없음)")
        name, value = line.split("를!", 1)
        name = name.strip()
        self.check_name(name)
        value = value.strip()
        if not value:
            self.error("뭐 이런 그지 값이 다 있어?('를!' 뒤에 값이 없음)")
        self.stack[-1].var[name] = self.calc(value)

    def print(self, line: str) -> None:
        print(self.calc(line))

    def if_(self, line: str) -> None:
        self.stack[-1].control.append(control("if", self.stack[-1].cnt))
        line = line.split(" ")
        if "하니?" not in line:
            self.error("너 지금 뭐하니?(조건문에 '하니?'가 없음)")
        pos = line.index("하니?")
        if line[pos+1:]:
            self.error("너 지금 뭐하니?('하니?' 뒤에 다른 멘트가 옴)")
        if not self.comp(" ".join(line[:pos])):
            while True:
                self.stack[-1].cnt += 1
                if self.stack[-1].cnt > len(self.lines):
                    self.lines.append("")
                    self.error("너 지금 뭐하니?(조건문이 끝나지 않음)")
                line = self.lines[self.stack[-1].cnt - 1].strip()
                if line in {"유링게슝", "유리게슝"} or line.startswith("뭉탱이"):
                    self.error("너 지금 뭐하니?(조건문이 끝나지 않음)")
                if line == "안하니?":
                    break
                if line == "에이씨 나쁜 놈":
                    self.stack[-1].control.pop()
                    break

    def else_(self, line: str) -> None:
        if line:
            self.error("너 지금 뭐하니?('안하니?' 뒤에 다른 멘트가 옴)")
        if self.stack[-1].control[-1].type != "if":
            self.error("너 지금 뭐하니?(조건문이 시작하지 않음)")
        while True:
            self.stack[-1].cnt += 1
            if self.stack[-1].cnt > len(self.lines):
                self.lines.append("")
                self.error("너 지금 뭐하니?(조건문이 끝나지 않음)")
            line = self.lines[self.stack[-1].cnt - 1].strip()
            if line in {"유링게슝", "유리게슝"} or line.startswith("뭉탱이"):
                self.error("너 지금 뭐하니?(조건문이 끝나지 않음)")
            if line == "에이씨 나쁜 놈":
                self.stack[-1].control.pop()
                break

    def for_(self, line: str) -> None:
        line = line.split(" ")
        if "와의" not in line:
            self.error("죽이고싶은 멘트(반복문에 '와의'가 없음)")
        if "선" not in line:
            self.error("죽이고싶은 멘트(반복문에 '선'이 없음)")
        pos1, pos2 = line.index("와의"), line.index("선")
        name, value = " ".join(line[:pos1]), " ".join(line[pos1+1:pos2])
        if line[pos2+1:]:
            self.error("죽이고싶은 멘트('선' 뒤에 다른 멘트가 옴)")
        if not (
            self.stack[-1].control
            and self.stack[-1].control[-1].type == "for"
            and self.stack[-1].control[-1].start == self.stack[-1].cnt
        ):
            self.stack[-1].control.append(control("for", self.stack[-1].cnt))
            self.stack[-1].var[name] = 0
        value = self.calc(value)
        if value < 0:
            self.error(f"죽이고싶은 멘트({value}번 반복할 수는 없음)")
        if self.stack[-1].var[name] >= value:
            while True:
                self.stack[-1].cnt += 1
                if self.stack[-1].cnt > len(self.lines):
                    self.lines.append("")
                    self.error("죽이고싶은 멘트(반복문이 끝나지 않음)")
                line = self.lines[self.stack[-1].cnt - 1].strip()
                if line in {"유링게슝", "유리게슝"} or line.startswith("뭉탱이"):
                    self.error("죽이고싶은 멘트(반복문이 끝나지 않음)")
                if line == "에이씨 나쁜 놈":
                    self.stack[-1].control.pop()
                    break
        else:
            self.stack[-1].var[name] += 1

    def while_(self, line: str) -> None:
        line = line.split(" ")
        if "중에는!" not in line:
            self.error("인 방송 중에는!(반복문에 '중에는!'이 없음)")
        pos = line.index("중에는!")
        value = " ".join(line[:pos])
        if line[pos+1:]:
            self.error("인 방송 중에는!('중에는!' 뒤에 다른 멘트가 옴)")
        if not (
            self.stack[-1].control
            and self.stack[-1].control[-1].type == "while"
            and self.stack[-1].control[-1].start == self.stack[-1].cnt
        ):
            self.stack[-1].control.append(control("while", self.stack[-1].cnt))
        value = self.comp(value)
        if not value:
            while True:
                self.stack[-1].cnt += 1
                if self.stack[-1].cnt > len(self.lines):
                    self.lines.append("")
                    self.error("인 방송 중에는!(반복문이 끝나지 않음)")
                line = self.lines[self.stack[-1].cnt - 1].strip()
                if line in {"유링게슝", "유리게슝"} or line.startswith("뭉탱이"):
                    self.error("인 방송 중에는!(반복문이 끝나지 않음)")
                if line == "에이씨 나쁜 놈":
                    self.stack[-1].control.pop()
                    break

    def break_(self, line: str) -> None:
        if line != "나쁜 놈":
            self.error("음 주겨벌랑(실행 가능한 구문이 아님)")
        if not self.stack[-1].control:
            self.error("만나면 나쁜 친구~(시작한 제어문이 없음)")
        T = self.stack[-1].control[-1].type
        if T == "if":
            self.stack[-1].control.pop()
        elif T in {"for", "while"}:
            self.stack[-1].cnt = self.stack[-1].control[-1].start - 1

    def set(self, line: str) -> None:
        self.check_name(line)
        self.stack[-1].jump[line] = self.stack[-1].cnt

    def jump(self, line: str) -> None:
        if line not in self.stack[-1].jump:
            self.error(f"없어...('{line}'{end_letter(line, '', '이')}라는 라벨은 없음)")
        self.stack[-1].cnt = self.stack[-1].jump[line] - 1

    def assign_func(self, line: str) -> None:
        if "(" not in line:
            self.error("음 주겨벌랑(실행 가능한 구문이 아님)")
        name, line = line.split("(", 1)
        self.check_name(name)
        if not line.endswith(")"):
            self.error("음 주겨벌랑(실행 가능한 구문이 아님)")
        if (
            self.stack[-1].control
            and self.stack[-1].control[-1].type == "func"
        ):
            self.error("뭉탱이로 유링게슝(함수 안에서 함수를 작성함)")
        line = line[:-1]
        names = line.split(",")
        if len(names) == 1 and not names[0]:
            names = []
        else:
            for i in names:
                self.check_name(i)
        self.funcs[name] = {"start": self.stack[-1].cnt, "params": tuple(names)}
        while True:
            self.stack[-1].cnt += 1
            if self.stack[-1].cnt > len(self.lines):
                self.lines.append("")
                self.error("뭉탱이로 유링게슝(함수가 끝나지 않음)")
            line = self.lines[self.stack[-1].cnt - 1].strip()
            if line in {"유리게슝", "유링게슝"}:
                break

    def end_func(self, line: str) -> None:
        if line:
            self.error("음 주겨벌랑(실행 가능한 구문이 아님)")
        elif len(self.stack) == 1:
            self.error("뭉탱이로 유링게슝(대응하는 함수 선언 구문이 없음)")
        self.stack.pop()
        self.stack[-1].cnt -= 1
        self.return_value = 0

    def return_(self, line: str) -> None:
        if len(self.stack) == 1:
            self.error("그 뒤는 안돼 임마!(함수 밖에서 리턴을 사용함)")
        self.return_value = self.calc(line) if line else 0
        self.stack.pop()
        self.stack[-1].cnt -= 1

    def execute_line(self, line: str) -> None:
        if line.startswith("코 ") or line == "":
            return
        for i, keyword in enumerate(self.keywords):
            if line.startswith(
                    keyword
                    if keyword in {"죄송합니다", "안하니?", "유리게슝", "유링게슝"}
                    else keyword+" "
            ):
                line = line[len(keyword):].strip()
                do = self.exec[i]
                if not do:
                    self.error("음 주겨벌랑(실행 가능한 구문이 아님)")
                do(line)
                return
        if "(" in line:
            pos = line.index("(")
            self.call(line[:pos], line[pos:])
        else:
            self.error("음 주겨벌랑(실행 가능한 구문이 아님)")

    def execute(self, stdin="main.mte", stdout=None, *_) -> None:
        global print
        if not os.path.exists(stdin):
            print("이거나드셔:")
            print(f"음 주겨벌랑(방송 파일'{stdin}'{end_letter(stdin, '이', '가')} 없음)")
            sys.exit(1)
        with open(stdin, "r", encoding="utf-8") as f:
            self.lines = list(map(lambda x: x.strip(), f.readlines()))
        if stdout is None:
            print(f"Kodrip-lang python {self.version}")
            print("하더놈: sangchoo1201")
            print()
        else:
            self.stdout = stdout
            with open(self.stdout, "w") as f:
                f.write("")
            print = self.write_file
        self.stack[-1].cnt = 2
        if self.lines[0] != "안녕하세요 저는":
            self.error("자~숙하자~(방송이 '안녕하세요 저는'으로 시작하지 않음)")
        while True:
            if self.stack[-1].cnt > len(self.lines):
                self.lines.append("")
                self.error("자~숙하자~(방송이 '죄송합니다'로 끝나지 않음)")
            self.execute_line(self.lines[self.stack[-1].cnt-1].strip())
            self.stack[-1].cnt += 1


if __name__ == "__main__":
    env = compiler()
    env.execute(*sys.argv[1:])
