# collision
## 1.分析逻辑
```c
if(strlen(argv[1]) != 20){
	printf("passcode length should be 20 bytes\n");
	return 0;
}

if(hashcode == check_password( argv[1] )){
	system("/bin/cat flag");
	return 0;
}
else
	printf("wrong passcode.\n");
```
我们注意到本题要求一个20字节的参数，将参数检查后与hashcode比较，若相等输出flag。
```c
unsigned long check_password(const char* p){
	int* ip = (int*)p;
	int i;
	int res=0;
	for(i=0; i<5; i++){
		res += ip[i];
	}
	return res;
}
```
检查函数将参数分割为五个整数，返回相加的和。而hashcode为`unsigned long hashcode = 0x21DD09EC;`
因此我们只需找到五个和为0x21DD09EC的数，将他们连接为20字节的比特串。
为了避免被截断，不能出现\x00,因此使用四个0x01010101和0x21DD09EC-0x01010101*4=0x1dd905e8
## 2.利用
```
col@pwnable:~$ ./col `python -c "print '\x01'*16+'\xe8\x05\xd9\x1d'"`
daddy! I just managed to create a hash collision :)
```
