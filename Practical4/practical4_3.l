%{
#include <stdio.h>
int words = 0;
int chars = 0;
int lines = 0;
int spaces = 0;
int tabs = 0; 
%}

%%
\n      { lines++; }
[ ]+    { spaces += yyleng; }
[\t]+   { tabs += yyleng; }
[a-zA-Z]+ { 
            chars += yyleng;
            words++;
        }
[^a-zA-Z \t\n]+ { 
            chars += yyleng;
        }
<<EOF>>	{ lines++; return 0;}
%%

int yywrap(){
    return 1;
}

int main(){
    FILE *fp;
    fp = fopen("/workspaces/DLP-PRACTICALS/practical_4/test.txt", "r");
    yyin = fp;

    yylex();
    printf("No. of lines: %d\n", lines);
    printf("No. of words: %d\n", words);
    printf("No. of characters: %d\n", chars);
    printf("No. of tabs: %d\n", tabs);
    printf("No. of spaces: %d\n", spaces);
    return 0;
}