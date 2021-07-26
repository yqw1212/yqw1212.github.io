import marshal, sys, opcode, types, dis

NOP = 9

HAVE_ARGUMENT = 90

JUMP_FORWARD = 110
JUMP_IF_FALSE_OR_POP = 111
JUMP_IF_TRUE_OR_POP = 112
JUMP_ABSOLUTE = 113
POP_JUMP_IF_FALSE = 114
POP_JUMP_IF_TRUE = 115

CONTINUE_LOOP = 119
FOR_ITER = 93

RETURN_VALUE = 83

used_set = set()

def deconf_inner(code, now):
    global used_set

    while code[now] != RETURN_VALUE:
        if now in used_set:
            break
        used_set.add(now)
        if code[now] >= HAVE_ARGUMENT:
            used_set.add(now+1)
            used_set.add(now+2)
        op = code[now]

        #print(str(now) + " " + opcode.opname[op])

        if op == JUMP_FORWARD:
            arg = code[now+2] << 8 | code[now+1]
            now += arg + 3
            continue

        elif op == JUMP_ABSOLUTE:
            arg = code[now+2] << 8 | code[now+1]
            now = arg
            continue

        elif op == JUMP_IF_TRUE_OR_POP:
            arg = code[now+2] << 8 | code[now+1] 
            deconf_inner(code, arg)

        elif op == JUMP_IF_FALSE_OR_POP:
            arg = code[now+2] << 8 | code[now+1] 
            deconf_inner(code, arg)

        elif op == POP_JUMP_IF_TRUE:
            arg = code[now+2] << 8 | code[now+1] 
            deconf_inner(code, arg)

        elif op == POP_JUMP_IF_FALSE: 
            arg = code[now+2] << 8 | code[now+1] 
            deconf_inner(code, arg)

        elif op == CONTINUE_LOOP:
            arg = code[now+2] << 8 | code[now+1] 
            deconf_inner(code, arg)

        elif op == FOR_ITER: 
            arg = code[now+2] << 8 | code[now+1] 
            deconf_inner(code, now + arg + 3)

        if op < HAVE_ARGUMENT:
            now += 1
        else:
            now += 3

    used_set.add(now)
    if code[now] >= HAVE_ARGUMENT:
        used_set.add(now+1)
        used_set.add(now+2)

def deconf(code):
    global used_set

    used_set = set() #Remember to clean up used_set for every target function

    cod = list(map(ord, code))
    deconf_inner(cod, 0)

    for i in range(len(cod)):
        if i not in used_set:
            cod[i] = NOP

    return "".join(list(map(chr, cod)))

with open(sys.argv[1], 'rb') as f:
    header = f.read(8)
    code = marshal.load(f)

'''
print(code.co_consts[3].co_name)
print(dis.dis(deconf(code.co_consts[3].co_code)))
'''

consts = list()

for i in range(len(code.co_consts)):
    if hasattr(code.co_consts[i], 'co_code'):
        consts.append(types.CodeType(code.co_consts[i].co_argcount,
            # c.co_kwonlyargcount,  Add this in Python3
            code.co_consts[i].co_nlocals,
            code.co_consts[i].co_stacksize,
            code.co_consts[i].co_flags,
            deconf(code.co_consts[i].co_code),
            code.co_consts[i].co_consts,
            code.co_consts[i].co_names,
            code.co_consts[i].co_varnames,
            code.co_consts[i].co_filename,
            code.co_consts[i].co_name,
            code.co_consts[i].co_firstlineno,
            code.co_consts[i].co_lnotab,   # In general, You should adjust this
            code.co_consts[i].co_freevars,
            code.co_consts[i].co_cellvars))
    else:
        consts.append(code.co_consts[i])

mode = types.CodeType(code.co_argcount,
    # c.co_kwonlyargcount,  Add this in Python3
    code.co_nlocals,
    code.co_stacksize,
    code.co_flags,
    deconf(code.co_code),
    tuple(consts),
    code.co_names,
    code.co_varnames,
    code.co_filename,
    code.co_name,
    code.co_firstlineno,
    code.co_lnotab,   # In general, You should adjust this
    code.co_freevars,
    code.co_cellvars)

f = open(sys.argv[1]+".mod", 'wb') 
f.write(header)
marshal.dump(mode, f)
