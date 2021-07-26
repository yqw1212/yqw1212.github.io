import bytecode_graph 
from dis import opmap
import sys
import marshal

pyc_file = open(sys.argv[1], "rb").read()
pyc = marshal.loads(pyc_file[8:])
bcg = bytecode_graph.BytecodeGraph(pyc)
graph = bytecode_graph.Render(bcg, pyc).dot()
graph.write_png('example_graph.png')