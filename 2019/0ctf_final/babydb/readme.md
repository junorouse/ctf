# babydb

## vuln (three-lines)

```ocaml
  | true, name when name = (SessionState.access user) ->
    let res = SessionState.put name in
    SessionState.bind res (fun _ -> SessionState.return (cont^"login|"))
```

If the code goes to the upper code path, we can set an arbitrary name.  
I don't know why but we put "login?user?pass?c:login???:store?a?b?c" on the `batch` command,  
`user` => `''`, `args` => `a`. (hooray we can get aribtrary file r/w).

## exploit

We can read arbitrary file but only fisrt line. I faced on `your flag here:` message when I read `../../../../../../flag`. I had to get a Code Execution to read the whole flag.
I am not at on-site. I asked to my teammate "I asked teammate, Is port 22 open?", he said yes, I changed the contents of `/home/user/.ssh/authorized_keys` to mine.

```shell
$ cat flag
your flag here:
flag{I_want_to_give_web_challenges_a_try_but_still_looks_like_misc_lol}
$
```
