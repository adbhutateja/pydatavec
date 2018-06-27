from ...graph import Op

class ColOp(Op):

    def __init__(self, columns):
        if type(columns) not in (list, tuple):
            columns = [columns]
        super(ColOp, self).__init__(columns=columns)

    def execute(self, inputs):
        inputs = inputs[:]
        outputs = []
        cols = self.columns
        for x in inputs:
            for c in cols:
                x[c] = self.transform(x[c])
            outputs.append(x)
        return outputs


class ToInt(ColOp):
    def transform(self, x):
        return int(float(x))


class ToFloat(ColOp):
    def transform(self, x):
        return float(x)


class ToUpper(ColOp):
    def transform(self, x):
        return x.upper()


class ToLower(ColOp):
    def transform(self, x):
        return x.lower()
