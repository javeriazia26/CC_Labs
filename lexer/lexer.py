# lexer.py

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

    while i < len(source_code):

        # Ignore spaces, tabs and new lines
        if source_code[i].isspace():
            i += 1
            continue

        # -------------------------
        # Keywords / Identifiers
        # -------------------------
        if source_code[i].isalpha():

            word = ""

            while i < len(source_code) and source_code[i].isalpha():
                word += source_code[i]
                i += 1

            # Keyword
            if word in KEYWORDS:
                tokens.append((KEYWORDS[word], word))

            # One lowercase letter = valid identifier
            elif word.islower():
                tokens.append(("IDENTIFIER", word))

            # Anything else is invalid
            else:
                tokens.append(("LEXICAL_ERROR", word))

            continue

        # -------------------------
        # Numbers
        # -------------------------
        if source_code[i].isdigit():

            number = ""

            while i < len(source_code) and source_code[i].isdigit():
                number += source_code[i]
                i += 1

            # Float
            if i < len(source_code) and source_code[i] == ".":

                number += "."
                i += 1

                # Decimal part must contain a digit
                if i >= len(source_code) or not source_code[i].isdigit():
                    tokens.append(("LEXICAL_ERROR", number))
                    continue

                while i < len(source_code) and source_code[i].isdigit():
                    number += source_code[i]
                    i += 1

                tokens.append(("FLOAT", number))

            # Integer
            else:
                tokens.append(("INTEGER", number))

            continue

        # -------------------------
        # Strings
        # -------------------------
        if source_code[i] == '"':

            i += 1
            string_value = ""

            while i < len(source_code) and source_code[i] != '"':
                string_value += source_code[i]
                i += 1

            # Missing closing quote
            if i >= len(source_code):
                tokens.append(("LEXICAL_ERROR", "Unterminated string"))

            else:
                i += 1
                tokens.append(("STRING", string_value))

            continue

        # -------------------------
        # Two-character operators
        # -------------------------
        if i + 1 < len(source_code):

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

        # -------------------------
        # One-character operators
        # -------------------------
        if source_code[i] in OPERATORS:

            tokens.append((
                OPERATORS[source_code[i]],
                source_code[i]
            ))

            i += 1
            continue

        # -------------------------
        # Symbols
        # -------------------------
        if source_code[i] in SYMBOLS:

            tokens.append((
                SYMBOLS[source_code[i]],
                source_code[i]
            ))

            i += 1
            continue

        # -------------------------
        # Unknown character
        # -------------------------
        tokens.append((
            "LEXICAL_ERROR",
            source_code[i]
        ))

        i += 1

    return tokens


# ==================================
# MAIN PROGRAM
# ==================================

print("Enter your program.")
print("Type END on a new line when finished.\n")

lines = []

while True:

    line = input()

    if line == "END":
        break

    lines.append(line)


source_code = "\n".join(lines)

# Run lexer
tokens = lexer(source_code)


# Display result
print("\nTokens:\n")

for token_type, value in tokens:
    print(f"{token_type:<20} {value}")