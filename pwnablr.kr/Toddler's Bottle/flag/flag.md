# flag
## 1.分析逻辑
注意到本题为加壳的，首先用upx脱壳。
```c
puts("I will malloc() and strcpy the flag there. take it.", argv, envp);
dest = (char *)malloc(100LL);
strcpy(dest, flag);
```
可知文件中有一个叫flag的全局变量，使用IDA找到该变量即可。
`.rodata:0000000000496628 aUpxSoundsLikeA db 'UPX...? sounds like a delivery service :)',0`