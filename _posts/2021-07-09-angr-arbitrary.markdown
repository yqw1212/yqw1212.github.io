---
layout: post
title:  Angr(5)
date:   2021-07-09 00:01:01 +0300
image:  2021-07-09-yoga.jpg
tags:   [ctf,reverse,angr]
---

## 15_angr_arbitrary_read

利用Angr实现内存地址的任意读

main

```assembly
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char v4; // [esp+Ch] [ebp-1Ch]
  char *s; // [esp+1Ch] [ebp-Ch]

  s = try_again;
  print_msg();
  printf("Enter the password: ");
  __isoc99_scanf("%u %20s", &key, &v4);
  if ( key == 19511649 )
    puts(s);
  else
    puts(try_again);
  return 0;
}
```

.bss

```assembly
.bss:594E6040 key             dd ?                    ; DATA XREF: main+35↑o
.bss:594E6040                                         ; main+47↑r
.bss:594E6040 _bss            ends
```

这题的关键是修改s处内存的指针地址使其指向"Good Job."的地址。

.rodata

```assembly
.rodata:594E424C aTryAgain       db 'Try again.',0       ; DATA XREF: .data:try_again↓o
.rodata:594E4257 aGoodJob        db 'Good Job.',0        ; DATA XREF: .data:good_job↓o
```

.data

```assembly
.data:594E6034 try_again       dd offset aTryAgain     ; DATA XREF: main+11↑r
.data:594E6034                                         ; main+5A↑r ...
.data:594E6034                                         ; "Try again."
.data:594E6038                 public good_job
.data:594E6038 good_job        dd offset aGoodJob      ; "Good Job."
```

观察一下v4的栈结构

```assembly
-0000001C var_1C          db ?
-0000001B                 db ? ; undefined
-0000001A                 db ? ; undefined
-00000019                 db ? ; undefined
-00000018                 db ? ; undefined
-00000017                 db ? ; undefined
-00000016                 db ? ; undefined
-00000015                 db ? ; undefined
-00000014                 db ? ; undefined
-00000013                 db ? ; undefined
-00000012                 db ? ; undefined
-00000011                 db ? ; undefined
-00000010                 db ? ; undefined
-0000000F                 db ? ; undefined
-0000000E                 db ? ; undefined
-0000000D                 db ? ; undefined
-0000000C s               dd ?                    ; offset
-00000008                 db ? ; undefined
-00000007                 db ? ; undefined
-00000006                 db ? ; undefined
-00000005                 db ? ; undefined
```

v4和s在内存上是相邻的，在scanf中，v4允许我们输入20个字符，存在越界写的问题，输入的字符串刚刚好可以覆盖到 `s`，从而修改s字符。

```assembly
import angr
import claripy
from Crypto.Util.number import long_to_bytes
import sys

def main(argv):
  project = angr.Project("./15_angr_arbitrary_read")

  # You can either use a blank state or an entry state; just make sure to start
  # at the beginning of the program.
  initial_state = project.factory.entry_state()

  # Again, scanf needs to be replaced.
  class ReplacementScanf(angr.SimProcedure):
    # scanf("%u %20s")
    def run(self, format_string, param0, param1):
      # %u 无符号整数
      scanf0 = claripy.BVS('scanf0', 32)
      
      # %20s
      scanf1 = claripy.BVS('scanf1', 20*8)

      # The bitvector.chop(bits=n) function splits the bitvector into a Python
      # list containing the bitvector in segments of n bits each. In this case,
      # we are splitting them into segments of 8 bits (one byte.)
      for char in scanf1.chop(bits=8):
        # Ensure that each character in the string is printable. An interesting
        # experiment, once you have a working solution, would be to run the code
        # without constraining the characters to the printable range of ASCII.
        # Even though the solution will technically work without this, it's more
        # difficult to enter in a solution that contains character you can't
        # copy, paste, or type into your terminal or the web form that checks 
        # your solution.
        self.state.add_constraints(char >= 'A', char <= 'Z')

      # Warning: Endianness only applies to integers. If you store a string in
      # memory and treat it as a little-endian integer, it will be backwards.
      self.state.memory.store(param0, scanf0, endness=project.arch.memory_endness) # 小端序
      self.state.memory.store(param1, scanf1)

      self.state.globals['solutions'] = (scanf0, scanf1)

  scanf_symbol = '__isoc99_scanf'  # :string
  project.hook_symbol(scanf_symbol, ReplacementScanf())

  # We will call this whenever puts is called. The goal of this function is to
  # determine if the pointer passed to puts is controllable by the user, such
  # that we can rewrite it to point to the string "Good Job."
  def check_puts(state):
    # The stack, registers, memory, etc should be set up as if the x86 call
    # instruction was just invoked (but, of course, the function hasn't copied
    # the buffers yet.)
    # The stack will look as follows:
    # ...
    # esp + 7 -> /----------------\
    # esp + 6 -> |      puts      |
    # esp + 5 -> |    parameter   |
    # esp + 4 -> \----------------/
    # esp + 3 -> /----------------\
    # esp + 2 -> |     return     |
    # esp + 1 -> |     address    |
    #     esp -> \----------------/
    # puts函数只有一个参数，那这个参数一定是存在栈上esp指针+4的位置
    puts_parameter = state.memory.load(state.regs.esp + 4, 4, endness=project.arch.memory_endness)

    # The following function takes a bitvector as a parameter and checks if it
    # can take on more than one value. While this does not necessary tell us we
    # have found an exploitable path, it is a strong indication that the 
    # bitvector we checked may be controllable by the user.
    # Use it to determine if the pointer passed to puts is symbolic.
    if state.se.symbolic(puts_parameter):
      # If we add this as a constraint to our solver,
      # it will try and find an input to make this expression true.
      # .rodata:594E4257 aGoodJob        db 'Good Job.',0        ; DATA XREF: .data:good_job↓o
      is_vulnerable_expression = puts_parameter == 0x594e4257 # :boolean bitvector expression

      # 对当前状态做一个拷贝，方便操作状态而不对原来的状态产生影响干扰，然后给状态添加约束条件
      copied_state = state.copy()

      copied_state.add_constraints(is_vulnerable_expression)
       
      if copied_state.satisfiable():
        # Before we return, let's add the constraint to the solver for real,
        # instead of just querying whether the constraint _could_ be added.
        state.add_constraints(is_vulnerable_expression)
        return True
      else:
        return False
    else: # not path.state.se.symbolic(???)
      return False

  simulation = project.factory.simgr(initial_state)

  def is_successful(state):
    # We are looking for puts. Check that the address is at the (very) beginning
    # of the puts function. Warning: while, in theory, you could look for
    # any address in puts, if you execute any instruction that adjusts the stack
    # pointer, the stack diagram above will be incorrect.
    # 检查puts函数调用时传入的参数s的值
    # .plt:08048370 _puts           proc near               ; CODE XREF: main+63↓p
    puts_address = 0x8048370
    if state.addr == puts_address:
      # Return True if we determine this call to puts is exploitable.
      return check_puts(state)
    else:
      # We have not yet found a call to puts; we should continue!
      return False

  simulation.explore(find=is_successful)

  if simulation.found:
    solution_state = simulation.found[0]

    (scanf0, scanf1) = solution_state.globals['solutions']
    solution = str(solution_state.se.eval(scanf0)) + ' ' + str(long_to_bytes(solution_state.se.eval(scanf1)))[2:-1]
    print(solution)
  else:
    raise Exception('Could not find the solution')

if __name__ == '__main__':
  main(sys.argv)

```

## 16_angr_arbitrary_write

main

```assembly
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char s; // [esp+Ch] [ebp-1Ch]
  char *dest; // [esp+1Ch] [ebp-Ch]

  dest = unimportant_buffer;
  memset(&s, 0, 0x10u);
  strncpy(password_buffer, "PASSWORD", 0xCu);
  print_msg();
  printf("Enter the password: ");
  __isoc99_scanf("%u %20s", &key, &s);
  if ( key == 24173502 )
    strncpy(dest, &s, 0x10u);
  else
    strncpy(unimportant_buffer, &s, 0x10u);
  if ( !strncmp(password_buffer, "DVTBOGZL", 8u) )
    puts("Good Job.");
  else
    puts("Try again.");
  return 0;
}
```

password_buffer的内容必须和"DVTBOGZL"相同。

.bss

```assembly
.bss:4655543C unimportant_buffer db 10h dup(?)        ; DATA XREF: main+11↑o
.bss:4655543C                                         ; main+8C↑o ...
.bss:4655544C                 public password_buffer
.bss:4655544C ; char password_buffer[16]
.bss:4655544C password_buffer db 10h dup(?)           ; DATA XREF: main+35↑o
.bss:4655544C                                         ; main+D3↑o
.bss:4655545C                 public key
.bss:4655545C key             dd ?                    ; DATA XREF: main+5E↑o
.bss:4655545C                                         ; main+70↑r
.bss:4655545C _bss            ends
```

strncpy

```assembly
strncpy(dest, &s, 0x10u);
```

可以将`dest`指向`password_buffer`，然后将`src`的内容修改为`"DVTBOGZL"`

```assembly
-0000001C s               db ?
-0000001B                 db ? ; undefined
-0000001A                 db ? ; undefined
-00000019                 db ? ; undefined
-00000018                 db ? ; undefined
-00000017                 db ? ; undefined
-00000016                 db ? ; undefined
-00000015                 db ? ; undefined
-00000014                 db ? ; undefined
-00000013                 db ? ; undefined
-00000012                 db ? ; undefined
-00000011                 db ? ; undefined
-00000010                 db ? ; undefined
-0000000F                 db ? ; undefined
-0000000E                 db ? ; undefined
-0000000D                 db ? ; undefined
-0000000C dest            dd ?                    ; offset
-00000008                 db ? ; undefined
-00000007                 db ? ; undefined
-00000006                 db ? ; undefined
-00000005                 db ? ; undefined
```

exp

```assembly
import angr
import claripy
from Crypto.Util.number import long_to_bytes
import sys

def main(argv):
  project = angr.Project("./16_angr_arbitrary_write")

  # You can either use a blank state or an entry state; just make sure to start
  # at the beginning of the program.
  initial_state = project.factory.entry_state()

  class ReplacementScanf(angr.SimProcedure):
    # Hint: scanf("%u %20s")
    def run(self, format_string, param0, param1):
      # %u
      scanf0 = claripy.BVS('scanf0', 32)

      # %20s
      scanf1 = claripy.BVS('scanf1', 20*8)

      for char in scanf1.chop(bits=8):
        self.state.add_constraints(char >= 48, char <= 96)

      self.state.memory.store(param0, scanf0, endness=project.arch.memory_endness)
      self.state.memory.store(param1, scanf1)

      self.state.globals['solutions'] = (scanf0, scanf1)

  scanf_symbol = '__isoc99_scanf'  # :string
  project.hook_symbol(scanf_symbol, ReplacementScanf())

  # In this challenge, we want to check strncpy to determine if we can control
  # both the source and the destination. It is common that we will be able to
  # control at least one of the parameters, (such as when the program copies a
  # string that it received via stdin).
  def check_strncpy(state):
    # The stack will look as follows:
    # ...          ________________
    # esp + 15 -> /                \
    # esp + 14 -> |     param2     |
    # esp + 13 -> |      len       |
    # esp + 12 -> \________________/
    # esp + 11 -> /                \
    # esp + 10 -> |     param1     |
    #  esp + 9 -> |      src       |
    #  esp + 8 -> \________________/
    #  esp + 7 -> /                \
    #  esp + 6 -> |     param0     |
    #  esp + 5 -> |      dest      |
    #  esp + 4 -> \________________/
    #  esp + 3 -> /                \
    #  esp + 2 -> |     return     |
    #  esp + 1 -> |     address    |
    #      esp -> \________________/
    # 把参数内容提取出来
    strncpy_src = state.memory.load(state.regs.esp + 8, 4, endness=project.arch.memory_endness)
    strncpy_dest = state.memory.load(state.regs.esp + 4, 4, endness=project.arch.memory_endness)
    strncpy_len = state.memory.load(state.regs.esp + 12, 4, endness=project.arch.memory_endness)

    # We need to find out if src is symbolic, however, we care about the
    # contents, rather than the pointer itself. Therefore, we have to load the
    # the contents of src to determine if they are symbolic.
    # Hint: How many bytes is strncpy copying?
    src_contents = state.memory.load(strncpy_src, strncpy_len)

    # Determine if the destination pointer and the source is symbolic.
    if state.se.symbolic(src_contents) and state.se.symbolic(strncpy_dest):
      # Create an expression that tests if the first n bytes is length. Warning:
      # while typical Python slices (array[start:end]) will work with bitvectors,
      # they are indexed in an odd way. The ranges must start with a high value
      # and end with a low value. Additionally, the bits are indexed from right
      # to left. For example, let a bitvector, b, equal 'ABCDEFGH', (64 bits).
      # The following will read bit 0-7 (total of 1 byte) from the right-most
      # bit (the end of the string).
      #  b[7:0] == 'H'
      # To access the beginning of the string, we need to access the last 16
      # bits, or bits 48-63:
      #  b[63:48] == 'AB'
      does_src_hold_password = src_contents[-1:-64] == 'DVTBOGZL'

      # Create an expression to check if the dest parameter can be set to
      # buffer_address. If this is true, then we have found our exploit!
      does_dest_equal_buffer_address = strncpy_dest == 0x4655544c

      # We can pass multiple expressions to extra_constraints!
      if state.satisfiable(extra_constraints=(does_src_hold_password, does_dest_equal_buffer_address)):
        state.add_constraints(does_src_hold_password, does_dest_equal_buffer_address)
        return True
      else:
        return False
    else: # not path.state.se.symbolic(???)
      return False

  simulation = project.factory.simgr(initial_state)

  def is_successful(state):
    strncpy_address = 0x8048410
    if state.addr == strncpy_address:
      return check_strncpy(state)
    else:
      return False

  simulation.explore(find=is_successful)
  if simulation.found:
    solution_state = simulation.found[0]

    scanf0, scanf1 = solution_state.globals['solutions']
    solution = str(solution_state.se.eval(scanf0)) + ' ' + str(long_to_bytes(solution_state.se.eval(scanf1)))
    print(solution)
  else:
    raise Exception('Could not find the solution')

if __name__ == '__main__':
  main(sys.argv)

```

## 17_angr_arbitrary_jump

任意地址跳转，即利用Angr处理无约束状态

main

```assembly
int __cdecl main(int argc, const char **argv, const char **envp)
{
  print_msg();
  printf("Enter the password: ");
  read_input();
  puts("Try again.");
  return 0;
}
```

read_input

```assembly
int read_input()
{
  char v1; // [esp+1Ah] [ebp-1Eh]

  return __isoc99_scanf("%s", &v1);
}
```

还可以发现存在一个没有被调用到的函数`print_good`

```assembly
void __noreturn print_good()
{
  puts("Good Job.");
  exit(0);
}
```

read_input()函数里的scanf存在栈溢出漏洞，这题就是非常简单的ROP使得我们跳转到print_good函数

当一条指令有太多可能的分支时，就会出现无约束状态。当指令指针完全是符号指针时，就会发生这种情况，这意味着用户输入可以控制计算机执行的代码的地址。

改变Angr的模拟引擎的默认设置，参数`save_unconstrained=True`时指定Angr不抛出不受约束的状态。相反，它会将它们移动到名为`simul.com unconstrained`的stashes 中。此外，我们将使用一些默认情况下不包含的stashes ，如’found’和’not_needed’。

- active：程序仍能进一步执行
- deadended：程序结束
- errored：Angr执行中出现错误的状态
- unconstrained：不受约束的状态
- found：找到路径答案的状态
- not_needed：所有其它情况

```assembly
import angr
import claripy
import sys

def main(argv):
  project = angr.Project("./17_angr_arbitrary_jump")

  initial_state = project.factory.entry_state() 

  # For example, imagine the following pseudo assembly:
  # mov user_input, eax
  # jmp eax

  # The save_unconstrained=True parameter specifies to Angr to not throw out
  # unconstrained states. Instead, it will move them to the list called
  # 'simulation.unconstrained'.
  # Additionally, we will be using a few stashes that are not included by
  # default, such as 'found' and 'not_needed'. You will see how these are used
  # later.
  simulation = project.factory.simgr(
    initial_state, 
    save_unconstrained=True,
    stashes={
      'active' : [initial_state],
      'unconstrained' : [],
      'found' : [],
      'not_needed' : []
    }
  )

  # 定义四个函数来获得我们想要获得的程序状态

  # 检查无约束状态是否可利用
  # The value of what the user entered dictates the next instruction. This
  # is an unconstrained state. It wouldn't usually make sense for the execution
  # engine to continue. (Where should the program jump to if eax could be
  # anything?) Normally, when Angr encounters an unconstrained state, it throws
  # it out. In our case, we want to exploit the unconstrained state to jump to
  # a location of our choosing. We will get to how to disable Angr's default
  # behavior later. For now, test if a state is vulnerable by checking if we
  # can set the instruction pointer to the address of print_good in the binary.
  def check_vulnerable(state):
    return state.se.symbolic(state.regs.eip)

  # Explore will not work for us, since the method specified with the 'find'
  # parameter will not be called on an unconstrained state. Instead, we want to
  # explore the binary ourselves.
  # To get started, construct an exit condition to know when we've found a
  # solution. We will later be able to move states from the unconstrained list
  # to the simulation.found list. Alternatively, you can create a boolean value
  # that serves the same purpose.
  def has_found_solution():
    return simulation.found

  # 检查是否还有未受约束的状态需要检查
  # Check if there are still unconstrained states left to check. Once we
  # determine a given unconstrained state is not exploitable, we can throw it
  # out. Use the simulation.unconstrained list.
  def has_unconstrained_to_check():
    return simulation.unconstrained

  # active是可以进一步探索的所有状态的列表
  # The list simulation.active is a list of all states that can be explored
  # further.
  def has_active():
    return simulation.active

  # 之前一直使用的simulation.explore方法并不适合现在这种情况，
  # 因为find参数指定的方法不会在无约束状态下被调用，
  # 想要自己探索未约束情况下的二进制代码，我们需要自己编写解决方案
  while (has_active() or has_unconstrained_to_check()) and (not has_found_solution()): # 如果出现了约束状态下的解则求解失败
    # Iterate through all unconstrained states and check them.
    for unconstrained_state in simulation.unconstrained:
      # Check if the unconstrained state is exploitable.
      #if check_vulnerable(unconstrained_state):
        # Found an exploit, exit the while loop and keep unconstrained_state as
        # the solution. The way the loops is currently set up, you should move
        # the exploitable unconstrained state to the 'found' stash.
        # A 'stash' should be a string that corresponds to a list that stores
        # all the states that the state group keeps. Values include:
        #  'active' = states that can be stepped
        #  'deadended' = states that have exited the program
        #  'errored' = states that encountered an error with Angr
        #  'unconstrained' = states that are unconstrained
        #  'found' = solutions
        #  anything else = whatever you want, perhaps you want a 'not_needed',
        #                  you can call it whatever you want

        # The following will move everything that passes the should_move check
        # from the from_stash to the to_stash.
        # def should_move(state):
        #   # Reimplement me if you decide to use me
        #   return False
        # simulation.move(from_stash, to_stash, filter_func=should_move)

        # # For example, the following moves everything in 'active' to
        # # 'not_needed' except if the state is in keep_states
        # keep_states = [ ... ]
        # def should_move(state):
        #   return not state in keep_states
        # simulation.move('active', 'not_needed', filter_func=should_move)
      def should_move(s):
        return s is unconstrained_state
      simulation.move('unconstrained', 'found', filter_func=should_move)

      #else: # unconstrained state is not exploitable
        # Move the unconstrained_state that you tested that doesn't work to a
        # different stash, perhaps 'not_needed'.
      #  def should_move(s):
      #    return s is state
      #  simulation.move('active', 'not_needed', filter_func=should_move)
        
 
    # Advance the simulation.
    simulation.step()

  if simulation.found:
    solution_state = simulation.found[0]

    # Constrain the instruction pointer to target the print_good function and
    # then solve for the user input (recall that this is
    # 'solution_state.posix.dumps(sys.stdin.fileno())')
    # .text:4D4C4749 print_good      proc near
    solution_state.add_constraints(solution_state.regs.eip == 0x4d4c4749)

    # Ensure that every printed byte is within the acceptable ASCII range (A..Z)
    # for byte in solution_state.posix.files[sys.stdin.fileno()].all_bytes().chop(bits=8):
    for byte in solution_state.posix.stdin.content[0][0].chop(bits=8):
      solution_state.add_constraints(
        claripy.Or(
          byte == 0x0,
          claripy.And(
            byte >= 'A', 
            byte <= 'Z'
          )
        )
      )

    solution = solution_state.posix.dumps(sys.stdin.fileno())
    print(solution)
  else:
    raise Exception('Could not find the solution')

if __name__ == '__main__':
  main(sys.argv)

```

