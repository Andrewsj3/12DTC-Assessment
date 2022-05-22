""" 07_store_data_v2: This second version will use a dictionary to store all
the product data. This includes the name, weight, unit, price, and price per
unit which will be calculated. Afterwards it displays the data with the
cheapest item for value first.
Jack Andrews
21/5/22
"""
import curses


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


def main(stdscr: curses.window):
    product_list = []
    base_unit = get_input(stdscr, "Enter base unit: ")
    sample_data = [["M&Ms", 100, 'g', 1.00], ["Squiggles", 200, 'g', 3.00],
                   ["Cadbury Chocolate", 250, 'g', 3.25],
                   ["Rice Crackers", 100, 'g', 1.50],
                   ["100s and 1000s", 50, 'g', 1.00]]
    # Used for testing
    for item in sample_data:
        test = {'name': item[0], 'weight': item[1], 'unit': item[2],
                'price': item[3], 'unit_price':
                    conv_to_base(item[2], item[3], item[1], base_unit)}
        product_list.append(test)
    list_data(stdscr, product_list)

    stdscr.getch()


if __name__ == '__main__':
    curses.wrapper(main)
