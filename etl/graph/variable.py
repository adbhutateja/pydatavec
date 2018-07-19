class Variable(object):

    def __init__(self, value=None, op=None, inputs=None, index=None):
        self.value = value
        self.op = op
        self.inputs = inputs
        self.index = index
        self._force_value = False  # allows sub graph execution
    def eval(self):
        if self._force_value:
            self._force_value = False
            return self.value
        if not self.op:
            return self.value
        inputs = self.inputs
        if type(inputs) is list:
            inputs = [x.eval() for x in inputs]
        elif isinstance(inputs, Variable):
            inputs = inputs.eval()
        if self.op.__class__.__name__ == 'Graph':
            self.value = self.op.execute(inputs)[self.index]
        else:
            self.value = self.op.execute(inputs)
        return self.value
