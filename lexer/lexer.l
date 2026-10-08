%{
#include <stdio.h>
%}

%%

"let"       { printf("TOKEN  LET              %s\n", yytext); }
"print"     { printf("TOKEN  PRINT            %s\n", yytext); }
"if"        { printf("TOKEN  IF               %s\n", yytext); }
"else"      { printf("TOKEN  ELSE             %s\n", yytext); }

"=="        { printf("TOKEN  EQUAL            %s\n", yytext); }
">="        { printf("TOKEN  GREATER_EQUAL    %s\n", yytext); }
"<="        { printf("TOKEN  LESS_EQUAL       %s\n", yytext); }
"="         { printf("TOKEN  ASSIGN           %s\n", yytext); }

">"         { printf("TOKEN  GREATER_THAN     %s\n", yytext); }
"<"         { printf("TOKEN  LESS_THAN        %s\n", yytext); }

"+"         { printf("TOKEN  PLUS             %s\n", yytext); }
"-"         { printf("TOKEN  MINUS            %s\n", yytext); }
"*"         { printf("TOKEN  MULTIPLY         %s\n", yytext); }
"/"         { printf("TOKEN  DIVIDE           %s\n", yytext); }


"//"[^\n]* {/* Ignore comment */}


"("         { printf("TOKEN  LPAREN           %s\n", yytext); }
")"         { printf("TOKEN  RPAREN           %s\n", yytext); }
"{"         { printf("TOKEN  LBRACE           %s\n", yytext); }
"}"         { printf("TOKEN  RBRACE           %s\n", yytext); }
":"         { printf("TOKEN  COLON            %s\n", yytext); }
","         { printf("TOKEN  COMMA            %s\n", yytext); }
";"         { printf("TOKEN  SEMICOLON        %s\n", yytext); }

[0-9]+\.[0-9]+ {
    printf("TOKEN  FLOAT            %s\n", yytext);
}

[0-9]+ {
    printf("TOKEN  INTEGER          %s\n", yytext);
}

\"[^\"]*\" {
    printf("TOKEN  STRING           %s\n", yytext);
}

[a-z]+ {
    printf("TOKEN  IDENTIFIER       %s\n", yytext);
}

[A-Za-z]+ {
    printf("LEXICAL_ERROR    %s\n", yytext);
}

[ \t\r\n]+ {
}

. {
    printf("LEXICAL_ERROR    %s\n", yytext);
}

%%

int main(void)
{
    FILE *file = fopen("program.txt", "r");

    if (file == NULL)
    {
        printf("Error: Could not open program.txt\n");
        return 1;
    }

    yyin = file;

    yylex();

    fclose(file);

    return 0;
}

int yywrap(void)
{
    return 1;
}