"""
RE1016 Assignment 2 by Yeo Shu Yi (REP).

To prevent any accidental edits to the given program,
assignment.py is called instead of editted directly.

Please refer to readme.md for setup and documentation.
"""


import re
import os
import sys
import builtins
import curses

#I am treating assignment.py as a module through import
#However assignment.py has a main() function without __name__ guard
#Thus I am spoofing a exit (5) input and suppressing assignment.py stdout
saved_stdin = builtins.input
builtins.input = lambda _: "5"
with open(os.devnull, 'w') as f:
    save_stdout = sys.stdout
    sys.stdout = f
    try:
        import assignment #This is assignment.py
    finally:
        sys.stdout = save_stdout
        if __debug__: print("[DEBUG] assignment.py main() spoofed.")
builtins.input = saved_stdin


DATABASE_PATH = "./canteens.xlsx"


class CanteenQuery:
    """This class handles the db query logic"""

    def __init__(self, path):
        self.keywords = assignment.load_stall_keywords(path)
        self.prices = assignment.load_stall_prices(path)
        self.canteen_locations = assignment.load_canteen_location(path)

    def search_by_keywords(self, key):
        """Return results by keyword"""

        if not isinstance(key, str): return 400
        parsed_key = self.normalize_query(key)
        # if __debug__: 
        #     print(f"[DEBUG] Query resolved as:\n{parsed_key}")
        results = self.find_keywords(parsed_key)
        
        return results
    
    def normalize_query(self, key):
        """
        Cleans query and resolve logical conflicts (AND OR). Follows rules:
        1.  Any leading/trailing AND, OR, /s is ignored.
        2.  Any non-alphanumeric symbols is ignored.
        3.  In all cases "Foo AND OR AND AND OR... Bar", logic is resolved to a single AND
            as long as a single "AND" is present. 
        4.  If no "AND" present, in the case of "Foo OR OR... Bar", logic is resolved to a single OR.
        5.  In all cases "Foo AND Bar OR Buz AND Qux", AND takes priority as (Foo & Bar) + (Buz & Qux).
        6.  Cases like the restaurant "ANDES" will not be resolved as AND, as only /bAND/b is accepted.

        For more detailed edge-case testing, refer to testbench code regextest.py.
        """

        # REGEX Cleaning
        key = key.upper()
        key = re.sub(r'[^a-zA-Z0-9\s]+', '', key)
        key = re.sub(r'\s+',' ', key)
        key = re.sub(r'\bAND\b', '&', key)
        key = re.sub(r'\bOR\b', '@', key)
        key = re.sub(r'(?<![@&])\s+(?![@&])', '&', key)
        key = re.sub(r'\s+','', key)
        key = re.sub(r'^[@&]+|[@&]+$', '', key)
        key = re.sub(r'[\s@]*&[\s@&]*', '&', key)
        key = re.sub(r'[@]*@[@]*', '@', key)

        or_groups_intermediate = re.split(r'@', key)
        key_groups = []

        for group in or_groups_intermediate:
            and_groups_intermediate = re.split(r'&', group)
            key_groups.append(and_groups_intermediate)

        return key_groups
    
    def find_keywords(self, conditions):
        results = []
        
        for canteen_name, stalls in self.keywords.items():
            for stall_name, keywords_str in stalls.items():
                stall_keywords = {k.strip().upper() for k in keywords_str.split(',')}
                matched_group = None
                for and_group in conditions:
                    if all(req_key in stall_keywords for req_key in and_group):
                        matched_group = and_group
                        break
        
            if matched_group:
                results.append({
                    "canteen": canteen_name,
                    "stall": stall_name,
                    "keywords": stall_keywords,
                    "matched": matched_group
                })

        return results
                        
    def search_by_location(self):
        assignment.get_user_location_interface()


class CurseMenu:
    """CLI Graphical Interface"""

    def __init__(self, db):
        self.db = db

    def __draw_menu(self, select_row, option):
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
        self.stdscr.bkgd(' ', curses.color_pair(2))
        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()
        title = "--- F&B RECOMMENDATION MENU ---"
        self.stdscr.attron(curses.A_BOLD)
        self.stdscr.addstr(1, w//2 - len(title)//2, title)
        self.stdscr.attroff(curses.A_BOLD)
        self.stdscr.border(0)

        for idx, row in enumerate(option):
            x = w//2 - len(row)//2
            y = h//2 - len(option)//2 + idx
            if idx == select_row:
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(y, x, row)
                self.stdscr.attroff(curses.color_pair(1))
            else:
                self.stdscr.addstr(y, x, row)
        self.stdscr.refresh()

    def __get_input(self, prompt, x, y):
        self.stdscr.addstr(x, y, prompt)
        curses.echo()
        user_input = self.stdscr.getstr(x+1, y, 80).decode('utf-8')
        curses.noecho()
        self.user_input = user_input

    def main_menu(self, stdscr):
        self.stdscr = stdscr
        h, w = self.stdscr.getmaxyx()
        if w < 150 or h < 20:
            raise SystemError(
                f"[ERROR] Please expand your CLI to at least 20x150. "
                f"This is to prevent grahical glitches."
            )
        
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
        menu = ['Display Data', 'Keyword Search', 'Price Search', 'Location Search', 'Exit']
        current_row = 0

        while True:
            self.__draw_menu(current_row, menu)
        
            key = self.stdscr.getch()

            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
                current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                match current_row:
                    case 0:
                        self.stdscr.clear()
                        title = "--- DATABASE DICTIONARIES ---"
                        self.stdscr.attron(curses.A_BOLD)
                        self.stdscr.addstr(1, w//2 - len(title)//2, title)
                        self.stdscr.attroff(curses.A_BOLD)
                        self.stdscr.border(0)

                        col1_width = 20
                        col2_width = w - col1_width - 10
                        start_y = 4
                        start_x = 5

                        data = [
                            ("Keywords", str(self.db.keywords)),
                            ("Prices", str(self.db.prices)),
                            ("Locations", str(self.db.canteen_locations))
                        ]
                        for idx, (category, content) in enumerate(data):
                            y = start_y + 2 + (idx * 2)
                            
                            if y >= h - 1:
                                break
                            clean_content = content[:col2_width].replace('\n', ' ')
                            self.stdscr.addstr(y, start_x, category.ljust(col1_width), curses.A_BOLD)
                            self.stdscr.addstr(y, start_x + col1_width, " | ")
                            self.stdscr.addstr(y, start_x + col1_width + 3, clean_content)
                            self.stdscr.addstr(y + 1, start_x, "-" * (col1_width + col2_width + 3), curses.A_DIM)

                        self.stdscr.addstr(h-2, start_x, "Press any key to return...")
                        self.stdscr.refresh()
                        self.stdscr.getch()
                        
                    
                    case 1:
                        self.stdscr.clear()
                        title = "--- KEYWORD SEARCH ---"
                        self.stdscr.attron(curses.A_BOLD)
                        self.stdscr.addstr(1, w//2 - len(title)//2, title)
                        self.stdscr.attroff(curses.A_BOLD)
                        self.stdscr.border(0)
                        
                        col_canteen = 25
                        col_stall = 25
                        self.__get_input("Enter Search Query:", 4, 2)
                        results = self.db.search_by_keywords(self.user_input)

                        self.stdscr.clear()
                        title = "--- SEARCH RESULTS ---"
                        self.stdscr.attron(curses.A_BOLD)
                        self.stdscr.addstr(1, w//2 - len(title)//2, title)
                        self.stdscr.attroff(curses.A_BOLD)
                        self.stdscr.border(0)

                        if not results:
                            self.stdscr.addstr(h//2, w//2 - 10, "No matches found.")
                        else:

                            header_str = f"{'CANTEEN'.ljust(col_canteen)} {'STALL'.ljust(col_stall)} {'  MATCHED'}"
                            self.stdscr.addstr(3, 4, header_str.ljust(w-8)) 
                            
                            for idx, match in enumerate(results):
                                y = 4 + idx
                                if y >= h - 3:
                                    self.stdscr.addstr(y, 4, "... more results hidden ...", curses.A_DIM)
                                    break
                                
                                c_name = match['canteen'][:col_canteen-1].ljust(col_canteen)
                                s_name = match['stall'][:col_stall-1].ljust(col_stall)
                                criteria = str(match['matched'])

                                row_str = f"{c_name} | {s_name} | {criteria}"
                                self.stdscr.addstr(y, 4, row_str)
                        self.stdscr.getch()
                    
                    case 2:
                        self.stdscr.clear()
                        title = "--- PRICE SEARCH ---"
                        self.stdscr.attron(curses.A_BOLD)
                        self.stdscr.addstr(1, w//2 - len(title)//2, title)
                        self.stdscr.attroff(curses.A_BOLD)
                        self.stdscr.border(0)

                        self.stdscr.getch()

                    case 3:
                        self.stdscr.clear()

                        self.db.search_by_location()
                        title = "--- LOCATION SEARCH ---"
                        self.stdscr.attron(curses.A_BOLD)
                        self.stdscr.addstr(1, w//2 - len(title)//2, title)
                        self.stdscr.attroff(curses.A_BOLD)
                        self.stdscr.border(0)

                        self.stdscr.getch()
                    
                    case 4:
                        break

def main():
    """Main function for user interface"""

    #Db and Menu Init
    db = CanteenQuery(path=DATABASE_PATH)
    menu = CurseMenu(db)
    curses.wrapper(menu.main_menu)
            


if __name__ == "__main__":
    if __debug__: print("[DEBUG] Program is in Debug mode. Run python3 -O main.py for Normal Mode.")
    main()