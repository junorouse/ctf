arm-linux-gnueabi-gcc -o b b.c libc.s -nostartfiles -nostdlib -static -Os -w
cat b | base64
