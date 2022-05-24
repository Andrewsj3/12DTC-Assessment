"""product_loop_v4 Completed version: Now contains all the code for getting
product info, storing info, displaying info, and lastly the code to ask user if
they want to compare another product
Written by Jack Andrews
23/5/22
"""
import curses
import re


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


def get_product_name(stdscr: curses.window):
    C_INFO, C_ERROR = init_info_and_error_cols()
    product_name = get_input(stdscr, "Enter name of product: ").title()
    if not product_name:  # If no input entered
        stdscr.addstr("Error: Product name cannot be blank", C_ERROR)
        y_pos = stdscr.getyx()[0]
        stdscr.getch()
        clear_line(stdscr, y_pos, y_pos - 1, cur_pos=(y_pos-1, 0))
        return get_product_name(stdscr)
    else:
        for char in product_name:
            if char.isalpha():  # Checking that there is at least one
                # alphabetical character
                return product_name
        else:
            stdscr.addstr("Error: Product name must contain at least "
                          "one alphabetical character", C_ERROR)
            y_pos = stdscr.getyx()[0]
            stdscr.getch()
            clear_line(stdscr, y_pos, y_pos-1, cur_pos=(y_pos-1, 0))
            return get_product_name(stdscr)


def get_price(stdscr: curses.window):
    C_INFO, C_ERROR = init_info_and_error_cols()
    price = get_input(stdscr, "Enter price of product: $")
    try:
        if not price:  # Checks if it's blank
            stdscr.addstr("Error: Price cannot be blank", C_ERROR)
            y_pos = stdscr.getyx()[0]
            stdscr.getch()
            clear_line(stdscr, y_pos, y_pos-1, cur_pos=(y_pos-1, 0))
            return get_price(stdscr)
        price = float(price)
        if price < 0:
            # Negative prices are invalid
            raise ValueError
        else:
            return price
    except ValueError:
        stdscr.addstr("Error: Price is invalid", C_ERROR)
        y_pos = stdscr.getyx()[0]
        stdscr.getch()
        clear_line(stdscr, y_pos, y_pos-1, cur_pos=(y_pos-1, 0))
        return get_price(stdscr)


def parse_volume(stdscr: curses.window, prompt, base_unit):
    C_INFO, C_ERROR = init_info_and_error_cols()
    solid_units = ["mg", 'g', "kg"]
    liquid_units = ["ml", 'l']
    if base_unit in solid_units:
        valid_units = solid_units
    else:
        valid_units = liquid_units
    info = get_input(stdscr, prompt).lower()
    info = info.strip().replace(" ", "")  # Removing all spaces from user input
    num_pattern = re.compile(r"^[0-9]+(\.[0-9]+)?")
    # This pattern matches at least one number, possibly followed by a decimal
    # and at least another number to get the weight component of the product
    idx = 0
    if re.fullmatch(r"^[0-9]+(\.[0-9]+)?[a-z]+$", info):
        # Ensuring user enters valid input
        matches = num_pattern.finditer(info)
        for match in matches:
            idx = match.end()  # Index of last digit in input

        assert idx != 0, "Pattern match failed"
        weight = float(info[:idx])
        if not (weight > 0):
            stdscr.addstr("Error: Product weight must be more than 0", C_ERROR)
            y_pos = stdscr.getyx()[0]
            stdscr.getch()
            clear_line(stdscr, y_pos, y_pos-1, cur_pos=(y_pos-1, 0))
            return parse_volume(stdscr, prompt, base_unit)
        unit = info[idx:]  # Splitting the strings into the two components
        if unit not in valid_units:
            stdscr.addstr("Error: Invalid unit", C_ERROR)
            y_pos = stdscr.getyx()[0]
            stdscr.getch()
            clear_line(stdscr, y_pos, y_pos-1, cur_pos=(y_pos-1, 0))
            return parse_volume(stdscr, prompt, base_unit)
        return weight, unit
    else:
        stdscr.addstr("Error: Input was not in expected format", C_ERROR)
        y_pos = stdscr.getyx()[0]
        stdscr.getch()
        clear_line(stdscr, y_pos, y_pos-1, cur_pos=(y_pos-1, 0))
        # Doing some fancy unpacking to clear multiple lines at once
        return parse_volume(stdscr, prompt, base_unit)


def conv_to_base(unit, price, weight, base_unit):
    solid_units = ["mg", 'g', "kg"]
    liquid_units = ["ml", 'l']
    if base_unit in solid_units:
        diff = solid_units.index(base_unit) - solid_units.index(unit)
    else:
        diff = liquid_units.index(base_unit) - liquid_units.index(unit)
        # This below statement converts the price with respect to weight into
        # the price of one base unit.
        # e.g. product weighing 200 grams costing $2 = $10/kg
    return round(price * ((1000 ** diff) / weight), 2)


def list_data(stdscr: curses.window, product_list):
    product_list.sort(key=lambda x: len(x['name']), reverse=True)
    # Longest names first, shortest names last
    longest_name = len(product_list[0]['name'])
    for name in product_list:
        name['name'] = name['name'].ljust(longest_name)
    stdscr.addstr(f"{'Name'.ljust(longest_name)}\t|Weight |Unit   |Price"
                  f"  |Unit Price\n")
    # Using ljust to make sure that everything is aligned
    # This method is much better and more reliable than the previous one
    product_list.sort(key=lambda y: y['unit_price'])
    # Sorting by cheapest unit price first
    for item in product_list:
        name, weight, unit, price, unit_price = item.values()
        stdscr.addstr(f"{name}\t|{weight}\t|{unit}\t|${price:.2f}\t|"
                      f"${unit_price:.2f}\t\n")
        # Formatting all the headings


def yes_no(stdscr: curses.window, prompt):
    C_INFO, C_ERROR = init_info_and_error_cols()
    response = get_input(stdscr, prompt).lower()
    if response in ("y", "yes"):
        return True
    elif response in ("n", "no"):
        stdscr.clear()
        stdscr.getch()
        stdscr.addstr("Summary:\n\n")
        return False
    elif response == '':
        stdscr.addstr("Error: Response cannot be blank", C_ERROR)
        y_pos = stdscr.getyx()[0]
        stdscr.getch()
        clear_line(stdscr, y_pos, y_pos-1, cur_pos=(y_pos-1, 0))
        return yes_no(stdscr, prompt)
    else:
        stdscr.addstr("Error: Response must be either 'y', 'yes',"
                      " or 'n', 'no'", C_ERROR)
        y_pos = stdscr.getyx()[0]
        stdscr.getch()
        clear_line(stdscr, y_pos, y_pos-1, cur_pos=(y_pos-1, 0))
        return yes_no(stdscr, prompt)


def product_loop(stdscr: curses.window):
    base_unit = get_input(stdscr, "Enter base unit for testing: ").lower()
    # Still need to enter base unit as the loop code has not yet been
    # integrated into main program
    product_list = []
    products_compared = 0
    while True:
        product_name = get_product_name(stdscr)
        p_weight, p_unit = parse_volume(stdscr,
                                        "Enter weight of product"
                                        " in the form '100mg': ", base_unit)
        product_price = get_price(stdscr)
        product_data = {'name': product_name, 'weight': p_weight,
                        'unit': p_unit,
                        'price': product_price,
                        'unit_price': conv_to_base(p_unit, product_price,
                                                   p_weight, base_unit)}
        product_list.append(product_data)
        y_pos = stdscr.getyx()[0]
        clear_line(stdscr, *[i for i in range(y_pos, 0, -1)], cur_pos=(1, 0))
        products_compared += 1
        if products_compared >= 2:  # Doesn't make sense to ask the question
            # if user has only entered info for one product
            if yes_no(stdscr, "Do you want to compare another product: "):
                continue
            else:
                list_data(stdscr, product_list)
                stdscr.getch()
                break


if __name__ == '__main__':
    curses.wrapper(product_loop)
