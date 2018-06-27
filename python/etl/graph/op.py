from .variable import Variable
import inspect

class Op(object):

    def __init__(self, **kwargs):
        for k in kwargs:
            setattr(self, k, kwargs[k])
        self.attribs = kwargs.keys()

    def execute(self, inputs):
        return inputs

    def serialize(self):
        attribs = getattr(self, 'attribs', inspect.getargspec(self.__init__).args[1:])
        config = {attr: getattr(self, attr) for attr in attribs}
        return config

    @classmethod
    def deserialize(cls, config):
        return cls(**config)

    def __call__(self, inputs=None):
        if type(inputs) in (list, tuple):
            inputs = list(inputs)
            for inp in inputs:
                if type(inp) != Variable:
                    raise TypeError("Received input of unexpected type: " + str(type(inp)) + ".")
        elif not isinstance(inputs, Variable):
            raise TypeError("Received input of unexpected type: " + str(type(inputs)) + ".")
        output = Variable()
        output.op = self
        output.inputs = inputs
        return output
