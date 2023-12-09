from termcolor import colored

errors = []

def lexical_error(t, lexer):
    error_info = {
        'type': "Lexical Error",
        'character': t.value[0],
        'lineno': t.lineno,
        'lexpos': t.lexpos
    }
    errors.append(error_info)

    print(colored('Lexical Error:', 'red', attrs=['bold']), f"Unexpected character '{error_info['character']}' at line {error_info['lineno']}")

    lexer.skip(1)

def syntax_error(t):
    error_info = {
            'type': "Syntax Error",
            'character': t.value,
            'lineno': t.lineno,
            'lexpos': t.lexpos
        }
    errors.append(error_info)
    
    print(colored('Syntax Error:', 'red', attrs=['bold']),f"Unexpected character '{error_info['character']}' at line {error_info['lineno']}")


def expected_error(t, lexer):
    error_info = {
            'type': "Expected Character",
            'character': t.value,
            'lineno': t.lineno,
            'lexpos': t.lexpos
        }
    errors.append(error_info)
    
    print(colored('Syntax Error:', 'red', attrs=['bold']), f"Expected character '{error_info['character']}' at line {error_info['lineno']}")

    lexer.skip(1)