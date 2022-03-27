from pwn import *

TRIALS = 200
data = set()
for i in range(TRIALS):
    r = remote('crypto.ctf.zer0pts.com', 10333)
    p = int(r.recvline().split()[2])
    n =  int(r.recvline().split()[2])
    e = int(r.recvline().split()[2])
    x1 = int(r.recvline().split()[2])
    x2 = int(r.recvline().split()[2])

    r.recvuntil(":")
    if (x1 + x2) % 2 == 0:
        s = (((x1 + x2) // 2)%n)
    else:
        s = (((x1 + x2 + n) // 2) % n)
    r.sendline(str(s))

    c1 = int(r.recvline().split()[2])
    c2 = int(r.recvline().split()[2])

    data.add(((c1+c2) % n, n))

    r.close()

print(data)