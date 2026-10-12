KEYWORDS = {
    "let": "LET",
    "print": "PRINT",
    "if": "IF",
    "else": "ELSE"
}

OPERATORS = {
    "==": "EQUAL",
    ">=": "GREATER_EQUAL",
    "<=": "LESS_EQUAL",
    "=": "ASSIGN",
    ">": "GREATER_THAN",
    "<": "LESS_THAN",
    "+": "PLUS",
    "-": "MINUS",
    "*": "MULTIPLY",
    "/": "DIVIDE"
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

        # Ignore comments
        if source_code.startswith("//", i):
            while i < length and source_code[i] != "\n":
                i += 1
            continue

        # Strings
        if source_code[i] == '"':
            start = i
            i += 1

            while (
                i < length
                and source_code[i] != '"'
                and source_code[i] != "\n"
            ):
                i += 1

            if i < length and source_code[i] == '"':
                i += 1
                tokens.append(("STRING", source_code[start:i]))
            else:
                tokens.append(("LEXICAL_ERROR", source_code[start:i]))

            continue

        # Numbers
        if source_code[i] in "0123456789":
            start = i

            while i < length and source_code[i] in "0123456789":
                i += 1

            # Recognize a float only if digits follow the decimal point
            if (
                i + 1 < length
                and source_code[i] == "."
                and source_code[i + 1] in "0123456789"
            ):
                i += 1

                while i < length and source_code[i] in "0123456789":
                    i += 1

                tokens.append(("FLOAT", source_code[start:i]))
            else:
                tokens.append(("INTEGER", source_code[start:i]))

            continue

        # Alphabetic words: keywords, identifiers, or lexical errors
        # Uppercase letters: lexical errors
        if "A" <= source_code[i] <= "Z":
            start = i

            while i < length and "A" <= source_code[i] <= "Z":
                i += 1

            tokens.append(("LEXICAL_ERROR", source_code[start:i]))
            continue

        # Lowercase words: keywords or identifiers
        if "a" <= source_code[i] <= "z":
            start = i

            while i < length and "a" <= source_code[i] <= "z":
                i += 1

            word = source_code[start:i]

            if word in KEYWORDS:
                tokens.append((KEYWORDS[word], word))
            else:
                tokens.append(("IDENTIFIER", word))

            continue

        # Operators: check two-character operators first        
        matched = False

        for operator in ("==", ">=", "<="):
            if source_code.startswith(operator, i):
                tokens.append((OPERATORS[operator], operator))
                i += len(operator)
                matched = True
                break

        if matched:
            continue

        # One-character operators
        if source_code[i] in OPERATORS:
            operator = source_code[i]
            tokens.append((OPERATORS[operator], operator))
            i += 1
            continue

        # Symbols
        if source_code[i] in SYMBOLS:
            symbol = source_code[i]
            tokens.append((SYMBOLS[symbol], symbol))
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
    try:
        line = input()
    except EOFError:
        break

    if line == "END":
        break

    lines.append(line)

source_code = "\n".join(lines)
tokens = lexer(source_code)

print("\nTokens:\n")

for token_type, value in tokens:
    print(f"{token_type:<20} {value}")
