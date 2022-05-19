""" 07_store_data_v1: This first version will use a class to store all the
product data. This includes the name, weight, unit, price, and price per unit
which will be calculated. Afterwards it displays the data
Jack Andrews
19/5/22
"""
import curses


class Product:
    def __init__(self, name, weight, unit, price, base_unit):
        self.name = name
        self.weight = weight
        self.unit = unit
        self.price = price
        self.unit_price = conv_to_base(self.unit, self.price, self.weight,
                                       base_unit)


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
    stdscr.move(y_pos, 0)  # Moving cursor to next line automatically to make
    # life easier
    return string


def list_data(stdscr: curses.window, product_list):
    product_list.sort(key=lambda x: len(x['name']), reverse=True)
    # Longest names first, shortest names last
    spaces = ''
    for name in product_list:
        name['name'] += (spaces := '    ' * product_list.index(name))
        # The shorter the name, the more spaces are added to it for formatting
    half_space = '    ' * (len(spaces) // 7)  # Adding spaces in the headings
    # so they are (decently) well formatted
    stdscr.addstr(f"{half_space}Name{half_space}\t|Weight |Unit   |Price"
                  f"  |Unit Price\n")
    product_list.sort(key=lambda y: y['unit_price'])
    # Sorting by cheapest unit price first
    for item in product_list:
        name, weight, unit, price, unit_price = item.values()
        stdscr.addstr(f"{name}\t|{weight}\t|{unit}\t|${price:.2f}\t|"
                      f"${unit_price:.2f}\t\n")
        # Formatting all the headings


def main(stdscr: curses.window):
    product_list = []
    base_unit = get_input(stdscr, "Enter base unit: ")
    sample_data = [["M&Ms", 100, 'g', 1.00], ["Squiggles", 200, 'g', 3.00],
                   ["Cadbury Chocolate", 250, 'g', 3.25],
                   ["Rice Crackers", 100, 'g', 1.50],
                   ["100s and 1000s", 50, 'g', 1.00]]
    # Used for testing
    for item in sample_data:
        test = Product(*item, base_unit)
        # *item splits the list, so it can fill several parameters
        product_list.append(test.__dict__)
        # stdscr.addstr(f"{test.__dict__}\n")
    list_data(stdscr, product_list)

    stdscr.getch()


if __name__ == '__main__':
    curses.wrapper(main)
