/* lex.l - Lexical analyzer */
%{
#include <stdio.h>
#include "y.tab.h"
%}

%%
i       { return I; }
t       { return T; }
a       { return A; }
e       { return LETTER_E; }  /* Changed from E to LETTER_E to avoid conflict */
b       { return B; }
\n      { return NL; }
.       { return yytext[0]; }
%%

int yywrap() {
    return 1;
}
