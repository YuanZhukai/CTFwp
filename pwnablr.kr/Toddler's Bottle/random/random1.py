from pwn import *
from zio3 import *
host = ssh(host="pwnable.kr",user='random',password='guest',port=2222)
print(host.connected())
target = host.process(executable='./random')
payload=str(0xdeadbeef^0x6b8b4567)
target.sendline(payload)
print(target.recvall())
