%{
#include <stdio.h>
#include <string.h>
int is_keyword(char *str) {
    char *keywords[] = {"auto", "break", "case", "char", "const", "continue", "default", "do",
                        "double", "else", "enum", "extern", "float", "for", "goto", "if",
                        "int", "long", "register", "return", "short", "signed", "sizeof",
                        "static", "struct", "switch", "typedef", "union", "unsigned",
                        "void", "volatile", "while"};
    int num_keywords = sizeof(keywords) / sizeof(keywords[0]);
    for (int i = 0; i < num_keywords; i++) {
        if (strcmp(str, keywords[i]) == 0)
            return 1;
    }
    return 0;
}
void lexical_error(const char *msg) {
    printf("Lexical Error: %s\n", msg);
}

FILE *yyin;
%}
%%
"/*"[^*]*"*"+([^*/][^*]*"*"+)*"/"    { }
"//".*                                { }
[ \t\r]+                             { }
[\n]                                 { }
"auto"|"break"|"case"|"char"|"const"|"continue"|"default"|"do"|"double"|"else"|"enum"|"extern"|"float"|"for"|"goto"|"if"|"int"|"long"|"register"|"return"|"short"|"signed"|"sizeof"|"static"|"struct"|"switch"|"typedef"|"union"|"unsigned"|"void"|"volatile"|"while"    { printf("Keyword: %s\n", yytext); }
[a-zA-Z_][a-zA-Z0-9_]*              { 
                                        if (is_keyword(yytext)) {
                                            printf("Keyword: %s\n", yytext);
                                        } else {
                                            printf("Identifier: %s\n", yytext);
                                        }
                                    }
[0-9]+                              { printf("Constant: %s\n", yytext); }
\"([^"\\]|\\.)*\"                   { printf("String: %s\n", yytext); }
[+\-*/%=!<>]=?                      { printf("Operator: %s\n", yytext); }
[;,(){}\[\]]                        { printf("Punctuation: %s\n", yytext); }
[0-9]+[a-zA-Z]+                     { lexical_error(yytext); }
.                                   { lexical_error("Invalid character encountered"); }
%%
int main() {
    // testcase 1 file: /workspaces/DLP-PRACTICALS/practical_5/test1.c
    // testcase 2 file: /workspaces/DLP-PRACTICALS/practical_5/test2.c
    // testcase 3 file: /workspaces/DLP-PRACTICALS/practical_5/test3.c
    yyin = fopen("/workspaces/DLP-PRACTICALS/practical_5/test2.c", "r");
    if (!yyin) {
        printf("Could not open File.c\n");
        return 1;
    }
    
    yylex();
    fclose(yyin);
    return 0;
}
int yywrap(void) {
    return 1;
}
