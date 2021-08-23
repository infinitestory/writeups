from pwn import *

xor_rules = r"""
^:(%)
*%$::0

0(:(0
1(:(1
)0:0)
)1:1)

(:*
):$

a0:0a
a1:1a
b0:0b
b1:1b

0a:c
1b:c
0b:d
1a:d

0%:%a
1%:%b

*%0:*%
*%1:1!%
*%a:*%
*%b:1!%
*%c:*%
*%d:1!%
!%0:0!%
!%1:1!%
!%a:0!%
!%b:1!%
!%c:0!%
!%d:1!%

!%$::
""".splitlines()
xor_rules = list(filter(lambda x: x != '', xor_rules))

mul_rules = r"""
_0:_
_1:_
_|:-
-1:1+
-0=::0
-0:-
+1:1+
+0:0+
-\:-
+\:+
-$:-
+$:+
-=::
+=::

x:(%)

0(:(0
1(:(1
)0:0)
)1:1)

(:*
):|0$=

c0:0c
c1:1c
d0:0d
d1:1d
c|:|c
d|:|d
0c$:\$0
1c$:\$1
0d$:\$1
1d$:/$0
|c$:|\$0
|d$:|\$1

0c\:\0
0d\:\1
1c\:\1
1d\:/0
0c/:\1
0d/:/0
1c/:/0
1d/:/1
|c\:|\0
|d\:|\1
|c/:|\1
|d/:|/0

a]:]c0
b]:]d1

#|:|#
0#$:$0
1#$:$1
|#$:|$0

%]:%

&|:]|
&0:a&
&1:b&
#0:0#
#1:1#
|/:|1
|\:|
1%:%&
0%:%#

*%:_
""".splitlines()
mul_rules = list(filter(lambda x: x != '', mul_rules))

r = remote('maotiplication.be.ax', 6000)

r.recvuntil('Rule: ')
r.sendline('strellic:')
r.recvuntil('Rule: ')
r.sendline('::jsgod')
r.recvuntil('Rule: ')
r.sendline('EOF')

for rule in xor_rules:
    r.recvuntil('Rule: ')
    r.sendline(rule)
r.recvuntil('Rule: ')
r.sendline('EOF')

for rule in mul_rules:
    r.recvuntil('Rule: ')
    r.sendline(rule)
r.interactive()
r.recvuntil('Rule: ')
r.sendline('EOF')
