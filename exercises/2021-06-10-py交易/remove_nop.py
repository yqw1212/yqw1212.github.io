import bytecode_graph 
from dis import opmap
import sys
import marshal
from opcode import *

def remove_nop_inner(co):
    try:
        bcg = bytecode_graph.BytecodeGraph(co)
        nodes = [x for x in bcg.nodes()]
        for n in nodes:
            if n.opcode == opmap['NOP']:
                bcg.delete_node(n)
        return bcg.get_code()
    except:
        pass

def remove_nop(co):
    #co = remove_nop_inner(co)

    inner = list()
    for i in range(len(co.co_consts)):
        if hasattr(co.co_consts[i], 'co_code'):
            inner.append(remove_nop_inner(co.co_consts[i]))
        else:
            inner.append(co.co_consts[i])

    co.co_consts = tuple(inner)

    return co

pyc_file = open(sys.argv[1], "rb").read()
pyc = marshal.loads(pyc_file[8:])
pyc = remove_nop(pyc)
bcg = bytecode_graph.BytecodeGraph(pyc)
graph = bytecode_graph.Render(bcg, pyc).dot()
graph.write_png('remove_nop_graph.png')