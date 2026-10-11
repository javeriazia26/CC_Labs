
KEYWORDS = {
    "let": "LET",
    "print": "PRINT",
    "if": "IF",
    "else": "ELSE"
}

OPERATORS = {
    "=": "ASSIGN",
    "+": "PLUS",
    "-": "MINUS",
    "*": "MULTIPLY",
    "/": "DIVIDE",
    ">": "GREATER_THAN",
    "<": "LESS_THAN"
}

SYMBOLS = {
    "(": "LPAREN",
    ")": "RPAREN",
    "{": "LBRACE",
    "}": "RBRACE",
    ":": "COLON",
    ",": "COMMA",
    ";": "SEMICOLON"
}


def lexer(source_code):
    tokens = []
    i = 0
    length = len(source_code)

    while i < length:

        # Ignore whitespace
        if source_code[i].isspace():
            i += 1
            continue

        # Ignore // comments
        if source_code.startswith("//", i):
            while i < length and source_code[i] != "\n":
                i += 1
            continue

        # Two-character operators
        if i + 1 < length:
            two_chars = source_code[i:i + 2]

            if two_chars == "==":
                tokens.append(("EQUAL", two_chars))
                i += 2
                continue

            if two_chars == ">=":
                tokens.append(("GREATER_EQUAL", two_chars))
                i += 2
                continue

            if two_chars == "<=":
                tokens.append(("LESS_EQUAL", two_chars))
                i += 2
                continue

        # Numbers
        if source_code[i].isdigit() and source_code[i].isascii():
            start = i

            while (
                i < length
                and source_code[i].isascii()
                and source_code[i].isdigit()
            ):
                i += 1

            if (
                i + 1 < length
                and source_code[i] == "."
                and source_code[i + 1].isascii()
                and source_code[i + 1].isdigit()
            ):
                i += 1

                while (
                    i < length
                    and source_code[i].isascii()
                    and source_code[i].isdigit()
                ):
                    i += 1

                tokens.append(("FLOAT", source_code[start:i]))
            else:
                tokens.append(("INTEGER", source_code[start:i]))

            continue

        # Strings
        if source_code[i] == '"':
            start = i
            i += 1

            while i < length and source_code[i] != '"' and source_code[i] != "\n":
                i += 1

            if i < length and source_code[i] == '"':
                i += 1
                tokens.append(("STRING", source_code[start:i]))
            else:
                tokens.append(("LEXICAL_ERROR", source_code[start:i]))
            continue


        # Keywords and identifiers
        if source_code[i].isascii() and source_code[i].isalpha():
            start = i

            while (
                i < length
                and source_code[i].isascii()
                and source_code[i].isalpha()
            ):
                i += 1

            word = source_code[start:i]

            if word in KEYWORDS:
                tokens.append((KEYWORDS[word], word))
            elif word.islower():
                tokens.append(("IDENTIFIER", word))
            else:
                tokens.append(("LEXICAL_ERROR", word))

            continue

        # One-character operators
        if source_code[i] in OPERATORS:
            tokens.append((OPERATORS[source_code[i]], source_code[i]))
            i += 1
            continue

        # Symbols
        if source_code[i] in SYMBOLS:
            tokens.append((SYMBOLS[source_code[i]], source_code[i]))
            i += 1
            continue

        # Unknown characters
        tokens.append(("LEXICAL_ERROR", source_code[i]))
        i += 1

    return tokens


# MAIN PROGRAM

print("Enter your program.")
print("Type END on a new line when finished.\n")

lines = []

while True:
    line = input()

    if line == "END":
        break

    lines.append(line)

source_code = "\n".join(lines)
tokens = lexer(source_code)

print("\nTokens:\n")

for token_type, value in tokens:
    print(f"{token_type:<20} {value}")
