- if there is no more space to alloc then crux returns 0.
- since the code section has RWX, base address=0, cs=0, we can simply overwrite the code, and execute arbitrary command.
- i could extract honcho(main hypervisor) binary via `out` ins. (crux binary bans `honcho` string)

- there is an out of bound access/write bug. no limitation of `vmmem` index.
- i don't make sense but in mac os, when you alloc large memory via `valloc`, the offset between its address and image base is always same.
- there is a little offset difference machine by machine, so i need to bruteforce it. 

- @c2w2m2 wrote final solver.
