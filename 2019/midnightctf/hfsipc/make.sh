#!/bin/bash
gcc -o exploit exploit.c -static -w
tar -czf x.tar.gz exploit
base64 x.tar.gz
