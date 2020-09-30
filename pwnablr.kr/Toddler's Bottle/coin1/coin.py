from pwn import *
import math
#from zio import *
io = remote('pwnable.kr', 9007)
def binarySearch(left, right):
	mid = int(math.floor((left+right) / 2))
	payload = ' '.join([ str(i) for i in range(left, mid+1 ) ] )
	io.sendline(payload)
	result = io.recvline().decode()
	if 'Correct!' not in result:
		result = int(result)
	else:
		print('Correct!')
		return
    # print (middle-left + 1)
	if result == 10*(mid + 1 -left):
		binarySearch(mid+1, right)
	else:
		binarySearch(left, mid)

def pwn():
	io.recvuntil('in 3 sec... -\n')
	io.recvline()
	for i in range(0,100):
		num = io.recvline().decode()
		print(num)
		li = num.split(' ')
		n = li[0].split('=')[1]
		c = li[1].split('=')[1]
		binarySearch(0,int(n) - 1)
	print(io.recvall())
pwn()
