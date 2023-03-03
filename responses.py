import random

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "<:dango:1080672889428246539>": 1,
    "<:cake:1080672806783688826>": 1,
    "<:macaron:1080672858948251768>": 1,
    "<:pancakes:1080672833606266981>": 1
}

symbol_value = {
    "<:dango:1080672889428246539>": 1,
    "<:cake:1080672806783688826>": 1,
    "<:macaron:1080672858948251768>": 1,
    "<:pancakes:1080672833606266981>": 1
}

dict = {}


def get_response(username: str, message: str) -> str:
    p_message = message.lower()

    if username not in dict.keys():
        dict[username] = {"step_deposit": False, "balance": 0}

    if p_message == "!deposit":
        dict[username]["step_deposit"] = True
        return "How much would you like to deposit?"

    if dict[username]["step_deposit"] == True and p_message.isdigit():
        amount = int(p_message)
        if amount > 0:
            dict[username]["balance"] += amount
            dict[username]["step_deposit"] = False
            return "Your current balance is $" + str(dict[username]["balance"])
        else:
            return "Please enter a valid number."

    if p_message == "!balance":
        return "Your current balance is $" + str(dict[username]["balance"])

    if p_message.startswith("!play"):
        bet = p_message.split()[1]
        if bet.isdigit():
            bet = int(bet)
        else:
            return "You entered an invalid number."
        if bet > dict[username]["balance"]:
            return "Your balance is insufficient."
        else:
            return get_slot_machine_spin(username, ROWS, COLS, bet, symbol_count)


def check_winnings(columns, row, bet, values):
    winnings = 0
    for line in range(row):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet

    return winnings


def get_slot_machine_spin(username, rows, cols, bet, symbols):
    all_symbols = []
    slot = ""
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            s = random.choice(current_symbols)
            current_symbols.remove(s)
            column.append(s)

        columns.append(column)

    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                slot += column[row] + " "
            else:
                slot += column[row] + "\n"

    winnings = check_winnings(columns, ROWS, bet, symbol_value)
    if winnings == 0:
        slot += "You did not win."
    else:
        slot += f"You won ${winnings}."
    total_winnings = winnings - bet
    dict[username]["balance"] += total_winnings
    slot += "\nYour current balance is now $" + str(dict[username]["balance"]) + "."
    return slot





















