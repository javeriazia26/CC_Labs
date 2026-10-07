# Simple Programming Language --- Lexer

## 1. Introduction

This project implements the **lexical analyzer (lexer)** for a simple
programming language as part of a Compiler Construction project.

The language supports:

-   Variable declaration and assignment
-   Printing values
-   Arithmetic operators
-   Comparison operators
-   Conditional statements
-   Single-line comments
-   Integer, floating-point, and string literals

The lexer reads the source program from `program.txt`, recognizes valid
lexical patterns, and prints the corresponding tokens.

The lexer also reports lexical errors for invalid characters and invalid
alphabetic patterns.

> **Current project stage:** Lexer only. Parser implementation is not
> part of the current stage.

------------------------------------------------------------------------

## 2. Language Overview

A basic program can contain statements such as:

``` text
let a = 10;
let b = 2.5;
let message = "Hello";

print(a);
print(message);

if (a > 5) {
    print("Greater");
} else {
    print("Smaller");
}
```

Comments can be added using `//`:

``` text
let a = 10; // assign 10 to a
```

Everything after `//` until the end of that line is ignored by the
lexer.

------------------------------------------------------------------------

# 3. Keywords

The language contains the following reserved keywords:

  Keyword   Token     Description
  --------- --------- ---------------------------------
  `let`     `LET`     Declares and assigns a variable
  `print`   `PRINT`   Displays a value
  `if`      `IF`      Starts a conditional statement
  `else`    `ELSE`    Provides an alternative block

Keywords must be written in lowercase.

Valid:

``` text
let
print
if
else
```

These are **not** recognized as keywords:

``` text
Let
Print
IF
Else
```

------------------------------------------------------------------------

# 4. Identifiers

Identifiers are used as variable names.

## Rule

An identifier consists of **one or more lowercase English letters from
`a` to `z`**.

The lexical pattern is:

``` text
[a-z]+
```

Valid identifiers:

``` text
a
x
abc
hello
student
variable
```

Invalid identifier forms:

``` text
A
ABC
Abc
abc1
a_b
```

The identifier rule is **not limited to one letter**. Multiple lowercase
letters are allowed.

------------------------------------------------------------------------

# 5. Literals / Values

The language supports:

1.  Integer literals
2.  Floating-point literals
3.  String literals
4.  Identifiers as values

------------------------------------------------------------------------

## 5.1 Integer Literals

Integers are whole numbers without a decimal point.

Examples:

``` text
0
5
10
100
102
```

Lexical pattern:

``` text
[0-9]+
```

Token:

``` text
INTEGER
```

------------------------------------------------------------------------

## 5.2 Floating-Point Literals

A floating-point number contains digits, a decimal point, and one or
more digits after the decimal point.

Examples:

``` text
2.5
5.0
10.25
100.75
```

Lexical pattern:

``` text
[0-9]+\.[0-9]+
```

Token:

``` text
FLOAT
```

A decimal point must have digits on both sides.

Therefore:

``` text
10.5
```

is a valid float.

The following are not valid float literals:

``` text
10.
.5
```

------------------------------------------------------------------------

## 5.3 String Literals

A string is enclosed in double quotation marks.

Examples:

``` text
"Hello"
"Hello World"
"Student"
"123"
```

Lexical pattern:

``` text
\"[^\"]*\"
```

Token:

``` text
STRING
```

The opening and closing quotation marks are required.

An unterminated string is treated as a lexical error.

------------------------------------------------------------------------

# 6. Variable Declaration and Assignment

Variables are declared using the `let` keyword.

Basic form:

``` text
let identifier = value;
```

Examples:

``` text
let a = 10;
let b = 5.5;
let c = "Hello";
let student = 100;
```

For:

``` text
let a = 10;
```

the lexer recognizes:

``` text
let       → LET
a         → IDENTIFIER
=         → ASSIGN
10        → INTEGER
;         → SEMICOLON
```

The language does not require an explicit data type in the declaration.

------------------------------------------------------------------------

# 7. Assignment Operator

The assignment operator is:

``` text
=
```

Token:

``` text
ASSIGN
```

Example:

``` text
let x = 10;
```

------------------------------------------------------------------------

# 8. Print Statement

The `print` keyword is recognized as:

``` text
PRINT
```

Examples:

``` text
print(x);
print("Hello");
print(10);
print(5.5);
```

The lexer only identifies the individual tokens. Whether the tokens form
a valid print statement is a parser/grammar responsibility.

------------------------------------------------------------------------

# 9. Conditional Statements

The language contains:

``` text
if
else
```

Tokens:

``` text
IF
ELSE
```

Conditions can use comparison operators.

Examples:

``` text
if x > 5:
if a == b:
if number >= 10:
```

The lexer recognizes the individual keywords, operators, and symbols.

------------------------------------------------------------------------

# 10. Operators

The language supports assignment, arithmetic, and comparison operators.

  Operator   Token             Purpose
  ---------- ----------------- ----------------------------------
  `=`        `ASSIGN`          Assignment
  `+`        `PLUS`            Addition
  `-`        `MINUS`           Subtraction
  `*`        `MULTIPLY`        Multiplication
  `/`        `DIVIDE`          Division
  `>`        `GREATER_THAN`    Greater-than comparison
  `<`        `LESS_THAN`       Less-than comparison
  `==`       `EQUAL`           Equality comparison
  `>=`       `GREATER_EQUAL`   Greater-than-or-equal comparison
  `<=`       `LESS_EQUAL`      Less-than-or-equal comparison

### Longest Match

Flex follows the **longest match rule**.

For example:

``` text
==
```

is recognized as:

``` text
EQUAL
```

rather than two separate `=` tokens.

Similarly:

``` text
>=
<=
```

are recognized as their two-character comparison operators.

If two rules match the same longest length, Flex chooses the rule that
appears first.

------------------------------------------------------------------------

# 11. Special Symbols

  Symbol   Token         Purpose
  -------- ------------- -------------------
  `(`      `LPAREN`      Left parenthesis
  `)`      `RPAREN`      Right parenthesis
  `{`      `LBRACE`      Left brace
  `}`      `RBRACE`      Right brace
  `:`      `COLON`       Colon
  `,`      `COMMA`       Comma
  `;`      `SEMICOLON`   Semicolon

The lexer recognizes these symbols as individual tokens.

Their complete syntactic meaning is determined by the parser.

------------------------------------------------------------------------

# 12. Whitespace

The lexer ignores:

-   Spaces
-   Tabs
-   Newlines
-   Carriage returns

For example:

``` text
let a = 10;
```

and:

``` text
let    a     =     10;
```

produce the same meaningful tokens.

Whitespace itself does not produce a token.

------------------------------------------------------------------------

# 13. Comments

The language supports **single-line comments** using:

``` text
//
```

A comment begins with `//` and continues until the end of the current
line.

Everything after `//` is ignored by the lexer.

Example:

``` text
let a = 10; // assign 10 to a
```

The lexer produces tokens for:

``` text
let a = 10;
```

and ignores:

``` text
// assign 10 to a
```

A complete line can also be a comment:

``` text
// This entire line is a comment
```

No token is generated for the comment.

### Flex Rule

The comment pattern is:

``` text
"//"[^\n]*
```

This matches `//` followed by all characters up to the newline.

### Comment Type Supported

Only **single-line `//` comments** are supported.

Multi-line comments such as:

``` text
/*
   comment
*/
```

are not supported.

------------------------------------------------------------------------

# 14. Lexical Rules

The lexer follows these rules:

1.  Recognize reserved keywords:

    -   `let`
    -   `print`
    -   `if`
    -   `else`

2.  Recognize identifiers containing one or more lowercase English
    letters.

3.  Recognize integer literals.

4.  Recognize floating-point literals.

5.  Recognize strings enclosed in double quotation marks.

6.  Recognize the assignment operator `=`.

7.  Recognize arithmetic operators:

    -   `+`
    -   `-`
    -   `*`
    -   `/`

8.  Recognize comparison operators:

    -   `>`
    -   `<`
    -   `==`
    -   `>=`
    -   `<=`

9.  Recognize parentheses and braces.

10. Recognize:

-   `:`
-   `,`
-   `;`

11. Ignore whitespace.

12. Recognize and ignore single-line `//` comments.

13. Detect uppercase or mixed-case alphabetic words as lexical errors.

14. Detect invalid characters as lexical errors.

15. Detect invalid lexical patterns such as unsupported forms.

16. Continue scanning after a lexical error so additional tokens and
    errors can be reported.

------------------------------------------------------------------------

# 15. Lexical Errors

A lexical error occurs when the lexer encounters a character or sequence
that does not follow the lexical rules.

## 15.1 Invalid Character

Input:

``` text
let @ = 10;
```

`@` is not a valid character in the language.

Output:

``` text
LEXICAL_ERROR    @
```

------------------------------------------------------------------------

## 15.2 Uppercase or Mixed-Case Word

Input:

``` text
let ABC = 10;
```

`ABC` is invalid because identifiers must contain lowercase English
letters.

Output:

``` text
LEXICAL_ERROR    ABC
```

Similarly:

``` text
let Abc = 10;
```

produces a lexical error.

------------------------------------------------------------------------

## 15.3 Invalid Identifier Pattern

The identifier rule is:

``` text
[a-z]+
```

Therefore, identifiers may contain lowercase letters only.

For example:

``` text
abc1
a_b
Abc
```

do not satisfy the identifier pattern.

The exact tokenization of a mixed sequence depends on the lexer rules
and Flex's longest-match behavior.

------------------------------------------------------------------------

## 15.4 Invalid Float

Valid:

``` text
10.5
```

Invalid float forms include:

``` text
10.
.5
```

The current float rule requires digits on both sides of the decimal
point.

------------------------------------------------------------------------

## 15.5 Unterminated String

Example:

``` text
print("Hello);
```

The closing quotation mark is missing.

The input is not a complete string literal and is treated as a lexical
error.

------------------------------------------------------------------------

# 16. Token Output

The lexer prints `TOKEN` before each recognized token.

Example:

``` text
let a = 10;
```

Output:

``` text
TOKEN  LET              let
TOKEN  IDENTIFIER       a
TOKEN  ASSIGN           =
TOKEN  INTEGER          10
TOKEN  SEMICOLON        ;
```

Another example:

``` text
print("Hello");
```

Output:

``` text
TOKEN  PRINT            print
TOKEN  LPAREN           (
TOKEN  STRING           "Hello"
TOKEN  RPAREN           )
TOKEN  SEMICOLON        ;
```

Comments do not produce output because they are ignored.

Example:

``` text
let a = 10; // assign 10 to a
```

produces:

``` text
TOKEN  LET              let
TOKEN  IDENTIFIER       a
TOKEN  ASSIGN           =
TOKEN  INTEGER          10
TOKEN  SEMICOLON        ;
```

------------------------------------------------------------------------

# 17. Lexer vs Parser

The lexer and parser perform different jobs.

## Lexer

The lexer:

-   Reads the source code
-   Identifies lexical patterns
-   Produces tokens
-   Ignores whitespace and comments
-   Reports lexical errors

Example:

``` text
let a = 10;
```

becomes:

``` text
LET
IDENTIFIER
ASSIGN
INTEGER
SEMICOLON
```

## Parser

The parser checks whether the generated tokens follow the grammar of the
language.

For example:

``` text
let = 10;
```

can produce:

``` text
LET
ASSIGN
INTEGER
SEMICOLON
```

The lexer can recognize these individual tokens, but the parser can
determine that an identifier is missing after `let`.

Therefore:

``` text
Lexer  → recognizes tokens
Parser → checks token structure
```

The current project stage focuses on the **lexer**.

------------------------------------------------------------------------

# 18. Complete Example Program

``` text
// Variable declarations
let a = 10;
let b = 2.5;
let message = "Hello";

// Output
print(a);
print(message);

// Conditional statement
if (a > 5) {
    print("Greater");
} else {
    print("Smaller");
}
```

This example demonstrates:

-   Keywords
-   Identifiers
-   Integer literals
-   Floating-point literals
-   String literals
-   Assignment
-   Comparison operators
-   Parentheses
-   Braces
-   Colon
-   Semicolon
-   Whitespace
-   Single-line comments

The lexer ignores the comments and converts the remaining source code
into tokens.

------------------------------------------------------------------------

# 19. Summary of Language Rules

  Category                     Rule
  ---------------------------- -----------------------------------------------
  Keywords                     `let`, `print`, `if`, `else`
  Identifier                   One or more lowercase English letters `a-z`
  Integer                      One or more digits
  Float                        Digits followed by `.` and one or more digits
  String                       Characters enclosed in double quotation marks
  Assignment                   `=`
  Arithmetic                   `+`, `-`, `*`, `/`
  Comparison                   `>`, `<`, `==`, `>=`, `<=`
  Parentheses                  `(` and `)`
  Braces                       `{` and `}`
  Other symbols                `:`, `,`, `;`
  Whitespace                   Ignored
  Comments                     Single-line `//` comments are ignored
  Uppercase/mixed-case words   Lexical error
  Invalid characters           Lexical error
  Invalid float forms          Lexical error / invalid tokenization
  Unterminated string          Lexical error
  Multi-line comments          Not supported

------------------------------------------------------------------------

# 20. Basic Language Grammar

The following is a simplified description of the intended syntax.

``` text
program → statement*

statement → declaration
          | print_statement
          | if_statement

declaration → "let" identifier "=" value ";"

print_statement → "print" "(" value ")" ";"

if_statement → "if" condition ":" "{" statement* "}"

if_statement → "if" condition ":" "{" statement* "}"
               "else" ":" "{" statement* "}"

value → identifier
      | integer
      | float
      | string

condition → value comparison_operator value

comparison_operator → ">"
                    | "<"
                    | "=="
                    | ">="
                    | "<="

identifier → lowercase_letter+

lowercase_letter → a | b | c | ... | z

integer → digit+

float → digit+ "." digit+

string → '"' characters '"'
```

Comments do not appear in the grammar because the lexer removes them
before the parser receives the token stream.

For example:

``` text
let a = 10; // assign 10 to a
```

is effectively passed forward as:

``` text
let a = 10;
```

------------------------------------------------------------------------

# 21. Project Structure

The current lexer project can be organized as:

``` text
CC Project/
│
├── program.txt
├── lex.yy.c
├── lexer.exe
│
├── lexer output/
│   └── lexer.l
│
└── parser output/
    ├── parser.y
    ├── parser.tab.c
    └── parser.tab.h
```

For the **current lexer-only stage**, the important files are:

  File            Purpose
  --------------- -----------------------------------
  `program.txt`   Source program given to the lexer
  `lexer.l`       Flex lexer rules
  `lex.yy.c`      C source generated by Flex
  `lexer.exe`     Compiled lexer executable

The parser files are not required for the current lexer-only
implementation.

------------------------------------------------------------------------

# 22. Running the Lexer

## Step 1: Write the source program

Put the program to be analyzed inside:

``` text
program.txt
```

Example:

``` text
let a = 10; // assign 10 to a
print(a);
```

## Step 2: Generate the C file

From PowerShell:

``` powershell
cd "D:\CC Project"
win_flex -o "lex.yy.c" "lexer output\lexer.l"
```

This generates:

``` text
lex.yy.c
```

## Step 3: Compile

Open the MSYS2 UCRT64 terminal:

``` bash
cd "/d/CC Project"
gcc lex.yy.c -o lexer.exe
```

## Step 4: Run

``` bash
./lexer.exe
```

The recognized tokens will be displayed in the terminal.

------------------------------------------------------------------------

# 23. Example Output

For:

``` text
let a = 10; // assign 10 to a
print(a);
```

the output is:

``` text
TOKEN  LET              let
TOKEN  IDENTIFIER       a
TOKEN  ASSIGN           =
TOKEN  INTEGER          10
TOKEN  SEMICOLON        ;
TOKEN  PRINT            print
TOKEN  LPAREN           (
TOKEN  IDENTIFIER       a
TOKEN  RPAREN           )
TOKEN  SEMICOLON        ;
```

The comment:

``` text
// assign 10 to a
```

does not appear in the output because it is ignored by the lexer.

------------------------------------------------------------------------

# 24. Important Flex Behavior

Flex uses the following matching rule:

> **The longest matching pattern is selected. If multiple rules match
> the same longest text, the rule appearing first is selected.**

For example, when the input contains:

``` text
//
```

the comment rule:

``` text
"//"[^\n]*
```

can match the entire comment, while the division rule:

``` text
"/"
```

matches only one `/`.

Therefore, the longer comment match is selected.

The order of rules matters when two rules match the same amount of text.

For example:

``` lex
"if"      { ... }
[a-z]+    { ... }
```

For the input:

``` text
if
```

both rules match two characters. Therefore, the `if` rule must appear
first so that `if` is recognized as the `IF` keyword rather than as an
identifier.

------------------------------------------------------------------------

# 25. Conclusion

This project implements a simple Flex-based lexical analyzer for a
custom programming language.

The lexer recognizes:

-   Keywords
-   Identifiers
-   Integers
-   Floating-point numbers
-   Strings
-   Operators
-   Special symbols
-   Single-line comments

It ignores whitespace and comments and reports lexical errors for
invalid input.

The lexer is the first stage of the compiler process:

``` text
Source Program
      ↓
    Lexer
      ↓
    Tokens
      ↓
    Parser
      ↓
Syntax Analysis
```

At the current stage, the project focuses on the **lexer and token
generation**.

