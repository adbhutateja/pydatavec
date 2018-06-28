from ...graph import Op

class ColOp(Op):

    def __init__(self, columns=None, **kwargs):
        if type(columns) is int:
            columns = [columns]
        super(ColOp, self).__init__(columns=columns, **kwargs)

    def execute(self, inputs):
        inputs = inputs[:]
        outputs = []
        cols = self.columns
        if cols is None:
            cols = list(range(len(inputs[0])))
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


class Replace(ColOp):

    def __init__(self, str1, str2, cols=None):
        super(Replace, self).__init__(str1=str1, str2=str2, cols=cols)

    def transform(self, x):
        return x.replace(self.str1, self.str2)
