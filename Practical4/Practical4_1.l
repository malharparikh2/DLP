%%
[0-9]+ {printf("%s\n", yytext);} 
[0-9]+\*\*[0-9] {
    int base = atoi(yytext);
    int exp = yytext[strlen(yytext)-1] - '0';
    int result = 1;
    for(int i = 0; i < exp; i++) {
        result *= base;
    }
    printf("%d\n", result);
}

[0-9]+[ ]*\*\*[ ]*[0-9] {
    int base = atoi(yytext);
    int exp = yytext[strlen(yytext)-1] - '0';
    int result = 1;
    for(int i = 0; i < exp; i++) {
        result *= base;
    }
    printf("%d\n", result);
}

[0-9]+\*[0-9]+ {
    int i;
    int num1 = 0, num2 = 0;
    for(i = 0; yytext[i] != '*'; i++) {
        num1 = num1 * 10 + (yytext[i] - '0');
    }
    i++;
    for(; i < strlen(yytext); i++) {
        num2 = num2 * 10 + (yytext[i] - '0');
    }
    printf("%d\n", num1 * num2);
}  

[0-9][ ]*+\*[ ]*[0-9]+ {
    int i;
    int num1 = 0, num2 = 0;
    for(i = 0; yytext[i] != '*'; i++) {
        num1 = num1 * 10 + (yytext[i] - '0');
    }
    i++;
    for(; i < strlen(yytext); i++) {
        num2 = num2 * 10 + (yytext[i] - '0');
    }
    printf("%d\n", num1 * num2);
}
[^0-9] ;
%%
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int yywrap(void) {
    return 1;
}

int main(void) {
    yylex();
    return 0;
}
