# maotiplication
misc // drakon // 2021 corCTF

## Setup

We are given three tasks which each involve taking an input string and transforming it in a specific way:
* input: 'strellic' repeated an arbitrary number of times; desired output: 'jsgod' - this is a tutorial challenge and won't be discussed in here
* input: two binary numbers with a `^` between them; desired output: the xor of those numbers in binary
* input: two binary numbers with a `x` between them; desired output: the product of those numbers in binary

To accomplish these tasks, we are allowed to provide an ordered list of literal string substitution rules.  The tester will repeatedly look through the list of rules, find the top one that matches the current string, and execute it.  There are also two special functionalities we can use.  We can specify a rule as terminal, which causes the tester to return when it runs that rule.  Also, if the left hand of the substitution rule is empty, the rule will instead prepend the right hand string to the current state.  Those rules match all strings.

The solutions I used here are almost certainly not minimal.  In fact, both of them probably have at least a few rules that are never executed, but I didn't bother optimizing them.  Don't treat them as optimal in any way.

## xor

```
initialization
^:(%)
*%$::0

0(:(0
1(:(1
)0:0)
)1:1)

(:*
):$

move a/b to the right
a0:0a
a1:1a
b0:0b
b1:1b

compute xor
0a:c
1b:c
0b:d
1a:d

generate a/b
0%:%a
1%:%b

cleanup
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
```

Example: `10111^1111010`

We begin by doing some initialization.  The `^` emits some parentheses, which migrate to the left and right ends of the string and then become a `*` and `$` respectively.  The `^` also becomes a `%` to make this a onetime step.

`*10111%1111010$`

If there are no `a` or `b`, the `%` will consume a binary digit on its left and turn it into a corresponding `a` or `b` on its right.

`*1011%b1111010$`

The `a` or `b` will then migrate all the way to its right until it reaches the `$`, at which point it stops.

`*1011%1111010b$`

Then, the lower-priority rule will compute xor on the `a` or `b` and the binary digit to its left.  (If none exist, the letter will stay a letter and be converted back to a digit at the cleanup step later).  The result of this xor will be represented as `c` or `d` so that future `a` or `b` digits cannot move past it.

`*1011%111101d$`

This repeats until there are no digits to the left of the `%`.

`*%11cddcd$`

At this point, the rules which contain `*%` kick in and start consuming digits and letters.  We don't want trailing zeroes, so we define a protocol where `*%` indicates that the leading 1 has not yet been found, but `!%` indicates that it has.  Therefore, `*%` will consume 0, `a`, and `c` entirely, whereas `!%` will turn them into 0.

`1101101!%$`

Then the rule `!%$::` cleans up all control characters and terminates the procedure.  As a special case, `*%$` can only exist if the correct answer is 0, so we output 0 in that case as the final transformation.

## multiplication

```
cleanup
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

initialization
x:(%)

0(:(0
1(:(1
)0:0)
)1:1)

(:*
):|0$=

move c/d to the right
c0:0c
c1:1c
d0:0d
d1:1d
c|:|c
d|:|d

generate \ or / (minor digit position pointer) and compute first addition
also bump $ (major digit position pointer)
0c$:\$0
1c$:\$1
0d$:\$1
1d$:/$0
|c$:|\$0
|d$:|\$1

compute addition when slash is already present
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

use ] to convert a/b to c0/d1 to duplicate the right operand
a]:]c0
b]:]d1

generate # by consuming 0 from left operand
#|:|#
0#$:$0
1#$:$1
|#$:|$0

generate & by consuming 1 from left operand
turn 0/1 to a/b using &
turn & to ] when it reaches the end of the right operand
and other detritus that may or may not be required
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
```

This is extremely unoptimized, and certainly has some totally dead rules.  After the initialization step, there are roughly 3 chunks of the string: a left operand, a right operand, and an answer section.  The general algorithm is to repeatedly consume a digit from the left operand, while maintaining a major digit position pointer (`$`) within the answer section.  If the left operand digit consumed is 0, we bump the major digit position pointer one space to the left.  Otherwise, we duplicate the right operand, and use a minor digit position pointer (`\` or `/`, to represent carry state) to add the right operand to the answer section starting from the major digit position pointer.

Example: `10101x1111010`

Initialize structure.  | delimits the boundary between the right operand and the answer section.

`*10101%1111010|0$=`

Consume a digit from the left operand.  Since it's a 1, we consume it as a `&`.

`*1010%&1111010|0$=`

The `&` wipes over the right operand, converting it to `a`/`b` and converting itself to a `]` when it hits the `|` delimiter.

`*1010%bbbbaba]|0$=`

The newly transformed `]` now wipes backwards over the right operand, duplicating its digits.

`*1010%bbbbab]c0|0$=`

`c` and `d` migrates to the right where it begins performing addition.

`*1010%bbbbab]0|0c$=`

Since the `c` is meeting the `$`, it will compute an addition, bump the major digit pointer since that's the last time that digit can be modified, and then generate a minor digit pointer based on carry state.

`*1010%bbbbab]0|\$0=`

The `]` now continues wiping to the left, producing `c` and `d`.

`*1010%bbbba]d10|\$0=`

`*1010%bbbba]10|d\$0=`

`*1010%bbbba]10|d\$0=`

`*1010%bbbba]10|\1$0=`

Notice how the `$` was only bumped once, but the `\` is being bumped every time an addition operation happens.  This process continues.

`*1010%]1111010|\111101$0=`

The `]` is now consumed to return to the idle state, as is the minor digit pointer.  The minor digit pointer is converted to a 1 if it represents a carry.

`*1010%1111010|111101$0=`

Next, we consume a 0, which becomes a `#`.

`*101%#1111010|111101$0=`

This migrates all the way to the `$` without interacting with any other symbols.

`*101%1111010|111101#$0=`

The major position pointer is bumped with no other changes to the answer state.

`*101%1111010|11110$10=`

This process repeats until the left operand contains no more digits.

`*%1111010|1010000$00010=`

`*%` matches the cleanup rule which converts that symbol to a `_`.  This rule has an extremely low priority so we can complete the operation resulting from consuming the last left operand digit.

`_1111010|1010000$00010=`

`_` consumes all symbols until it reaches the `|` delimiter, at which point it becomes a `-`.  This character consumes leading 0s, becoming a `+` if it finds a 1.  I don't think there actually can be leading zeros, but better safe than sorry.

`-1010000$00010=`
`101000000010+=`

`+=` triggers final cleanup and is the terminal rule.  As a special case, if one operand is 0, `-0=` becomes `0` and terminates.

`101000000010`