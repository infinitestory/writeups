from Crypto.Util.number import *
from Crypto.Cipher import AES

# if you know how to do this better i'd love to hear it
def rev_block_int(block):
    return int('{:0128b}'.format(block)[::-1], 2)

def xor_block(b1, b2):
    return long_to_bytes(bytes_to_long(b1) ^^ bytes_to_long(b2), 16)

expected_subkey = AES.new(b'goodhashGOODHASH', AES.MODE_ECB).encrypt(b'\x00'*16)
assert expected_subkey == b'\x8c[\xb3\x0f\xba\xa0\xdf\xdb\xc7\xee\xb7\x1f_M\xd6\xab'
expected_subkey_int = bytes_to_long(expected_subkey)

F = GF(2^128, name='x', modulus=x^128 + x^7 + x^2 + x + 1)
# Sage fetch_int interprets the input as big endian, we want little endian to match AES-GCM spec
H = F.fetch_int(rev_block_int(expected_subkey_int))

orig = b'dmin": false}\x00\x00\x00'
TARGET_STR = 'dmin":true  }'
modified = TARGET_STR.encode() + b'\x00'*3
assert len(modified) == 16
# Endianness flip, same reason as above
target_diff = rev_block_int(bytes_to_long(xor_block(orig, modified)))

# construct matrix
mat = []

# 1st block, multiply by H^3
hmod = H^3
for i in range(5):
    for bitpos in range(4):
        coeff = 1 << (127 - (8*i + bitpos))
        res = Integer((hmod * F.fetch_int(coeff)).integer_representation())
        # .digits() lists digits in little endian but that doesn't end up mattering
        mat.append(res.digits(base=2, padto=128))

# 2nd block, multiply by H^2
hmod = H^2
for i in range(16):
    for bitpos in range(4):
        coeff = 1 << (127 - (8*i + bitpos))
        res = Integer((hmod * F.fetch_int(coeff)).integer_representation())
        mat.append(res.digits(base=2, padto=128))

# 3rd block, multiply by H
# top 5 bytes available
hmod = H
for i in range(11):
    for bitpos in range(4):
        coeff = 1 << (127 - (8*(i+5) + bitpos))
        res = Integer((hmod * F.fetch_int(coeff)).integer_representation())
        mat.append(res.digits(base=2, padto=128))

# why it doesn't matter that .digits() lists in little endian
target_digits = vector(GF(2), Integer(target_diff).digits(base=2, padto=128))
M = matrix(GF(2), mat)

ans = M.solve_left(target_digits)

b1xor = 0
for i in range(5):
    for bitpos in range(4):
        b1xor += Integer(ans[i*4+bitpos]) * (1 << (127 - (8*i + bitpos)))

b2xor = 0
for i in range(16):
    for bitpos in range(4):
        b2xor += Integer(ans[(i+5)*4+bitpos]) * (1 << (127 - (8*i + bitpos)))

b3xor = 0
for i in range(11):
    for bitpos in range(4):
        b3xor += Integer(ans[(i+21)*4+bitpos]) * (1 << (127 - (8*(i+5) + bitpos)))

# double check
assert (F.fetch_int(b1xor) * H^3 + F.fetch_int(b2xor) * H^2 + F.fetch_int(b3xor) * H).integer_representation() == target_diff

# reverse again to get something we can apply directly via xor
print(rev_block_int(b1xor))
print(rev_block_int(b2xor))
print(rev_block_int(b3xor))
