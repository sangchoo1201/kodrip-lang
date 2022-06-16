class RTResult:
    def __init__(self):
        self.reset()

    def reset(self):
        self.value = None
        self.error = None
        self.return_value = None

    def register(self, res):
        self.error = res.error
        self.return_value = res.return_value
        return res.value

    def success(self, value):
        self.reset()
        self.value = value
        return self

    def success_return(self, value):
        self.reset()
        self.return_value = value
        return self

    def failure(self, error):
        self.reset()
        self.error = error
        return self

    def should_return(self):
        return (
            self.error or
            self.return_value is not None
        )


# Context
class Context:
    def __init__(self, name, parent=None, entry_pos=None):
        self.parent = parent
        self.name = name
        self.entry_pos = entry_pos
        self.symbol_table = None


class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def get(self, name):
        value = self.symbols.get(name)
        if value is not None:
            return value
        if self.parent is not None:
            return self.parent.get(name)
        return None

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]
