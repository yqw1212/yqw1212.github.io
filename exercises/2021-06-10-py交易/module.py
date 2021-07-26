import bytecode_graph as bytecode_graph
from dis import opmap
import sys
import marshal

pyc_file = open(sys.argv[1], "rb").read()
pyc = marshal.loads(pyc_file[8:])

for x in pyc.co_consts:
    if hasattr(x, 'co_code'):
        bcg = bytecode_graph.BytecodeGraph(x)
        graph = bytecode_graph.Render(bcg, x).dot()
        try:
            graph.write_png(x.co_name + '.png')
        except Exception, e:
            print(e)
            print(x.co_name)

bcg = bytecode_graph.BytecodeGraph(pyc)
graph = bytecode_graph.Render(bcg, pyc).dot()
graph.write_png('module.png')