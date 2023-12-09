# ------------------------------------------------------------
# Lexer para C
# ------------------------------------------------------------
import ply.lex as lex
from error_handler import lexical_error
from prettytable import PrettyTable

# List of token names.   This is always required
tokens = (
   'identificador',
   'LPAREN', # (
   'RPAREN', # )
   'coma', # ,
   'char', 
   'int',
   'string',
   'float',
   'void',
   'finInstruccion', # ;
   'return',
   'equals', # =
   'PLUS', # +
   'MINUS', # -
   'TIMES', # *
   'DIVIDE', # /
   'NUMBER', 
   'word',
   'letter',
   'equalscomparision', # ==
   'menorque', # <
   'mayorque', # >
   'if',
   'inicioBloque', # {
   'finBloque', # }
   'else',
   'while',
   'not',
   'and',
   'OR',
   'comentario', # //
   'comentario_bloque', # /* **/
   'eof' # $
)

# Regular expression rules for simple tokens
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_coma = r'\,'
t_finInstruccion = r'\;'
t_equalscomparision = r'=='
t_equals = r'\='
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/' 
t_menorque  = r'<'
t_mayorque  = r'>'
t_inicioBloque = r'\{'
t_finBloque = r'\}'
t_and = r'\&&'
t_OR = r'\|\|'
t_not = r'\!'
t_eof= r'\$'

#t_vacia= r'\'  

# A regular expression rule with some action code


def t_char(t):
    r'(char)'
    return t

def t_int(t):
    r'(int)'
    return t

def t_string(t):
    r'(string)'
    return t

def t_float(t):
    r'(float)'
    return t

def t_void(t):
    r'(void)'
    return t

def t_return(t):
    r'(return)'
    return t
    
def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_word(t):
    r'\".*\"'
    return t

def t_letter(t):
    r"'.*'"
    return t

def t_if(t):
    r'(if)'
    return t

def t_else(t):
    r'(else)'
    return t

def t_while(t):
    r'(while)'
    return t
    
def t_identificador(t):
    r'([a-z]|[A-Z]|_)([a-z]|[A-Z]|\d|_)*'
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

def t_keyword(t):
    r'(char)|(int)|(float)|(string)|(return)|(if)|(else)|(while)|(void)'
    return t

def t_comentario(t):
    r'\/\/.*'
    pass  # Ignorar comentarios de una línea

def t_comentario_bloque(t):
    r'\/\*(.|\n)*\*\/'
    pass  # Ignorar comentarios de bloque

# Error handling rule
def t_error(t):
    lexical_error(t, lexer)

def add_eof(data):
    data_list = list(data)
    data_list.append("$")
    return ''.join(data_list)


# Build the lexer
lexer = lex.lex()

symbol_table = []

# Tokenize y crea la tabla de símbolos
def create_symbol_table(input):
    lexer.input(input)
    while True:
        tok = lexer.token()
        symbol_entry = {}
        if not tok:
            break  # No hay más entrada
        
        if tok.type in ('char', 'int', 'float', 'string', 'void'):
            type = tok.type
            tok = lexer.token()

            # Manejar declaraciones de variables múltiples
            if tok.type == 'identificador':
                while True:
                    name = tok.value
                    symbol_entry = {
                        'name': name,
                        'type': type,
                        'value': None,
                        'line': tok.lineno# Inicializar el valor como None
                    }

                    # Verificar si hay una asignación de valor
                    tok = lexer.token()
                    if tok.type == 'equals':
                        tok = lexer.token()
                        symbol_entry['value'] = tok.value

                    symbol_table.append(symbol_entry)

                    # Verificar si hay más identificadores o coma
                    if tok.type == 'coma':
                        tok = lexer.token()
                    elif tok.type == 'identificador':
                        continue
                    else:
                        break

            else:
                name = tok.value
                tok = lexer.token()
                if tok.type == 'equals':
                    tok = lexer.token()
                    value = tok.value
                    
                    symbol_entry = {
                        'name': name,
                        'type': type,
                        'value': value,
                        'line': tok.lineno
                    }
                    
                    symbol_table.append(symbol_entry)
                else:
                    break
    
    
    print('\n','Tabla de símbolos:')
    table = PrettyTable(['Name', 'Type', 'Value', 'Line'])

    for row in symbol_table:
        table.add_row([row['name'], row['type'], row['value'], row['line']])

    print(table)


# Agregar a la tabla de símbolos
def add_to_symbol_table(name, type, value, line):
    symbol_entry = {
        'name': name,
        'type': type,
        'value': value,
        'line': line
    }
    symbol_table.append(symbol_entry)

# Buscar en la tabla de símbolos
def search_symbol_table(name):
    for symbol in symbol_table:
        if symbol['name'] == name:
            return symbol
    return None

# Actualizar la tabla de símbolos
def update_symbol_table(name, value):
    for symbol in symbol_table:
        if symbol['name'] == name:
            symbol['value'] = value
            return
    return None

# Eliminar de la tabla de símbolos
def delete_from_symbol_table(name):
    for symbol in symbol_table:
        if symbol['name'] == name:
            symbol_table.remove(symbol)
            return
    return None
