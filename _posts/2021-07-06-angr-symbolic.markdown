---
layout: post
title:  Angr(2)
date:   2021-07-06 00:01:01 +0300
image:  2021-07-06-skyscrapers.jpg
tags:   [ctf,reverse,angr]
---

## 03_angr_symbolic_registers

这题主要是因为angr在处理复杂格式的字符串scanf()输入的时候不是很好，我们可以直接将符号之注入寄存器，也就是主要学会符号化寄存器

main

```assembly
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int v3; // ebx
  int v4; // eax
  int v5; // edx
  int v6; // ST1C_4
  unsigned int v7; // ST14_4
  unsigned int v9; // [esp+8h] [ebp-10h]
  int v10; // [esp+Ch] [ebp-Ch]

  print_msg();
  printf("Enter the password: ");
  v4 = get_user_input();
  v6 = v5;
  v7 = complex_function_1(v4);
  v9 = complex_function_2(v3);
  v10 = complex_function_3(v6);
  if ( v7 || v9 || v10 )
    puts("Try again.");
  else
    puts("Good Job.");
  return 0;
}
```

get_user_input

```assembly
int get_user_input()
{
  int v1; // [esp+0h] [ebp-18h]
  int v2; // [esp+4h] [ebp-14h]
  int v3; // [esp+8h] [ebp-10h]
  unsigned int v4; // [esp+Ch] [ebp-Ch]

  v4 = __readgsdword(0x14u);
  __isoc99_scanf("%x %x %x", &v1, &v2, &v3);
  return v1;
}
```

这次的输入是一个复杂的格式化字符串，`"%x %x %x"`意味着使用三个十六进制值作为输入，看一下汇编代码

```assembly
.text:08048876                 push    offset aXXX     ; "%x %x %x"
.text:0804887B                 call    ___isoc99_scanf
.text:08048880                 add     esp, 10h
.text:08048883                 mov     ecx, [ebp+var_18]
.text:08048886                 mov     eax, ecx
.text:08048888                 mov     ecx, [ebp+var_14]
.text:0804888B                 mov     ebx, ecx
.text:0804888D                 mov     ecx, [ebp+var_10]
.text:08048890                 mov     edx, ecx
```

可以得知输入的三个值最后是分别赋值给了EAX，EBX，EDX寄存器，所以要控制输入只需要控制这三个寄存器的值就行.

complex_function_1

```assembly
unsigned int __cdecl complex_function_1(int a1)
{
  return (((((((((((((((((((a1 ^ 0x221EAE23) + 1943863989) ^ 0x66601FED) - 83740949) ^ 0x6D77A1B4) + 2131817319) ^ 0x4312DEE6)
                   + 475856759) ^ 0xCCF1CE68)
                 + 107800371) ^ 0x8207BD30)
               + 826826807) ^ 0x41936615)
             + 1251292781) ^ 0x74CA67D8)
           + 2053741170) ^ 0x9C162D98)
         - 444090937) ^ 0xBA325959)
       + 747736473;
}
```

complex_function_2

```assembly
unsigned int __cdecl complex_function_2(int a1)
{
  return ((((((((((((((((((((a1 - 564117216) ^ 0x79A22076) - 1060914832) ^ 0xB9718A59) - 2108913029) ^ 0x99547626)
                     - 448148732
                     + 796556377) ^ 0x32FF23C5)
                   + 641881611) ^ 0x8AD12165)
                 - 62182379) ^ 0xD0DF16FE)
               - 233298404) ^ 0x8F15E734)
             + 615145695) ^ 0xFA757053)
           + 1683850174) ^ 0xC748AA81)
         + 768426521) ^ 0x216F031D)
       - 1519599985;
}
```

complex_function_3

```assembly
unsigned int __cdecl complex_function_3(int a1)
{
  return ((((((a1 - 1969053699) ^ 0xACD1FF8C) + 1063335477) ^ 0x10820E6B) - 1436537775) ^ 0x2999881D) + 492215691;
}
```

#### 状态预设

除了使用`.entry_state()` 创建 state 对象, 我们还可以根据需要使用其他构造函数创建 state:

|        名称        |                             描述                             |
| :----------------: | :----------------------------------------------------------: |
|  `.entry_state()`  |           构造一个已经准备好从函数入口点执行的状态           |
|   `.blank_state`   | 构造一个“空状态”，它的大多数数据都是未初始化的。当使用未初始化的的数据时，一个不受约束的符号值将会被返回 |
|   `.call_state`    |             构造一个已经准备好执行某个函数的状态             |
| `.full_init_state` | 构造一个已经执行过所有与需要执行的初始化函数，并准备从函数入口点执行的状态。比如，共享库构造函数（constructor）或预初始化器。当这些执行完之后，程序将会跳到入口点 |

#### 位向量(bitvector)

更应该准确的说是符号位向量，符号位向量是angr用于将符号值注入程序的数据类型。这些将是angr将解决的方程式的“ x”，也就是约束求解时的自变量。可以通过 `BVV(value,size)` 和 `BVS( name, size)` 接口创建位向量，也可以用 FPV 和 FPS 来创建浮点值和符号

```assembly
# Angr doesn't currently support reading multiple things with scanf (Ex: 
# scanf("%u %u).) You will have to tell the simulation engine to begin the
# program after scanf is called and manually inject the symbols into registers.

import angr
import claripy
import sys

def main(argv):
  project = angr.Project("./03_angr_symbolic_registers")

  # Sometimes, you want to specify where the program should start. The variable
  # start_address will specify where the symbolic execution engine should begin.
  # Note that we are using blank_state, not entry_state.
  # 这次可以不用从main函数的开头开始，
  # 直接跳过get_user_input()函数，直接设置寄存器eax, ebx, edx
  '''
  .text:080488BF                 push    offset aEnterThePasswo ; "Enter the password: "
  .text:080488C4                 call    _printf
  .text:080488C9                 add     esp, 10h
  .text:080488CC                 call    get_user_input
  .text:080488D1                 mov     [ebp+var_14], eax
  .text:080488D4                 mov     [ebp+var_10], ebx
  .text:080488D7                 mov     [ebp+var_C], edx
  .text:080488DA                 sub     esp, 0Ch
  .text:080488DD                 push    [ebp+var_14]
  .text:080488E0                 call    complex_function_1
  '''
  start_address = 0x80488d1  # :integer (probably hexadecimal)
  # 在start_address地址创建一个新状态
  initial_state = project.factory.blank_state(addr=start_address)

  # Create a symbolic bitvector (the datatype Angr uses to inject symbolic
  # values into the binary.) The first parameter is just a name Angr uses
  # to reference it. 
  # You will have to construct multiple bitvectors. Copy the two lines below
  # and change the variable names. To figure out how many (and of what size)
  # you need, dissassemble the binary and determine the format parameter passed
  # to scanf.
  # 使用claripy通过BVS()方法生成三个位向量。
  # 此方法有两个参数：第一个是angr用来引用位向量的名称，第二个是位向量本身的大小（以位为单位）。
  # 由于符号值存储在寄存器中，并且寄存器的长度为32位，因此位向量的大小将为32位
  password_size_in_bits = 32  # :integer
  password0 = claripy.BVS('password0', password_size_in_bits)
  password1 = claripy.BVS('password1', password_size_in_bits)
  password2 = claripy.BVS('password2', password_size_in_bits)

  # 访问寄存器
  # Set a register to a symbolic value. This is one way to inject symbols into
  # the program.
  # initial_state.regs stores a number of convenient attributes that reference
  # registers by name. For example, to set eax to password0, use:
  #
  # initial_state.regs.eax = password0
  #
  # You will have to set multiple registers to distinct bitvectors. Copy and
  # paste the line below and change the register. To determine which registers
  # to inject which symbol, dissassemble the binary and look at the instructions
  # immediately following the call to scanf.
  # 通过 state.regs 对象的属性访问以及修改寄存器的数据
  initial_state.regs.eax = password0
  initial_state.regs.ebx = password1
  initial_state.regs.edx = password2

  simulation = project.factory.simgr(initial_state)

  def is_successful(state):
    stdout_output = state.posix.dumps(sys.stdout.fileno())
    return b'Good Job.' in stdout_output

  def should_abort(state):
    stdout_output = state.posix.dumps(sys.stdout.fileno())
    return b'Try again.' in stdout_output

  simulation.explore(find=is_successful, avoid=should_abort)

  if simulation.found:
    solution_state = simulation.found[0]

    # 约束求解
    # Solve for the symbolic values. If there are multiple solutions, we only
    # care about one, so we can use eval, which returns any (but only one)
    # solution. Pass eval the bitvector you want to solve for.
    # 使用state.solver.eval(symbol)对各个断言进行评测来求出一个合法的符号值（若有多个合法值，返回其中的一个）
    solution0 = solution_state.se.eval(password0)
    solution1 = solution_state.se.eval(password1) 
    solution2 = solution_state.se.eval(password2)

    # Aggregate and format the solutions you computed above, and then print
    # the full string. Pay attention to the order of the integers, and the
    # expected base (decimal, octal, hexadecimal, etc).
    solution = ' '.join(map('{:x}'.format, [ solution0, solution1, solution2 ]))  # :string
    print(solution)
  else:
    raise Exception('Could not find the solution')

if __name__ == '__main__':
  main(sys.argv)

```

## 04_angr_symbolic_stack

上一题学习了符号化寄存器，这题主要是学习如何符号化栈上的值

main

```assembly
int __cdecl main(int argc, const char **argv, const char **envp)
{
  print_msg();
  printf("Enter the password: ");
  handle_user();
  return 0;
}
```

handle_user

```assembly
int handle_user()
{
  int result; // eax
  int v1; // [esp+8h] [ebp-10h]
  int v2; // [esp+Ch] [ebp-Ch]

  __isoc99_scanf("%u %u", &v2, &v1);
  v2 = complex_function0(v2);
  v1 = complex_function1(v1);
  if ( v2 == 1726148847 && v1 == -1738470817 )
    result = puts("Good Job.");
  else
    result = puts("Try again.");
  return result;
}
```

与上一题不同，这一题scanf读入的内容保存在了栈上，查看汇编语言。

```assembly
.text:0804867F                 sub     esp, 4
.text:08048682                 lea     eax, [ebp+var_10]
.text:08048685                 push    eax
.text:08048686                 lea     eax, [ebp+var_C]
.text:08048689                 push    eax
.text:0804868A                 push    offset aUU      ; "%u %u"
.text:0804868F                 call    ___isoc99_scanf
.text:08048694                 add     esp, 10h
.text:08048697                 mov     eax, [ebp+var_C] ; 参数1,[ebp-0Ch]
.text:0804869A                 sub     esp, 0Ch
.text:0804869D                 push    eax
.text:0804869E                 call    complex_function0
.text:080486A3                 add     esp, 10h
.text:080486A6                 mov     [ebp+var_C], eax
.text:080486A9                 mov     eax, [ebp+var_10] ; 参数2,[ebp-10h]
.text:080486AC                 sub     esp, 0Ch
.text:080486AF                 push    eax
.text:080486B0                 call    complex_function1
.text:080486B5                 add     esp, 10h
```

complex_function0

```assembly
int __cdecl complex_function0(int a1)
{
  return a1 ^ 0x2EB80E9D;
}
```

complex_function1

```assembly
unsigned int __cdecl complex_function1(int a1)
{
  return a1 ^ 0xDCA14C40;
}
```

使用angr对栈上的值进行符号化处理

```assembly
# This challenge will be more challenging than the previous challenges that you
# have encountered thus far. Since the goal of this CTF is to teach symbolic
# execution and not how to construct stack frames, these comments will work you
# through understanding what is on the stack.


import angr
import claripy
import sys

def main(argv):
  project = angr.Project("./04_angr_symbolic_stack")

  # For this challenge, we want to begin after the call to scanf.
  #
  # Now, the question is: do we start on the instruction immediately following
  # scanf (add $0x10,%esp), or the instruction following that (not shown)?
  # Consider what the 'add $0x10,%esp' is doing. Hint: it has to do with the
  # scanf parameters that are pushed to the stack before calling the function.
  # Given that we are not calling scanf in our Angr simulation, where should we
  # start?
  start_address = 0x8048697
  initial_state = project.factory.blank_state(addr=start_address)

  # We are jumping into the middle of a function! Therefore, we need to account
  # for how the function constructs the stack. The second instruction of the
  # function is:
  #   mov    %esp,%ebp
  # At which point it allocates the part of the stack frame we plan to target:
  #   sub    $0x18,%esp
  # Note the value of esp relative to ebp. The space between them is (usually)
  # the stack space. Since esp was decreased by 0x18
  #
  #        /-------- The stack --------\
  # ebp -> |                           |
  #        |---------------------------|
  #         . . . (total of 0x18 bytes)
  #         . . . Somewhere in here is
  #         . . . the data that stores
  #         . . . the result of scanf.
  # esp -> |                           |
  #        \---------------------------/
  #
  # Since we are starting after scanf, we are skipping this stack construction
  # step. To make up for this, we need to construct the stack ourselves. Let us
  # start by initializing ebp in the exact same way the program does.
  # 先将ESP指针恢复到和EBP指针一致，恢复栈帧初始状态，方便计算
  initial_state.regs.ebp = initial_state.regs.esp

  # scanf("%u %u") needs to be replaced by injecting four bitvectors. The
  # reason for this is that Angr does not (currently) automatically inject
  # symbols if scanf has more than one input parameter. This means Angr can
  # handle 'scanf("%u")', but not 'scanf("%u %u")'.
  password0 = claripy.BVS('password0', 32)
  password1 = claripy.BVS('password1', 32)

  # Here is the hard part. We need to figure out what the stack looks like, at
  # least well enough to inject our symbols where we want them. In order to do
  # that, let's figure out what the parameters of scanf are:
  #   sub    $0x4,%esp
  #   lea    -0x10(%ebp),%eax
  #   push   %eax
  #   lea    -0xc(%ebp),%eax
  #   push   %eax
  #   push   $0x80489c3
  #   call   8048370 <__isoc99_scanf@plt>
  #   add    $0x10,%esp 
  #   汇编：
  #   sub     esp, 4
  #   lea     eax, [ebp+var_10]
  #   push    eax
  #   lea     eax, [ebp+var_C]
  #   push    eax
  #   push    offset aUU      ; "%u %u"
  #   call    ___isoc99_scanf
  #   add     esp, 10h
  # As you can see, the call to scanf looks like this:
  # scanf(  0x80489c3,   ebp - 0xc,   ebp - 0x10  )
  #      format_string    password0    password1
  #  From this, we can construct our new, more accurate stack diagram:
  #
  #            /-------- The stack --------\
  # ebp ->     |          padding          |
  #            |---------------------------|
  # ebp - 0x01 |       more padding        |
  #            |---------------------------|
  # ebp - 0x02 |     even more padding     |
  #            |---------------------------|
  #                        . . .               <- How much padding? Hint: how
  #            |---------------------------|      many bytes is password0?
  # ebp - 0x0b |   password0, second byte  |
  #            |---------------------------|
  # ebp - 0x0c |   password0, first byte   |
  #            |---------------------------|
  # ebp - 0x0d |   password1, last byte    |
  #            |---------------------------|
  #                        . . .
  #            |---------------------------|
  # ebp - 0x10 |   password1, first byte   |
  #            |---------------------------|
  #                        . . .
  #            |---------------------------|
  # esp ->     |                           |
  #            \---------------------------/
  #
  # Figure out how much space there is and allocate the necessary padding to
  # the stack by decrementing esp before you push the password bitvectors.
  padding_length_in_bytes = 4 + 4  # :integer
  initial_state.regs.esp -= padding_length_in_bytes

  # Push the variables to the stack. Make sure to push them in the right order!
  # The syntax for the following function is:
  #
  # initial_state.stack_push(bitvector)
  #
  # This will push the bitvector on the stack, and increment esp the correct
  # amount.
  initial_state.stack_push(password0)  # :bitvector (claripy.BVS, claripy.BVV, claripy.BV)
  initial_state.stack_push(password1)

  simulation = project.factory.simgr(initial_state)

  def is_successful(state):
    stdout_output = state.posix.dumps(sys.stdout.fileno())
    return b'Good Job.' in stdout_output

  def should_abort(state):
    stdout_output = state.posix.dumps(sys.stdout.fileno())
    return b'Try again.' in stdout_output

  simulation.explore(find=is_successful, avoid=should_abort)

  if simulation.found:
    solution_state = simulation.found[0]

    solution0 = solution_state.se.eval(password0)
    solution1 = solution_state.se.eval(password1)

    solution = ' '.join(map(str, [ solution0, solution1 ]))
    print(solution)
  else:
    raise Exception('Could not find the solution')

if __name__ == '__main__':
  main(sys.argv)

```

### eval

- `solver.eval(expression)` 将会解出一个可行解
- `solver.eval_one(expression)`将会给出一个表达式的可行解，若有多个可行解，则抛出异常。
- `solver.eval_upto(expression, n)`将会给出最多n个可行解，如果不足n个就给出所有的可行解。
- `solver.eval_exact(expression, n)`将会给出n个可行解，如果解的个数不等于n个，将会抛出异常。
- `solver.min(expression)`将会给出最小可行解
- `solver.max(expression)`将会给出最大可行解

另外还有还有`cast_to`可以接收一个参数来指定把结果映射到哪种数据类型。目前这个参数只能是`str`，它将会以字符串形式展示返回的结果

## 05_angr_symbolic_memory

符号化内存

main

```assembly
int __cdecl main(int argc, const char **argv, const char **envp)
{
  signed int i; // [esp+Ch] [ebp-Ch]

  memset(user_input, 0, 0x21u);
  print_msg();
  printf("Enter the password: ");
  __isoc99_scanf("%8s %8s %8s %8s", user_input, &unk_A29FAA8, &unk_A29FAB0, &unk_A29FAB8);
  for ( i = 0; i <= 31; ++i )
    *(_BYTE *)(i + 170523296) = complex_function(*(char *)(i + 170523296), i);
  if ( !strncmp(user_input, "QUNKPPITSSQFDTYAZZCZABBUAKBMLUHX", 0x20u) )
    puts("Good Job.");
  else
    puts("Try again.");
  return 0;
}
```

点击scanf的变量发现将读入的内容存在了.bss段。

```assembly
.bss:0A29FAA0 user_input      db 8 dup(?)             ; DATA XREF: main+18↑o
.bss:0A29FAA0                                         ; main+4C↑o ...
.bss:0A29FAA8 unk_A29FAA8     db    ? ;               ; DATA XREF: main+47↑o
.bss:0A29FAA9                 db    ? ;
.bss:0A29FAAA                 db    ? ;
.bss:0A29FAAB                 db    ? ;
.bss:0A29FAAC                 db    ? ;
.bss:0A29FAAD                 db    ? ;
.bss:0A29FAAE                 db    ? ;
.bss:0A29FAAF                 db    ? ;
.bss:0A29FAB0 unk_A29FAB0     db    ? ;               ; DATA XREF: main+42↑o
.bss:0A29FAB1                 db    ? ;
.bss:0A29FAB2                 db    ? ;
.bss:0A29FAB3                 db    ? ;
.bss:0A29FAB4                 db    ? ;
.bss:0A29FAB5                 db    ? ;
.bss:0A29FAB6                 db    ? ;
.bss:0A29FAB7                 db    ? ;
.bss:0A29FAB8 unk_A29FAB8     db    ? ;               ; DATA XREF: main+3D↑o
.bss:0A29FAB9                 db    ? ;
.bss:0A29FABA                 db    ? ;
.bss:0A29FABB                 db    ? ;
.bss:0A29FABC                 db    ? ;
.bss:0A29FABD                 db    ? ;
.bss:0A29FABE                 db    ? ;
.bss:0A29FABF                 db    ? ;
```

complex_function

```assembly
int __cdecl complex_function(signed int a1, int a2)
{
  if ( a1 <= 64 || a1 > 90 )
  {
    puts("Try again.");
    exit(1);
  }
  return (9 * a2 + a1 - 65) % 26 + 65;
}
```

### state.memory

前面提到可以通过 `state.mem[index]` 访问内存，但对于一段连续内存的操作十分不方便。因此我们也可以使用 `state.memory` 的 `.load(addr, size) / .store(addr, val)` 接口读写内存, size 以 bytes 为单位

这些函数的原型：

```assembly
def load(self, addr, size=None, condition=None, fallback=None, add_constraints=None, action=None, endness=None,
             inspect=True, disable_actions=False, ret_on_segv=False):
'''
Loads size bytes from dst.
addr:             The address to load from. #读取的地址
size:            The size (in bytes) of the load. #大小
condition:       A claripy expression representing a condition for a conditional load.
fallback:        A fallback value if the condition ends up being False. 
add_constraints: Add constraints resulting from the merge (default: True).
action:          A SimActionData to fill out with the constraints.
endness:         The endness to load with. #端序
'''
        
def store(self, addr, data, size=None, condition=None, add_constraints=None, endness=None, action=None,
              inspect=True, priv=None, disable_actions=False):
'''
Stores content into memory.
addr:        A claripy expression representing the address to store at. #内存地址
data:        The data to store (claripy expression or something convertable to a claripy expression).#写入的数据
size:        A claripy expression representing the size of the data to store. #大小
'''
```

exp:

```assembly
import angr
import claripy
from Crypto.Util.number import long_to_bytes
import sys

def main(argv):
  project = angr.Project("./05_angr_symbolic_memory")

  start_address = 0x8048606
  initial_state = project.factory.blank_state(addr=start_address)

  # The binary is calling scanf("%8s %8s %8s %8s").
  password0 = claripy.BVS('password0', 8*8)
  password1 = claripy.BVS('password1', 8*8)
  password2 = claripy.BVS('password2', 8*8)
  password3 = claripy.BVS('password3', 8*8)

  # Determine the address of the global variable to which scanf writes the user
  # input. The function 'initial_state.memory.store(address, value)' will write
  # 'value' (a bitvector) to 'address' (a memory location, as an integer.) The
  # 'address' parameter can also be a bitvector (and can be symbolic!).
  password0_address = 0xa29faa0
  initial_state.memory.store(password0_address, password0)
  password1_address = 0xa29faa8
  initial_state.memory.store(password1_address, password1)
  password2_address = 0xa29fab0
  initial_state.memory.store(password2_address, password2)
  password3_address = 0xa29fab8
  initial_state.memory.store(password3_address, password3)

  # 将模拟管理器重置为设置好的状态
  simulation = project.factory.simgr(initial_state)

  def is_successful(state):
    stdout_output = state.posix.dumps(sys.stdout.fileno())
    return b'Good Job.' in stdout_output

  def should_abort(state):
    stdout_output = state.posix.dumps(sys.stdout.fileno())
    return b'Try again.' in stdout_output

  simulation.explore(find=is_successful, avoid=should_abort)

  if simulation.found:
    solution_state = simulation.found[0]

    # Solve for the symbolic values. We are trying to solve for a string.
    # Therefore, we will use eval, with named parameter cast_to=str
    # which returns a string instead of an integer.
    solution0 = long_to_bytes(solution_state.se.eval(password0))
    solution1 = long_to_bytes(solution_state.se.eval(password1))
    solution2 = long_to_bytes(solution_state.se.eval(password2))
    solution3 = long_to_bytes(solution_state.se.eval(password3))

    # solution = ' '.join([ solution0, solution1, solution2, solution3 ])

    print(solution0+solution1+solution2+solution3)

  else:
    raise Exception('Could not find the solution')

if __name__ == '__main__':
  main(sys.argv)

```

## 06_angr_symbolic_dynamic_memory

符号化动态内存

main

```assembly
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char *v3; // ebx
  char *v4; // ebx
  int v6; // [esp-10h] [ebp-1Ch]
  signed int i; // [esp+0h] [ebp-Ch]

  buffer0 = (char *)malloc(9u);
  buffer1 = (char *)malloc(9u);
  memset(buffer0, 0, 9u);
  memset(buffer1, 0, 9u);
  print_msg();
  printf("Enter the password: ");
  __isoc99_scanf("%8s %8s", buffer0, buffer1, v6);
  for ( i = 0; i <= 7; ++i )
  {
    v3 = &buffer0[i];
    *v3 = complex_function(buffer0[i], i);
    v4 = &buffer1[i];
    *v4 = complex_function(buffer1[i], i + 32);
  }
  if ( !strncmp(buffer0, "IQMEHECM", 8u) && !strncmp(buffer1, "PYBDSYBB", 8u) )
    puts("Good Job.");
  else
    puts("Try again.");
  free(buffer0);
  free(buffer1);
  return 0;
}
```

buffer

```assembly
.bss:0A79A118 buffer0         dd ?                    ; DATA XREF: main+1F↑w
.bss:0A79A118                                         ; main+36↑r ...
.bss:0A79A11C                 public buffer3
.bss:0A79A11C buffer3         db    ? ;
.bss:0A79A11D                 db    ? ;
.bss:0A79A11E                 db    ? ;
.bss:0A79A11F                 db    ? ;
.bss:0A79A120                 public buffer1
.bss:0A79A120 ; char *buffer1
.bss:0A79A120 buffer1         dd ?                    ; DATA XREF: main+31↑w
.bss:0A79A120                                         ; main+4B↑r ...
```

complex_function

```assembly
int __cdecl complex_function(signed int a1, int a2)
{
  if ( a1 <= 64 || a1 > 90 )
  {
    puts("Try again.");
    exit(1);
  }
  return (13 * a2 + a1 - 65) % 26 + 65;
}
```

回到最开始认识angr的时候，我们知道angr并没有真正“运行”二进制文件（至少到目前为止），它只是在模拟运行状态，因此它实际上不需要将内存分配到堆中，实际上可以伪造任何地址。我们所做的是在堆栈选择两个地址存放我们的缓冲区地址。之后告诉angr，将两个fake address分别保存到 `buffer0`,`buffer1` ，因为程序实际执行的时候就会把 **malloc**返回的地址保存到这里。最后我们把符号位向量保存到伪造的地址里。

参数 `endness` 用于设置端序，angr默认为大端序，总共可选的值如下：

```assembly
LE – 小端序(little endian, least significant byte is stored at lowest address)
BE – 大端序(big endian, most significant byte is stored at lowest address)
ME – 中间序(Middle-endian. Yep.)
```

这里我们直接设置为与项目的程序相同即可

```assembly
import angr
import claripy
from Crypto.Util.number import long_to_bytes
import sys

def main(argv):
  project = angr.Project("./06_angr_symbolic_dynamic_memory")

  '''
  .text:08048674                 push    offset aEnterThePasswo ; "Enter the password: "
  .text:08048679                 call    _printf
  .text:0804867E                 add     esp, 10h
  .text:08048681                 mov     edx, ds:buffer1
  .text:08048687                 mov     eax, ds:buffer0
  .text:0804868C                 sub     esp, 4
  .text:0804868F                 push    edx
  .text:08048690                 push    eax
  .text:08048691                 push    offset a8s8s    ; "%8s %8s"
  .text:08048696                 call    ___isoc99_scanf
  .text:0804869B                 add     esp, 10h
  .text:0804869E                 mov     [ebp+var_C], 0
  .text:080486A5                 jmp     short loc_804870B
  '''
  start_address = 0x804869e
  initial_state = project.factory.blank_state(addr=start_address)

  # The binary is calling scanf("%8s %8s").
  password0 = claripy.BVS('password0', 8*8)
  password1 = claripy.BVS('password0', 8*8)

  # Note: by default, Angr stores integers in memory with big-endianness. To
  # specify to use the endianness of your architecture, use the parameter
  # endness=project.arch.memory_endness. On x86, this is little-endian.
  fake_heap_address0 = 0x4444444
  pointer_to_malloc_memory_address0 = 0xa79a118
  initial_state.memory.store(pointer_to_malloc_memory_address0, fake_heap_address0, endness=project.arch.memory_endness)
  fake_heap_address1 = 0x4444454
  pointer_to_malloc_memory_address1 = 0xa79a120
  initial_state.memory.store(pointer_to_malloc_memory_address1, fake_heap_address1, endness=project.arch.memory_endness)

  # Store our symbolic values at our fake_heap_address. Look at the binary to
  # determine the offsets from the fake_heap_address where scanf writes.
  initial_state.memory.store(fake_heap_address0, password0)
  initial_state.memory.store(fake_heap_address1, password1)

  simulation = project.factory.simgr(initial_state)

  def is_successful(state):
    stdout_output = state.posix.dumps(sys.stdout.fileno())
    return b'Good Job.' in stdout_output

  def should_abort(state):
    stdout_output = state.posix.dumps(sys.stdout.fileno())
    return b'Try again.' in stdout_output

  simulation.explore(find=is_successful, avoid=should_abort)

  if simulation.found:
    solution_state = simulation.found[0]

    solution0 = solution_state.se.eval(password0,cast_to=str)
    solution1 = solution_state.se.eval(password1,cast_to=str)

    solution = ' '.join([ solution0, solution1 ])

    print(solution)
  else:
    raise Exception('Could not find the solution')

if __name__ == '__main__':
  main(sys.argv)

```

## 07_angr_symbolic_file

符号化一个文件里面的内容

main

```assembly
int __cdecl __noreturn main(int argc, const char **argv, const char **envp)
{
  signed int i; // [esp+Ch] [ebp-Ch]

  memset(buffer, 0, 0x40u);
  print_msg();
  printf("Enter the password: ");
  __isoc99_scanf("%64s", buffer);
  ignore_me((int)buffer, 0x40u);
  memset(buffer, 0, 0x40u);
  fp = fopen("WCEXPXBW.txt", "rb");
  fread(buffer, 1u, 0x40u, fp);
  fclose(fp);
  unlink("WCEXPXBW.txt");
  for ( i = 0; i <= 7; ++i )
    *(_BYTE *)(i + 134520992) = complex_function(*(char *)(i + 134520992), i);
  if ( strncmp(buffer, "GHTVZDUX", 9u) )
  {
    puts("Try again.");
    exit(1);
  }
  puts("Good Job.");
  exit(0);
}
```

使用fread函数从文件中加载内容，加密后再进行比较。

ignore_me

```assembly
unsigned int __cdecl ignore_me(int a1, size_t n)
{
  void *v2; // esp
  int v4; // [esp+0h] [ebp-28h]
  void *ptr; // [esp+Ch] [ebp-1Ch]
  size_t v6; // [esp+10h] [ebp-18h]
  void *s; // [esp+14h] [ebp-14h]
  FILE *stream; // [esp+18h] [ebp-10h]
  unsigned int v9; // [esp+1Ch] [ebp-Ch]

  ptr = (void *)a1;
  v9 = __readgsdword(0x14u);
  v6 = n - 1;
  v2 = alloca(16 * ((n + 15) / 0x10));
  s = &v4;
  memset(&v4, 0, n);
  unlink("WCEXPXBW.txt");
  stream = fopen("WCEXPXBW.txt", "a+b");
  fwrite(ptr, 1u, n, stream);
  fseek(stream, 0, 0);
  __isoc99_fscanf(stream, "%64s", s);
  fseek(stream, 0, 0);
  fwrite(s, 1u, n, stream);
  fclose(stream);
  return __readgsdword(0x14u) ^ v9;
}
```

把输入的密码存入`WCEXPXBW.txt`， 不用我们自己创建文件。

complex_function

```assembly
int __cdecl complex_function(signed int a1, int a2)
{
  if ( a1 <= 64 || a1 > 90 )
  {
    puts("Try again.");
    exit(1);
  }
  return (17 * a2 + a1 - 65) % 26 + 65;
}
```

使用Angr模拟一个文件系统，其中该文件被我们自己的模拟文件所替代，然后将该文件进行符号化处理。

#### 状态插件（state plugin)

除了刚刚讨论过的选项集，所有存储在SimState中的东西实际上都存储在附加在state上的“插件”中。到目前为止我们讨论的几乎所有state的属性都是一个插件——`memory`、`registers`、`mem`、`regs`、`solver`等等。这种设计带来了代码的模块化和能够便捷地为模拟状态的其他方面实现新的数据存储，或者提供插件的替代实现能力。

比如说，通常`memory`插件模拟一个平坦地址空间，但是在分析中可以选择开启“抽象内存”插件来支持`state.memory`，“抽象内存”使用新的数据类型表示地址，以模拟浮动的独立内存空间映射。反过来，插件可以减少代码的复杂性：`state.memory`和`state.registers`实际上是同一个插件的不同实例，因为寄存器也是用一块地址空间模拟的。

### 仿真文件系统-The Emulated Filesystem

在angr中与文件系统，套接字，管道或终端的任何交互的根源都是SimFile对象。SimFile是一种存储抽象，它定义符号或其他形式的字节序列。可以从某个位置读取文件，可以在某个位置写入文件，可以询问文件中当前存储了多少字节，还可以具体化文件，并为其生成测试用例。

```assembly
simgr_file = angr.storage.SimFile(filename, content=xxxxxx, size=file_size)
```

然后需要传给state的初始化过程来影响对文件系统的使用。我们可以利用`fs`选项以文件名的字典来预配置SimFile对象，也可以`fs.insert`是将文件插入到文件系统中，需要文件名与符号化的文件

```assembly
initial_state.fs.insert(filename, simgr_file)
```

由于版本问题，这个angr解题脚本似乎存在一些问题

```assembly
# We want to:
# 1. Determine the file from which fread reads.
# 2. Use Angr to simulate a filesystem where that file is replaced with our own
#    simulated file.
# 3. Initialize the file with a symbolic value, which will be read with fread
#    and propogated through the program.
# 4. Solve for the symbolic input to determine the password.

import angr
import claripy
import sys

def main(argv):
  project = angr.Project("./07_angr_symbolic_file")

  start_address = 0x80488db
  initial_state = project.factory.blank_state(addr=start_address)

  # Specify some information needed to construct a simulated file. For this
  # challenge, the filename is hardcoded, but in theory, it could be symbolic. 
  # Note: to read from the file, the binary calls
  # 'fread(buffer, sizeof(char), 64, file)'.
  filename = 'WCEXPXBW.txt'  # :string
  symbolic_file_size_bytes = 64

  # A file, in Linux, represents a stream of sequential data. This stream may
  # come from a physical file on your hard drive, the network, the output of
  # another program (ex: /dev/urandom), or anything else. In our case, we want
  # to construct a block of memory where we store our symbolic variables for the
  # program to read. The following constructs the symbolic memory that will
  # supply the stream of data to the Linux file. Also, to communicate with 
  # Angr's constraint solving system, we need to associate the memory with the 
  # initial_state.
  symbolic_file_backing_memory = angr.state_plugins.SimSymbolicMemory()
  symbolic_file_backing_memory.set_state(initial_state)

  # Construct a bitvector for the password and then store it in the file's
  # backing memory. The store method works exactly the same as the store method
  # you have already used. In fact, it's the exact same method! That means that
  # memory.store(address, bitvector) will write bitvector to the address we
  # specify. In this memory, unlike our program's memory, we want to write to
  # the beginning, as the Linux file will stream data from the beginning of the
  # file. For example, imagine a simple file, 'hello.txt':
  #
  # Hello world, my name is John.
  # ^                       ^
  # ^ address 0             ^ address 24 (count the number of characters)
  # In order to represent this in memory, we would want to write the string to
  # the beginning of the file:
  #
  # hello_txt_contents = claripy.BVV('Hello world, my name is John.', 30*8)
  # hello_txt_backing_memory.store(0, hello_txt_contents)
  #
  # Perhaps, then, we would want to replace John with a
  # symbolic variable. We would call:
  #
  # name_bitvector = claripy.BVS('symbolic_name', 4*8)
  # hello_txt_backing_memory.store(24, name_bitvector)
  #
  # Then, after the program calls fopen('hello.txt', 'r') and then
  # fread(buffer, sizeof(char), 30, hello_txt_file), the buffer would contain
  # the string from the file, except four symbolic bytes where the name would be
  # stored.
  password = claripy.BVS('password', symbolic_file_size_bytes * 8)
  symbolic_file_backing_memory.store(0, password)

  # Construct the symbolic file. The file_options parameter specifies the Linux
  # file permissions (read, read/write, execute etc.) The content parameter
  # specifies from where the stream of data should be supplied. If content is
  # an instance of SimSymbolicMemory (we constructed one above), the stream will
  # contain the contents (including any symbolic contents) of the memory,
  # beginning from address zero.
  # Set the content parameter to our SimSymbolicMemory instance that holds the
  # symbolic data.
  file_options = 'r'
  # password_file = angr.storage.SimFile(filename, file_options, content=symbolic_file_backing_memory, size=symbolic_file_size_bytes)
  password_file = angr.storage.SimFile(filename, content=symbolic_file_backing_memory, size=symbolic_file_size_bytes)

  # We have already created the file and the memory that stores the data that
  # the file will stream to the program, but we now need to tell Angr where the
  # file should appear to exist on the filesystem. This is a mapping between 
  # strings representing the filenames and the angr.storage.SimFiles themselves. For
  # example, if hello_txt_file was a SimFile,
  # symbolic_filesystem = {
  #   'hello.txt' : hello_txt_file
  # }
  # would specify that any fopen('hello.txt', 'r') calls should stream data from
  # hello_txt_file.
  symbolic_filesystem = {
    filename : password_file
  }
  initial_state.posix.fs = symbolic_filesystem

  simulation = project.factory.simgr(initial_state)

  def is_successful(state):
    stdout_output = state.posix.dumps(sys.stdout.fileno())
    return b'Good Job.' in stdout_output

  def should_abort(state):
    stdout_output = state.posix.dumps(sys.stdout.fileno())
    return b'Try again.' in stdout_output

  simulation.explore(find=is_successful, avoid=should_abort)

  if simulation.found:
    solution_state = simulation.found[0]

    solution = solution_state.se.eval(password,cast_to=str)

    print(solution)
  else:
    raise Exception('Could not find the solution')

if __name__ == '__main__':
  main(sys.argv)

```

