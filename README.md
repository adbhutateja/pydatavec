# ETL library for SKIL

## Key features:

* Define transform process as a graph in python
* Test transform process on dummy data in python
* Get serialized (json) graph
* Execute the graph in java on real data
    

## Example:

* Read a CSV file
* Convert first row to int
* Convert second row to upper case
* Replace all occurances of "NULL" in third column with 0.

```python
from etl import *

input = Variable()  # empty input for graph consistency
csv = CSVReader('test.csv')(input)
csv = ToInt(0)(csv)
csv = ToUpper(1)(csv)
csv = Replace("NULL", "0", 2)(csv)
csv = ToInt(2)(csv) # "0" -> 0

graph = Graph(input, csv)

graph_json = graph.serialize()


```
