import interpreter


def run(stdin="main.mte", stdout=""):
    with open(stdin, "r", encoding="utf-8") as f:
        file_text = f.read()

    file_text = file_text.strip()
    start_pos = file_text.find("안녕하세요 저는")
    end_pos = file_text.find("죄송합니다")

    if start_pos == -1:
        print("자~숙하자~: 코드가 '안녕하세요 저는'으로 시작하지 않습니다")
    if end_pos == -1:
        print("자~숙하자~: 코드가 '죄송합니다'로 끝나지 않습니다")

    file_text = file_text[start_pos + len("안녕하세요 저는"):end_pos]

    result, error = interpreter.run(stdin, file_text, stdout)

    if error:
        print(error.as_string())
