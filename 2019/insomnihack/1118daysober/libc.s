__syscall:
	stmfd	sp!, {r4, r5, r7, lr}
	ldr	r4, [sp, #16]
	ldr	r5, [sp, #20]
	mov	r7, r12
	swi	#0

	cmn	r0, #4096
	rsbcs	r2, r0, #0
	ldrcs	r3, =errno
	mvncs	r0, #0
	strcs	r2, [r3]
	ldmfd	sp!, {r4, r5, r7, pc}

.global errno
errno:
	.word	0

.global _exit
_exit:
	mov	r12, #1
	b	__syscall

.global read
read:
	mov	r12, #3
	b	__syscall

.global write
write:
	mov	r12, #4
	b	__syscall

.global open
open:
	mov	r12, #5
	b	__syscall

.global close
close:
	mov	r12, #6
	b	__syscall

.global pipe
pipe:
	mov	r12, #42
	b	__syscall

.global mmap
mmap:
	mov	r12, #192
	b	__syscall

.global munmap
munmap:
	mov	r12, #91
	b	__syscall
