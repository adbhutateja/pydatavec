from ...graph import Op

class Select(Op):
    def __init__(self, cols):
        if type(cols) is int:
            cols = [cols]
        super(Select, self).__init__(cols=cols)

    def execute(self, inputs):
        row_len = len(inputs[0])
        cols = self.cols
        return [[row[i] for i in range(row_len) if i in cols] for row in inputs]


class Head(Op):
    def __init__(self, size):
        super(Head, self).__init__(size=size)

    def execute(self, inputs):
        return inputs[:self.size]


class Tail(Op):
    def __init__(self, size):
        super(Tail, self).__init__(size=size)

    def execute(self, inputs):
        return inputs[self.size:]

