
%{
#include <stdio.h>
#include <string.h>
%}


%%

"let"       { printf("%-20s %s\n", "LET", yytext); }
"print"     { printf("%-20s %s\n", "PRINT", yytext); }
"if"        { printf("%-20s %s\n", "IF", yytext); }
"else"      { printf("%-20s %s\n", "ELSE", yytext); }

"=="        { printf("%-20s %s\n", "EQUAL", yytext); }
">="        { printf("%-20s %s\n", "GREATER_EQUAL", yytext); }
"<="        { printf("%-20s %s\n", "LESS_EQUAL", yytext); }
"="         { printf("%-20s %s\n", "ASSIGN", yytext); }

">"         { printf("%-20s %s\n", "GREATER_THAN", yytext); }
"<"         { printf("%-20s %s\n", "LESS_THAN", yytext); }

"+"         { printf("%-20s %s\n", "PLUS", yytext); }
"-"         { printf("%-20s %s\n", "MINUS", yytext); }
"*"         { printf("%-20s %s\n", "MULTIPLY", yytext); }
"/"         { printf("%-20s %s\n", "DIVIDE", yytext); }

"//"[^\n]*  { /* Ignore comments */ }

"("         { printf("%-20s %s\n", "LPAREN", yytext); }
")"         { printf("%-20s %s\n", "RPAREN", yytext); }
"{"         { printf("%-20s %s\n", "LBRACE", yytext); }
"}"         { printf("%-20s %s\n", "RBRACE", yytext); }
":"         { printf("%-20s %s\n", "COLON", yytext); }
","         { printf("%-20s %s\n", "COMMA", yytext); }
";"         { printf("%-20s %s\n", "SEMICOLON", yytext); }

[0-9]+\.[0-9]+ {
    printf("%-20s %s\n", "FLOAT", yytext);
}

[0-9]+ {
    printf("%-20s %s\n", "INTEGER", yytext);
}


\"[^\n\"]*\" {
    printf("%-20s %s\n", "STRING", yytext);
}

\"[^\n\"]* {
    printf("%-20s %s\n", "LEXICAL_ERROR", yytext);
}

[A-Z]+ {
    printf("%-20s %s\n", "LEXICAL_ERROR", yytext);
}

[a-z]+ {
    if (strcmp(yytext, "let") == 0)
        printf("%-20s %s\n", "LET", yytext);
    else if (strcmp(yytext, "print") == 0)
        printf("%-20s %s\n", "PRINT", yytext);
    else if (strcmp(yytext, "if") == 0)
        printf("%-20s %s\n", "IF", yytext);
    else if (strcmp(yytext, "else") == 0)
        printf("%-20s %s\n", "ELSE", yytext);
    else
        printf("%-20s %s\n", "IDENTIFIER", yytext);
}

[ \t\r\n]+ {
    /* Ignore whitespace */
}

. {
    printf("%-20s %s\n", "LEXICAL_ERROR", yytext);
}

%%



int main(void)
{
    FILE *file = fopen("../program.txt", "r");

    if (file == NULL)
    {
        printf("Error: Cannot open program.txt\n");
        return 1;
    }

    yyin = file;

    printf("Tokens:\n\n");
    yylex();

    fclose(file);

    return 0;
}


int yywrap(void)
{
    return 1;
}
