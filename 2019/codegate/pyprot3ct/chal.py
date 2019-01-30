import play

f = open("code", "rb")
code = f.read()
code = bytearray(code)
f.close()

flag = input().strip()
flag = bytearray(flag, "utf-8")

if play.first_call(code, flag):
    print(":)")
else:
    print(":(")