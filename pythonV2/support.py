from unicodedata import east_asian_width


def get_width(text):
    return sum(2 if east_asian_width(c) in 'FWA' else 1 for c in text)


def draw_arrow(text, pos_start, pos_end):
    result = ''

    index_start = max(text.rfind('\n', 0, pos_start.index), 0)
    index_end = text.find('\n', index_start + 1)
    if index_end < 0:
        index_end = len(text)

    line_count = pos_end.line - pos_start.line + 1
    for i in range(line_count):
        line = text[index_start:index_end]
        column_start = pos_start.column if i == 0 else 0
        column_start = get_width(line[:column_start])
        column_end = pos_end.column if i == line_count - 1 else len(line)
        column_end = get_width(line[:column_end])-1+get_width(line[column_end] if column_end < len(line) else ' ')

        result += line + '\n'
        result += ' ' * column_start + '^' * (column_end - column_start)

        index_start = index_end
        index_end = text.find('\n', index_start + 1)
        if index_end < 0:
            index_end = len(text)

    return result.replace('\t', ' ')


if __name__ == '__main__':
    from position import Position
    txt = "a가efgsdf"
    print(draw_arrow(txt, Position(0, 0, 0, "a", txt), Position(0, 0, 5, "a", txt)))
