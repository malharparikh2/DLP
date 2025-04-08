%{
    #include <stdio.h>
    int upper = 0;
    int lower = 0;
    int num = 0;
    int special = 0;
    int length = 0;

    void validate(){
        if(upper < 1 || lower < 1 || num < 1 || special < 1 || length < 9 || length > 10){
            printf("Invalid Password\n");
        }
        else{
            printf("Valid Password\n");
        }
    }
%}

%%
[A-Z] {upper++; length++;}
[a-z] {lower++; length++;}
[0-9] {num++; length++;}
[*,;#$@] {special++; length++;}
\n {validate(); return 0;}
. {printf("Invalid password\n"); return 0;}
%%

int yywrap(){
    return 0;
}

int main(){

    yylex();
    return 0;
}