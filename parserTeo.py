from lexer import *
from LL1_table import *
from termcolor import colored
from error_handler import errors, syntax_error, expected_error

f = open('./source_code/C_main.c', 'r')
input_text = add_eof(f.read())

stack = ['eof', 0]
sync = [ 'LPAREN','inicioBloque','finBloque', 'return', 'char', 'int', 'string', 'float', 'void','identificador', 'while', 'if', 'else','finInstruccion','eof']

def buscar_en_tabla(no_terminal, terminal):
    for i in range(len(tabla2)):
        if( tabla2[i][0] == no_terminal and tabla2[i][1] == terminal):
            return tabla2[i][2] #retorno la celda

def agregar_pila(produccion):
    for elemento in reversed(produccion):
        if elemento != 'vacia': #la vacía no la inserta
            stack.append(elemento)

def panic_mode(terminal):
    is_sync_found = False
    is_panic_out = False
    is_matching_sync = False
    while not is_panic_out:
        # print('terminal: ',terminal.type,'\nstack: ',stack)
        if not terminal:
            return terminal
        while is_sync_found:
            if not terminal:
                return terminal
            if terminal.type == 'eof':
                #se encontro eof
                return terminal
            if terminal.type in sync:
                is_sync_found == True
                break
            else:
                terminal = lexer.token()
        if terminal.type in stack:
            # print('aqui')
            while not is_matching_sync:
                if terminal.type == stack[-1]:
                    is_matching_sync = True
                    is_panic_out = True
                    break
                else:
                    stack.pop()
        elif terminal.type == 'finInstruccion':
            while not is_matching_sync:
                if 0 == stack[-1] or 6== stack[-1]:
                    terminal = lexer.token()
                    break
                if 11 == stack[-1]:
                    is_matching_sync = True
                    is_panic_out = True
                    terminal = lexer.token()
                    break
                else:
                    stack.pop()
        else:
            # print("Token is not in current stack, nor end of instruction.",'\n')
            terminal = lexer.token()
            continue

        # a = input('continue')
        if is_matching_sync:
            return terminal

def parser():
     # Abrir el archivo y agregar $ al final del contenido
    lexer.input(input_text)

    # Obtener el primer token
    tok = lexer.token()
    x = stack[-1]  # Primer elemento de derecha a izquierda

    while True:
        # Verificar si se llego al final de la derivación exitosamente
        if x == tok.type and x == 'eof':
            if not errors:
                print(colored("Cadena reconocida exitosamente", 'green', attrs=['bold']))
            return

        # Verificar si se llego al final de un camino de derivación
        if x == tok.type and x != 'eof':  
            if stack:
                stack.pop()
                x = stack[-1]
                tok = lexer.token()

        # Manejar errores de coincidencia de tokens
        elif x in tokens and x != tok.type:
            expected_error(tok, lexer)
            tok = panic_mode(tok)
            x = stack[-1]

        elif x not in tokens:  # No terminal
            celda = buscar_en_tabla(x, tok.type)

            if celda is None:
                # Error de sintaxis, intentar recuperación de error
                print(stack, tok)
                syntax_error(tok)
                tok = panic_mode(tok)
                x = stack[-1]
            else:
                # Continuar el análisis sintáctico sacando de la pila y agregando nuevos símbolos
                stack.pop()
                agregar_pila(celda)
                x = stack[-1]

        # Verificar fin inesperado de archivo
        if not tok:
            print(colored('Warn:', 'yellow', attrs=['bold']), "Unexpected end of file")
            break
        
parser()
create_symbol_table(input_text)