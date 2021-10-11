from Crypto.Util.number import *
from pwn import *

def xor_block(b1, b2):
    return long_to_bytes(bytes_to_long(b1) ^ bytes_to_long(b2), 16)

r = remote('good-hash.chal.perfect.blue', 1337)

r.recvuntil('Body: ')
token_body = r.recvline().strip()
print(token_body)

evil = xor_block(token_body[:16], long_to_bytes(47479916811, 16)) \
        + xor_block(token_body[16:32], long_to_bytes(18676733080516473137467035176970027780, 16)) \
        + xor_block(token_body[32:48], long_to_bytes(1329290032072102227859345453623541760, 16)) \
        + b'dmin":true  }'

print(evil)

r.recvuntil('> ')
r.sendline(evil.decode('utf-8'))
r.interactive()