from etl import *

a = Variable()
b = Op()(a)

g = Graph(a, b)

s = g.serialize()

g2 = Graph.deserialize(s)

