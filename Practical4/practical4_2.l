%{
#include <stdio.h>
%}

%%
charusat {printf("university");}
CHARUSAT {printf("UNIVERSITY");}
Charusat {printf("University");}
\n {printf("\n");}
. {printf("%s", yytext);}

%%

int yywrap(){
    return 0;
}

int main(){
    yylex();
    return 0;
}