from ArtGallery import *
import random
import os

# Zda-li nejsou nainstalované uvedené knihovny, nastane automaticky jejich instalace.
try:
    import inquirer
    from colorama import Fore
except ImportError:
    os.system('pip install inquirer')
    os.system('pip install colorama')
    import inquirer
    from colorama import Fore

# Globální proměnné
Player = Fore.RED + 'X' + Fore.RESET
Computer = Fore.BLUE + 'O' + Fore.RESET

chance = 70    # 1-100% na zablokování

os.system('cls')

# special symbols:
# ┌ ┐ └ ┘ ─ │ ├ ┤ ┼ ┬ ┴

# Skvěle propracované informace
def Informace():
    os.system('cls')
    informace()
    print('''Od vysvětlování informaci vážně nejsem, jinak by to byla docela slohovka.
Pro dobro nás všech, tady máte to info : https://en.wikipedia.org/wiki/Tic-tac-toe''')
    holder = input(Fore.BLUE + 'Zmáčkni Enter pro pokračování.' + Fore.RESET)

# Input hráče místa pro jeho symbol
def Player_move(board):
    row_mapping = {
        'Řádek 1.': 0,
        'Řádek 2.': 1,
        'Řádek 3.': 2
    }
    column_mapping = {
        'Sloupec 1.': 0,
        'Sloupec 2.': 1,
        'Sloupec 3.': 2
    }

    question = [inquirer.List('player_x', message=Fore.LIGHTRED_EX + 'Vyber z možností řádek' + Fore.RESET, choices=['Řádek 1.', 'Řádek 2.', 'Řádek 3.'])]
    x_response = inquirer.prompt(question)
    question = [inquirer.List('player_y', message=Fore.LIGHTRED_EX + 'Vyber z možností sloupec' + Fore.RESET, choices=['Sloupec 1.', 'Sloupec 2.', 'Sloupec 3.'])]
    y_response = inquirer.prompt(question)

    x = row_mapping[x_response['player_x']]
    y = column_mapping[y_response['player_y']]

    if board[x][y] == ' ':
        board[x][y] = Player
    else:
        print(Fore.RED + "\nNeplatný údaj\n" + Fore.RESET)
        Player_move(board)

# Vygenerování náhodného políčka počítače
def Computer_move(board, Free_block, Free_spaces):
    number = 0
    if Free_block != None:
        number = random.randint(1, 100)
        if number <= chance:    # Je 70% šance, že počítač zablokuje hráči možnost vítězství
            x = Free_block[0]   # Předání x lokace volného bloku
            y = Free_block[1]   # Předání y lokace volného bloku
            # print('Blocked')
        # else:
            # print('You have got lucky')

    if not number <= chance or Free_block == None:
        x = random.randint(0, 2)
        y = random.randint(0, 2)
        # print('Not Blocked')
        
    if board[x][y] == ' ':
        board[x][y] = Computer
    elif Check_free_spaces(board) > 0:
        Computer_move(board, Free_block, Free_spaces)
    else:
        Check_winner(board)

# Resetování hrací desky
def Reset_board():
    board = [[' ', ' ', ' '],
             [' ', ' ', ' '],
             [' ', ' ', ' ']]
    return board

# Napsání hrací desky
def Print_board(board):
    print("┌───┬───┬───┐")
    for row in range(3):
        for column in range(3):
            print(f"│ {board[row][column]}", end=" ")
        print("│")
        print("├───┼───┼───┤") if row != 2 else print("└───┴───┴───┘")

# Napsání vítěze
def Print_winner(winner, Free_spaces, board):
    os.system('cls')
    Print_board(board)

    if winner == Player:
        výhra()
        print(Fore.LIGHTRED_EX + "Vyhrál Hráč, gratuluji!")
    elif winner == Computer:
        prohra()
        print(Fore.LIGHTRED_EX + "Vyhrál Počítač")
    elif Free_spaces == 0:
        remíza()
        print(Fore.LIGHTRED_EX + "Je to Remíza")
    
    Fore.RESET

# Kontrola počtu zbylých volných míst
def Check_free_spaces(board):
    Free_spaces = 0
    for row in range(3):
        for column in range(3):
            if board[row][column] == " ":
                Free_spaces += 1

    return Free_spaces

# Kontrola vítěze
def Check_winner(board):
    # check rows
    for row in range(3):
        if board[row][0] == board[row][1] and board[row][0] == board[row][2]:
            return board[row][0]
        
    # check columns
    for column in range(3):
        if board[0][column] == board[1][column] and board[0][column] == board[2][column]:
            return board[0][column]

    # check diagonals 
    if board[0][0] == board[1][1] and board[0][0] == board [2][2]:
        return board[0][0]
    
    if board[0][2] == board[1][1] and board[0][2] == board [2][0]:
        return board[0][2]
    
# Kontrola možného zablokování hráče k výhře
def Check_possible_blockage(board):
    conformity = 0  # Shoda znaků

    # print('HORIZONTÁLNÍ')

    # Horizontální kontrola
    for row in range(3):
        for column in range(3):
            # Kontrola blocku tabule
            if board[row][column] == Player:
                conformity += 1
        # Pokud byly zjištěny dvě shody, zkontroluje se, jestli je jiné políčko volné
        if conformity == 2:
            for column in range(3):
                # Pokud je nalezeno volné políčko, vrátíme jeho hodnotu
                if board[row][column] == ' ':
                    # print(f'{row}. Conformity = {conformity}')
                    conformity = 0
                    return row, column
                    
        # print(f'{row}. Conformity = {conformity}')
        conformity = 0
    
    # print('\nVERTIKÁLNÍ')

    # Vertikální kontrola
    for column in range(3):
        for row in range(3):
            # Kontrola blocku tabule
            if board[row][column] == Player:
                conformity += 1
        # Pokud byly zjištěny dvě shody, zkontroluje se, jestli je jiné políčko volné
        if conformity == 2:
            for row in range(3):
                # Pokud je nalezeno volné políčko, vrátíme jeho hodnotu
                if board[row][column] == ' ':
                    # print(f'{column}. Conformity = {conformity}')
                    conformity = 0
                    return row, column
                    
        # print(f'{column}. Conformity = {conformity}')
        conformity = 0

    # print('\nDIAGONÁLNÍ - ZLEVA DO PRAVA DOLŮ')

    # Diagonální kontrola - Zleva do prava dolů
    for block in range(3):
        if board[block][block] == Player:
            conformity += 1

    # print(f'{block}. Conformity = {conformity}')

    if conformity == 2:
        for block in range(3):
            # Pokud je nalezeno volné políčko, vrátíme jeho hodnotu
            if board[block][block] == ' ':
                conformity = 0
                return block, block
            
    conformity = 0
            
    # print('\nDIAGONÁLNÍ - ZPRAVA DO LEVA DOLŮ')
            
    # Diagonální kontrola - Zprava do leva dolů
    row, column = 0, 2
    for block in range(3):
        if board[row][column] == Player:
            conformity += 1
        row += 1
        column -= 1

    # print(f'{block}. Conformity = {conformity}')

    if conformity == 2:
        row, column = 0, 2
        for block in range(3):
            if board[row][column] == ' ':
                conformity = 0
                return row, column
            row += 1
            column -= 1

    conformity = 0

# Nastavení hry pro hráče
def Settings():
    global chance
    global Player
    global Computer

    while True:
        os.system('cls')
        nastavení()
        
        question = [inquirer.List('settings_choices', message='Výběr nastavení', choices=['Šance zablokování hráče', 'Symboly', 'Exit'])]
        answer = inquirer.prompt(question)

        match answer['settings_choices']:

            # Šance zablokování hráče
            case 'Šance zablokování hráče':
                os.system('cls')
                nastavení()
                print('Šance zablokování hráče\n')
                while True:
                    print(f'Aktuální hodnota = {chance}%')
                    chance = int(input(Fore.BLUE + 'Zadej novou hodnotu >>> ' + Fore.RESET))
                    if chance > 100 or chance < 0: print(Fore.RED + 'Hodnota musí být pouze od 0 do 100 %' + Fore.RESET)
                    else: break

            # Libovolné nastavení symbolů pro hráče
            case 'Symboly':
                while True:
                    os.system('cls')
                    nastavení()
                    print(f'Aktuální symboly:\nHráč = {Player}\nPočítač = {Computer}\n')
                    question = [inquirer.List('Symbols', message='Vyber z možností', choices=['Symbol Hráče', 'Symbol Počítače', 'Exit'])]
                    answer = inquirer.prompt(question)

                    match answer['Symbols']:
                        case 'Symbol Hráče':
                            while True:
                                Pl_symbol = input('Zadej nový symbol pro hráče >>> ')
                                if len(Pl_symbol) != 1: print(Fore.RED + 'Musí se jednat o symbol s jedním charakterem' + Fore.RESET)
                                else: break

                            Player = Fore.RED + Pl_symbol + Fore.RESET

                        case 'Symbol Počítače':
                            while True:
                                Co_symbol = input('Zadej nový symbol pro počítač >>> ')
                                if len(Pl_symbol) != 1: print(Fore.RED + 'Musí se jednat o symbol s jedním charakterem' + Fore.RESET)
                                else: break
                
                            Computer = Fore.BLUE + Co_symbol + Fore.RESET

                        case 'Exit': break

            case 'Exit': break

def Main():
    board = [[' ', ' ', ' '],
             [' ', ' ', ' '],
             [' ', ' ', ' ']]
    winner = ' '
    running = True

    Reset_board()
    os.system('cls')

    while running:
        os.system('cls')
        menu()

        print(f'Hráč = {Player}\nPočítač = {Computer}')

        Print_board(board)
        Free_spaces = Check_free_spaces(board)

        Check_winner(board)
        winner = Check_winner(board)
        if winner != ' ' and winner != None or Free_spaces == 0:
            break

        Player_move(board)
        Check_winner(board)
        if winner != ' ' and winner != None or Free_spaces == 0:
            break
        
        Free_block = Check_possible_blockage(board)
            # print(f'\nFree block = {Free_block}')

        Computer_move(board, Free_block, Free_spaces)
        Check_winner(board)
        if winner != ' ' and winner != None or Free_spaces == 0:
            break

    Print_board(board)
    Print_winner(winner, Free_spaces, board)

    question = [inquirer.List('end', message='Cheš pokračovat?', choices=['Ano', 'Ne'])]
    answer = inquirer.prompt(question)

    match answer['end']:
        case 'Ano':
            Main()
        case 'Ne':
            not running

if __name__ == "__main__":
    # Aktuální verze
    version = '1.3'

    while True:
        menu()
        print(f'Verze {Fore.BLUE + version + Fore.RESET}\n')
        question = [inquirer.List('start', message='Menu', choices=['Start', 'Informace', 'Nastavení'])]
        answer = inquirer.prompt(question)

        match answer['start']:
            case 'Start':
                break
            case 'Informace':
                Informace()
            case 'Nastavení':
                Settings()
        os.system('cls')
    Main()