import random
from interpreter import apply_runs

FLAG = "REDACTED"

def intro():
    rep = random.randint(1, 10)
    test = "strellic"*rep
    expected = "jsgod"
    return (test, expected)

def xor():
    a = random.randint(0, 255)
    b = random.randint(0, 255)
    c = a^b
    test = bin(a)[2:] + '^' + bin(b)[2:]
    expected = bin(c)[2:]
    return (test, expected)

def mult():
    a = random.randint(0, 255)
    b = random.randint(0, 255)
    c = a*b
    test = bin(a)[2:] + 'x' + bin(b)[2:]
    expected = bin(c)[2:]
    return (test, expected)

def run_round(test_case, max_operations, max_rules, trials=256, use_rules=None):
    for i in range(5):
        case = test_case()
        print(f"\'{case[0]}\' => \'{case[1]}\'")

    print(f"\nConstraints: {max_rules} rules, {max_operations} substitutions\n\n")

    if use_rules != None:
        rules = [rule.split(':') for rule in use_rules]
    else:
        rules = []
        while True:
            rule = input('Rule: ')
            if ':' in rule:
                rules.append(rule.split(':'))
            elif 'EOF' in rule:
                break
        
    if len(rules) > max_rules:
        print('Maximum rules exceeded!')
        exit()
   
    for i in range(trials):
        case = test_case()
        result = apply_runs(case[0], rules, max_operations=max_operations)
        if result != case[1]:
            print(f"\'{case[0]}\' => \'{result}\' (Test Failed, expected \'{case[1]}\')")
            exit()
    print("All tests passed!\n\n")


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

# Run the demo from the writeup
print('xor demo:')
print('------')
apply_runs('10111^1111010', [rule.split(':') for rule in xor_rules], debug=True)
print('------')

# Run a real test round
# run_round(xor, 120, 50, use_rules=xor_rules)

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

# Run the demo from the writeup
print('mul demo:')
print('------')
apply_runs('10101x1111010', [rule.split(':') for rule in mul_rules], debug=True)
print('------')

# Run a real test round
# run_round(mult, 2500, 100, use_rules=mul_rules, trials=256)