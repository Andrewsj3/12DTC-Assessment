"""get_weight_v2: This function asks user for a unit and a weight and checks
that they are valid. Now checks units to see if they can be compared with each
other.
Written by Jack Andrews
10/5/22
"""

import curses
import re  # This will be used to parse the weight and the unit of the product


def get_input(stdscr: curses.window, prompt):
    # stdscr is the terminal window on which the program is displayed
    if isinstance(prompt, tuple):
        stdscr.addstr(*prompt)
    else:
        stdscr.addstr(prompt)  # addstr prints output to the window
    string = ""
    curses.echo(True)  # Prints the user's keystrokes as they type them
    while True:
        key = stdscr.getkey()
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
    return string


def init_info_and_error_cols():
    # Creates the info and error colours and assigns variables to them
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    C_INFO = curses.color_pair(1)
    C_ERROR = curses.color_pair(2)
    return C_INFO, C_ERROR


def clear_line(stdscr: curses.window, *y_pos, cur_pos=0):
    # *ypos allows us to clear multiple lines in one function call
    # cur_pos allows us to control where the cursor finishes if we want that
    if cur_pos == 0:
        cur_pos = stdscr.getyx()
    for pos in y_pos:
        stdscr.move(pos, 0)
        stdscr.clrtoeol()  # Clears a line
    stdscr.move(*cur_pos)  # Unpacking finish coordinates


def parse_volume(stdscr: curses.window, prompt):
    C_INFO, C_ERROR = init_info_and_error_cols()
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
        unit = info[idx:]  # Splitting the strings into the two components
        return weight, unit
    else:
        y = stdscr.getyx()[0]
        stdscr.addstr(2, 0, "Error: Input was not in expected format", C_ERROR)
        stdscr.getch()
        clear_line(stdscr, *[i for i in range(y+1, 0, -1)])
        # Doing some fancy unpacking to clear multiple lines at once
        return parse_volume(stdscr, prompt)


def main(stdscr: curses.window):
    solid_measures = ['mg', 'g', 'kg']
    liquid_measures = ['ml', 'l']
    C_INFO, C_ERROR = init_info_and_error_cols()
    base_unit = get_input(stdscr, "Enter base unit for testing: ")
    if base_unit in solid_measures:
        valid_units = solid_measures.copy()
    else:
        valid_units = liquid_measures.copy()
    # No validation for base unit as this will be handled by get_unit
    while True:
        weight, unit = parse_volume(stdscr, (1, 0, "Enter weight of product"
                                                   " in the form '100mg': "))
        y = stdscr.getyx()[0]
        if unit in valid_units:
            stdscr.addstr(y+1, 0, f"Product weight: {weight}\n", C_INFO)
            stdscr.addstr(f"Product unit: {unit}", C_INFO)
            # Testing to make sure the data was parsed correctly
            stdscr.getch()
            break
        else:
            stdscr.addstr(y+1, 0, f"Error: {unit} cannot be converted into"
                                  f" {base_unit}", C_ERROR)
            stdscr.getch()
            clear_line(stdscr, y+1, y)


if __name__ == '__main__':
    curses.wrapper(main)
