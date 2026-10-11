
%{
#include <stdio.h>
#include <string.h>
%}

%x STRING_STATE

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


[a-z]+ {
    printf("%-20s %s\n", "IDENTIFIER", yytext);
}



[A-Za-z]+ {
    printf("%-20s %s\n", "LEXICAL_ERROR", yytext);
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
    char source_code[10000];
    char line[1000];

    source_code[0] = '\0';

    printf("Enter your program.\n");
    printf("Type END on a new line when finished.\n\n");

    while (fgets(line, sizeof(line), stdin) != NULL)
    {
        if (strcmp(line, "END\n") == 0 ||
            strcmp(line, "END\r\n") == 0 ||
            strcmp(line, "END") == 0)
        {
            break;
        }

        if (strlen(source_code) + strlen(line) >= sizeof(source_code))
        {
            printf("Input is too long.\n");
            return 1;
        }

        strcat(source_code, line);
    }

    YY_BUFFER_STATE buffer = yy_scan_string(source_code);

    printf("\nTokens:\n\n");

    yylex();

    yy_delete_buffer(buffer);

    return 0;
}



int yywrap(void)
{
    return 1;
}
