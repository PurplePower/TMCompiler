# Turing Machine Compiler

Turing Machine programs are effectively state machines, 
which can be represented in flow charts or tuple of 5.

However, constructing such a state machine directly 
can be difficult. A higher level language can be useful
in such cases.

The language defined as below:


```yacc
SYMBOL : ‘0’ | ‘1’

action : LEFT | RIGHT | WRITE SYMBOL | HALT

program : stmt_seq

stmt_seq : stmt_seq stmt | empty

stmt : action | while_stmt | if_stmt | goto_stmt | labelled_stmt

label : ID

lebelled_stmt: label ‘:’ stmt

while_stmt : WHILE ( SYMBOL ) action

goto_stmt : GOTO label

if_stmt : IF ( SYMBOL ) action | IF ( SYMBOL ) GOTO label
```

Each `stmt` corresponds to one state, with edges going out.
In this way writing a turing machine program looks like
programming using some assembly-like language.


E.g. 
```txt
write 1
right
if (0) goto L1
while (1) right

L1:
halt
```

More examples can be found in `/src/`.

`ply` package is used for compiler construction, where rules files
are in `lex_rules.py` and `yacc_rules.py`.

`main.py` parse a txt input as a program, construct a state machine
and output 5-tuple to a script. You can simulate the state machine
simply copying the script to https://morphett.info/turing/turing.html
and set your input.



