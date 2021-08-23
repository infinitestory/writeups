# mystery_stream
crypto // qopruzjf // 2021 corCTF

## Setup

We are provided with the source code of a stream cipher, and a ciphertext created by running this stream cipher on some input.  The flag has been randomly inserted somewhere into the plaintext.  This stream cipher uses a single [LFSR](https://en.wikipedia.org/wiki/Linear-feedback_shift_register) of length 64 to generate pad bytes, which are multiplied by the plaintext bytes in GF(256).  We're also provided the program used to generate the 64-bit key, which is the initial state of the LFSR.

## Solution

This is almost certainly not the intended solution, as it completely bypasses periodic analysis of the LFSR and any constraints introduced by the key generation.

Due to the structure of single-LFSR stream ciphers, at any point during encryption, the state of the LFSR is just the concatenation of the most recent 8 pad bytes generated.  Therefore, if we can guess any 8-character block of plaintext, we can recover a guess for the LFSR state at the end of those 8 characters, and then use that LFSR state to decrypt the next several characters.  It's not a stretch of the imagination to assume that the flag is entirely composed of ascii-printable characters, is at least 30 characters long including prefix, and most notably starts with the string `corctf{`, which is 7 characters already and completely fixed.  The ciphertext is only ~100k characters long, so even if we guess every single ascii-printable character for the first character of the flag, that's ~10M total guesses and easily feasible to compute.  Then, the chance that the next 22 characters are all printable ascii is less than `1/2^22`, so on average we should only see ~2 guesses of noise.

Running this solution method recovers the flag at position 24145, `corctf{p3ri0dic4lly_l00ping_on_4nd_on...}`.  The plaintext is [an English translation of Kenji Miyazawa's _Night on the Milky Way Train_](http://ircamera.as.arizona.edu/NatSci102/NatSci/kenji/main.htm).

A few notes about the solution code:

```
        # guess loop constructs state in reverse bit order, there has to be a better way to do this
        state = int(''.join([str(b) for b in Integer(state).bits()]), 2)
```

This is probably one of the worst lines of code I've ever written, but because Sage's documentation is so unsearchable, I couldn't find an easy util to reverse a bit string.  The state of the LFSR is in big-endian order.  In other words, the lowest-order bit of the state is the top-order bit of the pad byte used 8 characters ago.  Sage's `.bits()` util for some reason provides a list of bits in big-endian order, so we need only convert that back to an int in the same order.

Also, even if the flag ended up being shorter than 30 characters, ~21 characters still probably would have been manually doable, since that's ~1k guesses of noise.  That's still easily feasible to sift through manually.

And if we had taken the further assumption that the input plaintext was in _English_, we could have instead searched for `because `, which is a string that's almost guaranteed to show up in any English plaintext of this length.  This also works and is notably totally independent of the flag structure, so this attack works just fine in a non-CTF context.
