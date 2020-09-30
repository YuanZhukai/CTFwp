# fd
## 1.漏洞
```c
if(argc<2){
	printf("pass argv[1] a number\n");
	return 0;
}
int fd = atoi( argv[1] ) - 0x1234;
int len = 0;
len = read(fd, buf, 32);
if(!strcmp("LETMEWIN\n", buf)){
	printf("good job :)\n");
	system("/bin/cat flag");
	exit(0);
}
```

本题可直接获取源文件，如上所示。

其将传入的第一个参数转化为数字减去0x1234,作为句柄打开并读取其中32个字节，与LETMEWIN作比较，若相等则给flag。

## 2.分析
当fd为0时，表示标准输入，因此我们只需要传参0x1234=4660,之后输入LETMEWIN。
