/* yacc.y - Syntax analyzer */
%{
#include <stdio.h>
#include <stdlib.h>

void yyerror(char *msg);
int yylex();
%}

%token I T A LETTER_E B NL

%%
start: S NL { printf("Valid String\n"); return 0; }
     ;

S: I E T S Sprime
 | A Sprime
 ;

Sprime: LETTER_E S
      | /* epsilon - empty */
      ;

E: B
 ;

%%

void yyerror(char *msg) {
    printf("Invalid String\n");
    exit(0);
}

int main() {
    printf("Enter a string to parse: ");
    int result = yyparse();
    return result;
}