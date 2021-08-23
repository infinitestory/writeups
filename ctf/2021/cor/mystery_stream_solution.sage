import string

def bsum(state, taps, l):
	ret = 0
	for i in taps:
		ret ^^= (state >> (l - i))
	return ret & 1

class Gen:
	def __init__(self, key, slength):
		self.state = key
		self.slength = slength
		self.TAPS = [2, 4, 5, 7, 10, 12, 13, 17, 19, 24, 25, 27, 30, 32, 
		33, 34, 35, 45, 47, 49, 50, 52, 54, 56, 57, 58, 59, 60, 61, 64]

	def clock(self):
		out = bsum(self.state, self.TAPS, self.slength)
		self.state = (out << (self.slength - 1)) + (self.state >> 1)
		return out

F = GF(2^8, name='x', modulus=x^8 + x^4 + x^3 + x + 1)

with open('ct', 'rb') as f:
    ct = f.read()

for guess_idx in range(len(ct)):
    for guess_flag_start in string.printable:
        guess_flag = ('corctf{' + guess_flag_start).encode('ascii')
        
        # this works too and doesn't rely on knowing the flag structure
        # guess_flag = 'because '.encode('ascii')
        # guess_flag_start = ''
        
        state = 0
        ok = True
        for idx, c in enumerate(guess_flag):
            state <<= 8
            plain_byte = c
            enc_byte = ct[idx + guess_idx]
            if plain_byte == 0:
                ok = False
                break
            state_byte = (F.fetch_int(enc_byte) / F.fetch_int(plain_byte)).integer_representation()
            state += state_byte
        if not ok:
            continue

        # guess loop constructs state in reverse bit order, there has to be a better way to do this
        state = int(''.join([str(b) for b in Integer(state).bits()]), 2)
        cipher = Gen(state, 64)
        
        out = b''
        ok = True
        for idx in range(8, 24):
            state_byte = 0
            for i in range(8):
                state_byte = state_byte << 1
                state_byte += cipher.clock()
            enc_byte = ct[idx + guess_idx]
            if state_byte == 0:
                ok = False
                break
            plain_byte = (F.fetch_int(enc_byte) / F.fetch_int(state_byte)).integer_representation()
            if plain_byte < 32 or plain_byte > 126:
                ok = False
                break
            out += plain_byte.to_bytes(1, 'big')
        if ok:
            print('idx: {}, guess: {}, next: {}'.format(guess_idx, guess_flag_start, out))
