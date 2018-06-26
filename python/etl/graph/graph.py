from .op import Op
from .variable import Variable


class Graph(Op):

    def __init__(self, inputs, outputs):
        if type(inputs) != list:
            if type(inputs) is tuple:
                inputs = list(inputs)
            else:
                inputs = [inputs]
        self._list_output = True
        if type(outputs) != list:
            if type(outputs) is tuple:
                outputs = list(outputs)
            else:
                self._list_output = False
                outputs = [outputs]
        self.inputs = inputs
        self.outputs = outputs
        self.traverse_graph()

    def traverse_graph(self):
        vars = []
        temp = self.outputs[:]
        while(temp):
            temp2 = []
            for var in temp:
                inp = var.inputs
                if type(inp) is list:
                    temp2 += inp
                elif isinstance(inp, Variable):
                    temp2.append(inp)
            vars += temp
            temp = temp2
        self.nodes = list(set([x.op for x in vars if x.op is not None]))

    def execute(self, inputs):
        if type(inputs) != list:
            if type(inputs) is tuple:
                inputs = list(inputs)
            else:
                inputs = [inputs]
        for val, var in zip(inputs, self.inputs):
            var.value = val
            var._force_value = True
        outputs = [o.eval() for o in self.outputs]
        if self._list_output:
            return outputs
        else:
            return outputs[0]

    def __call__(self, inputs):
        if type(inputs) in (list, tuple):
            inputs = list(inputs)
            for inp in inputs:
                if isinstance(inp, Variable):
                    raise TypeError("Received input of unexpected type: " + str(type(inp)) + ".")
        else:
            raise TypeError("Received input of unexpected type: " + str(type(inp)) + ".")
        outputs = [Variable(op=self, inputs=inputs, index=i) for i in range(len(self.outputs))]
        if self._list_output:
            return outputs
        else:
            return outputs[0]

    def serialize(self):
        nodes = self.nodes
        node_configs = [{'class_name': node.__class__.__name__, 'config': node.serialize()} for node in nodes]
        node_to_index = {nodes[i] : i  for i in range(len(nodes))}
        var_to_index = {}
        def get_var_index(var):
            idx = var_to_index.get(var)
            if idx is None:
                idx = len(var_to_index)
                var_to_index[var] = idx
            return idx
        
        connectome = {}
        vars = self.outputs[:]
        while(vars):
            temp = []
            for var in vars:
                var_id = get_var_index(var)
                op = var.op
                if op is not None:
                    op = node_to_index[op]
                inp = var.inputs
                if isinstance(inp, list):
                    temp += inp
                    inp = [get_var_index(x) for x in inp]
                elif isinstance(inp, Variable):
                    temp.append(inp)
                    inp = get_var_index(inp)
                connectome[var_id] = {'op': op, 'inputs': inp}
            vars = temp
        outputs = [get_var_index(o) for o in self.outputs]
        inputs = [get_var_index(i) for i in self.inputs]
        config = {}
        config['inputs'] = inputs
        config['outputs'] = outputs
        config['nodes'] = node_configs
        config['connectome'] = connectome
        config['_list_output'] = self._list_output
        return config

    @staticmethod
    def _get_var(index_to_var, idx):
        var = index_to_var.get(idx)
        if var is None:
            var = Variable()
            index_to_var[idx] = var
        return var

    @classmethod
    def deserialize(cls, config):

        index_to_var = {}
        get_var = Graph._get_var
        nodes = []
        exec('from ..ops import *')
        for node in config['nodes']:
            node_class = node['class_name']
            node_class = globals()[node_class]
            nodes.append(node_class.deserialize(node['config']))

        connectome = config['connectome']
        for k in connectome:
            v = connectome[k]
            op = v['op']
            inputs = v['inputs']
            if op is not None:
                op = nodes[op]
            if type(inputs) is list:
                inputs = [get_var(index_to_var, x) for x in inputs]
            elif type(inputs) is int:
                inputs = get_var(index_to_var, inputs)
            var = get_var(index_to_var, k)
            var.op = op
            var.inputs = inputs

        inputs = [get_var(index_to_var, i) for i in config['inputs']]
        outputs = [get_var(index_to_var, i) for i in config['outputs']]        
        g = cls(inputs, outputs)
        g._list_output = config['_list_output']
        return g





