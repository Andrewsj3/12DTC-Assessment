"""09_find_best_item: This function takes the product list as a parameter and
sorts by unit price. It iterates through it and finds the cheapest item that
fits in the budget. If no items fit in the budget, it suggests the cheapest
item.
Jack Andrews
27/05/22
"""


import curses


def get_input(stdscr: curses.window, prompt):
    # stdscr is the terminal window on which the program is displayed
    if isinstance(prompt, tuple):
        stdscr.addstr(*prompt)
    else:
        stdscr.addstr(prompt)  # addstr prints output to the window
    string = ""
    curses.echo(True)
    # Prints the user's keystrokes as they type them
    x_pos = stdscr.getyx()[1]

    while True:
        key = stdscr.getkey()
        if (stdscr.getyx()[1] - 1) < x_pos:
            stdscr.move(stdscr.getyx()[0], x_pos)
            # Making sure that the cursor doesn't move too far back
        if key in (curses.KEY_BACKSPACE, '\b', '\x7f'):
            if len(string) > 0:
                string = string[:-1]
                stdscr.delch()  # Deletes the most recent character
            continue
        elif key in ('\r', '\n', '\r\n'):  # User has pressed enter, signalling
            break  # end of input
        else:
            string += key

    curses.echo(False)
    y_pos = stdscr.getyx()[0] + 1
    stdscr.move(y_pos, 0)
    return string


def init_info_and_error_cols():
    # Creates the info and error colours and assigns variables to them
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    C_INFO = curses.color_pair(1)
    C_ERROR = curses.color_pair(2)
    return C_INFO, C_ERROR


def clear_line(stdscr: curses.window, *y_pos, cur_pos=None):
    # *ypos allows us to clear multiple lines in one function call
    # cur_pos allows us to control where the cursor finishes if we want that
    if cur_pos is None:
        cur_pos = stdscr.getyx()
    for pos in y_pos:
        stdscr.move(pos, 0)
        stdscr.clrtoeol()  # Clears a line
    stdscr.move(*cur_pos)  # Unpacking finish coordinates


def get_budget(stdscr: curses.window):
    C_INFO, C_ERROR = init_info_and_error_cols()
    budget = get_input(stdscr, "What is your budget: $")
    try:
        budget = float(budget)

    except ValueError:
        stdscr.addstr("Error: Please enter a valid number", C_ERROR)
        y_pos = stdscr.getyx()[0]
        stdscr.getch()
        clear_line(stdscr, y_pos, y_pos - 1, cur_pos=(y_pos - 1, 0))
        return get_budget(stdscr)
    if budget <= 0:
        stdscr.addstr("Error: Budget must be more than $0", C_ERROR)
        y_pos = stdscr.getyx()[0]
        stdscr.getch()
        clear_line(stdscr, y_pos, y_pos - 1, cur_pos=(y_pos - 1, 0))
        return get_budget(stdscr)
    return budget


def best_item(stdscr: curses.window, product_list):
    C_INFO, _ = init_info_and_error_cols()
    budget = get_budget(stdscr)
    product_list.sort(key=lambda item: item['unit_price'])
    # Cheapest items first
    for thing in product_list:
        if thing.get("price") <= budget:
            stdscr.addstr(f"{thing.get('name')} is the cheapest option")
            stdscr.getch()
            return

    else:
        stdscr.addstr(f"No items fit your budget, but "
                      f"{product_list[0].get('name')} is the cheapest option")
        stdscr.getch()
        # The item at product_list[0] will be the cheapest because it has been
        # sorted that way


if __name__ == '__main__':
    product_list = [
        {'name': 'Sparkling Water', 'weight': 750.0, 'unit': 'ml',
         'price': 1.0,
         'unit_price': 1.33},
        {'name': 'Fanta', 'weight': 1.5, 'unit': 'l', 'price':
            2.25, 'unit_price': 1.5},
        {'name': 'Sprite', 'weight': 1.25, 'unit': 'l', 'price': 2.0,
         'unit_price': 1.6}, {'name': 'Coca-Cola', 'weight': 2.25,
                              'unit': 'l', 'price': 4.0, 'unit_price': 1.78}]
    # Test data copied from previous tests
    curses.wrapper(best_item, product_list)
