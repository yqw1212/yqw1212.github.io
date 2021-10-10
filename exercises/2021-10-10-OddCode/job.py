from ctypes import addressof
from unicorn import *
from unicorn.x86_const import *
from capstone import *
 
ADDRESS = 0x2E1000          # 程序加载的地址
INPUT_ADDRESS = 0x2E701D    # 输入的地址
KEY_ADDRESS = 0x2E705C      # 16字节key的地址
with open('OddCode.exe', 'rb') as file:
    file.seek(0x400)
    X64_CODE = file.read(0x4269)    # 读取代码
 
class Unidbg:
 
    def __init__(self, flag, except_hit):
        self.except_hit = except_hit
        self.hit = 0
        self.success = False
        mu = Uc(UC_ARCH_X86, UC_MODE_64)
        # 基址为0x2E1000，分配16MB内存
        mu.mem_map(ADDRESS, 0x1000000)
        mu.mem_write(ADDRESS, X64_CODE)
        mu.mem_write(INPUT_ADDRESS, flag)       # 随便写入一个flag
        mu.mem_write(KEY_ADDRESS, b'\x90\xF0\x70\x7C\x52\x05\x91\x90\xAA\xDA\x8F\xFA\x7B\xBC\x79\x4D')
        # 初始化寄存器，寄存器的状态就是切换到64位模式之前的状态，可以通过动调得到
        mu.reg_write(UC_X86_REG_RAX, 1)
        mu.reg_write(UC_X86_REG_RBX, 0x51902D)
        mu.reg_write(UC_X86_REG_RCX, 0xD86649D8)
        mu.reg_write(UC_X86_REG_RDX, 0x2E701C)
        mu.reg_write(UC_X86_REG_RSI, INPUT_ADDRESS)  # input参数
        mu.reg_write(UC_X86_REG_RDI, KEY_ADDRESS)    # key参数
        mu.reg_write(UC_X86_REG_RBP, 0x6FFBBC)
        mu.reg_write(UC_X86_REG_RSP, 0x6FFBAC)
        mu.reg_write(UC_X86_REG_RIP, 0x2E1010)
        mu.hook_add(UC_HOOK_CODE, self.trace)        # hook代码执行，保存代码块执行轨迹
        #mu.hook_add(UC_HOOK_MEM_READ, self.hook_mem_read)
        self.mu = mu
        self.except_addr = 0
        self.traces = []        # 用来保存代码块执行轨迹
        self.md = Cs(CS_ARCH_X86, CS_MODE_64)
 
    def trace(self, mu, address, size, data):
        '''
        disasm = self.md.disasm(mu.mem_read(address, size), address)
        for i in disasm:
            mnemonic = i.mnemonic
            if mnemonic == 'cmp' or mnemonic == 'test':
                print(f'Instruction {mnemonic} at {hex(address)}')
        '''
        if address != self.except_addr:
            self.traces.append(address)
        self.except_addr = address + size
        if address == 0x2E38EF:
            self.hit += 1
            #print(f'hit {self.hit}')
            if self.hit == self.except_hit:
                self.success = True
                mu.emu_stop()
 
 
    def hook_mem_read(self, mu, access, address, size, value, data):
        if address >= INPUT_ADDRESS and address <= INPUT_ADDRESS + 41:
            print(f'Read input[{address - INPUT_ADDRESS}] at {hex(mu.reg_read(UC_X86_REG_RIP))}')
        if address >= KEY_ADDRESS and address <= KEY_ADDRESS + 16:
            print(f'Read key[{address - KEY_ADDRESS}] at {hex(mu.reg_read(UC_X86_REG_RIP))}')
 
 
    def solve(self):
        try:
            self.mu.emu_start(0x2E1010, -1)
        except:
            pass
        return self.success
 
def get_flag(flag, except_hit):
    for i in b'1234567890abcdefABCDEF':
        for j in b'1234567890abcdefABCDEF':
            flag[8 + (except_hit - 1) * 2] = i
            flag[8 + (except_hit - 1) * 2 + 1] = j
            if Unidbg(bytes(flag), except_hit).solve():
                return
 
flag = bytearray(b'SangFor{00000000000000000000000000000000}')
for i in range(1, 17):
    get_flag(flag, i)
    print(flag.decode())