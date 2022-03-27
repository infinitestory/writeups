# OK
crypto // theoremoon, keymoon // 2022 zer0pts ctf

## Setup

We are interacting a server that is doing some computations reminiscent of RSA encryption on the flag, though with a major difference that the flag has been XOR'd against a random one-time pad ("key"), with the result being called "ciphertext".  Two random numbers `x1` and `x2` are then generated and provided to us.  We are given a 1-query oracle which allows us to submit a number, which is combined with `x1` and `x2` respectively in a particular way.  The results are then added to the key and ciphertext respectively, and printed.  The goal is to recover the flag, presumably by computing the XOR of the key and ciphertext.

## In-depth inspection of calculations

The beginning portion of the calculations is consistent with standard RSA.  `e` is set to 65537.  Two 512-bit primes `p` and `q` are chosen, their product `n` computed, and `d = inverse(e, (p-1)*(q-1))` is computed.  `n` is revealed to us.

From here, the scheme diverges from RSA.  The flag is taken to the power of `e` mod `P`, where `P` is a fixed value (it's the largest 999-bit prime) and has nothing to do with `p`, `q,` or `n`.  Since `P` is a fixed prime, we can in fact precompute what `inverse(e, P-1)` is, so that we can recover the flag from `pow(flag, e, P)`.

A one-time pad `key` is randomly generated from 0 to `n`, and XOR'd with the modified flag to get a `ciphertext`.  Note that the `key` and `ciphertext` are in fact symmetric; there is no difference in their roles, and we need only compute their XOR to recover the flag.  Two random numbers `x1` and `x2` are also generated and revealed.

We are given an oracle where we can submit a number `v`, which is combined with the above parameters in the following way:

`k1 = pow(v - x1, d, n)`

`c1 = (k1 + key) % n`

`k2 = pow(v - x2, d, n)`

`c2 = (k2 + ciphertext) % n`

Again, these operations are symmetric.  The intermediate values `k1` and `k2` are not revealed, but `c1` and `c2` are.

## Motivation

The flavortext helpfully suggests that if we set `v = x1`, then `k1 = 0` so we can recover `key`, or vice versa to recover `ciphertext`.  However, in either case, `k2` or `k1` will effectively become random noise, so the data from the other parameter will be totally lost.

Indeed, we need to pick a value that retains information on both sides.  Even though the exponentiation means we have little control over `k1` and `k2`, it also seems intuitive that we should pick `v` such that `k1` and `k2` are related if possible.

In keeping with the symmetry of the twin operations, the natural choice is `v = (x1 + x2) / 2`.  With this value, `v - x1 = -(v - x2)`.  Because `d` is always odd, we will then have `k1 = -k2`.  Then, `c1 + c2 = (key + ciphertext) % n`.

## Relations between addition and xor

`key + ciphertext` is not `key ^ ciphertext`, but it is highly related.

Consider any individual bit position of `key ^ ciphertext`, such that there is no incoming carry when adding `key + ciphertext` at that position.  For example, the LSB has this property.

If it is a 0, `key` and `ciphertext` will always have the same bit.  Therefore, `key + ciphertext` will also have a 0 at that position.  A carry bit will be propagated upwards half the time, in the case where both `key` and `ciphertext` have a 1 at this position.  Therefore, there will be no correlation between the value of `key + ciphertext` at this bit position and the next one.

If it is a 1, `key` and `ciphertext` will always have different bits.  Therefore, `key + ciphertext` will also have a 1 at that position, and there will never be a carry bit propagated.  Because there is no carry bit, there will be a perfect correlation between the value of this bit position and the next one.

Now we think about how incoming carries affects the value.

If the position is a 0, then an incoming carry bit will not be propagated.  There will still be no correlation.

If the position is a 1, then an incoming carry bit will propagate through this position and the next one, flipping both of them.  There will still be a perfect correlation.

Therefore, if perform a decent number of trials and observe a perfect correlation between two consecutive bit positions, the lower of the two is a 1 in the XOR.  If not, the lower of the two is a 0.  We will use this property to recover the flag.

Note that we don't actually have `key + ciphertext`, but rather `(key + ciphertext) % n`.  Luckily, because `key` and `ciphertext` are both at most `n`, the value we have is either `key + ciphertext` or `key + ciphertext - n`.  Also, `n` is odd, so if we guess the parity of `key + ciphertext`, we can figure out whether we need to add `n` to the value we have.  It turns out that a similar correlation analysis can be done to figure out the answer for sure, or even rerunning trials until `c1 + c2 > n`, but simply assuming each case and carrying out the rest of the solution also works.

## Solution

We first performed 200 trials where we submitted `v = ((x1 + x2) / 2) % n`, collecting a pair `(c1 + c2, n)` for each.

We determined that `key ^ ciphertext` is odd, so for each pair, if `c1 + c2` was even, we first added `n` to obtain `c1 + c2 + n = key + ciphertext`.

We created a `correlations` array of length 1023, where position `i` of that array is a pair.  The first element of this pair corresponds to the frequency with which the `i`th least-significant bit is the same as the `i+1`th least-significant bit.  The second element of this pair corresponds to the frequency with which they are different.  In essence, we can tally the correlation factor with `correlations[i][f[i] ^ f[i+1]] += 1`, and then taking the difference between the two pair elements at the end

Iterating through all trials, we find that indeed some of the bits have perfect correlation of 200, and the rest have nearly no correlation, as expected.  This lets us recover the values of the lower 1023 bits of `key ^ ciphertext`.  Because `key ^ ciphertext` is a `modexp` computation modulo `P`, where `P` is shorter than `n`, we know the top bit of `key ^ ciphertext` is 0.  Exponentiating the result by `inverse(e, P)` recovers the flag, `zer0pts{hav3_y0u_unwittin91y_acquir3d_th3_k3y_t0_th3_d00r_t0_th3_N3w_W0r1d?}`.