arm-linux-gnueabi-gcc -o a a.c libc.s -nostartfiles -nostdlib -static -Os -w
cat a | base64
