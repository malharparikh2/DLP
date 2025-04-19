# Makefile for the YACC string parser

all: parser

parser: y.tab.c lex.yy.c
	gcc -o parser y.tab.c lex.yy.c -ll

y.tab.c: yacc.y
	yacc -d yacc.y

lex.yy.c: lex.l
	lex lex.l

clean:
	rm -f parser y.tab.c y.tab.h lex.yy.c