"""
RE1016 Assignment 2 by Yeo Shu Yi (REP).

To prevent any accidental edits to the given program,
assignment.py is called instead of editted directly.

Please refer to readme.md for setup and documentation.
Follow additional setup steps if running on Windows.
"""


import re
import os
import sys
import builtins
import curses
import time
import math
import pygame
import textwrap
import pandas as pd
from PIL import Image


#Using os to find path for cross compatability between Windows / UNIX
if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATABASE_PATH = os.path.join(BASE_DIR, "src", "canteens.xlsx")


def import_assignmentpy():
    """
    The entire chunk below this is used to deal with issues importing assignment.py.
    Monkey patching and std redirects is used because assignment.py was not designed to be modular.

    Problem 1.  main() is being called without __name__ guard in assignment.py
                This results in assignment.py's CLI interface being called

    Solution 1. stdout is redirected before assignment.py is imported
                A "5" is inserted to stdin to exit assignment.py's main()

    Problem 2.  canteen_stall_keywords = load_stall_keywords("canteens.xlsx")
                The line above is hardcoded to run in assignment.py, using Pandas
                Since I have relocated the files to ./src/, this will fail

    Solution 2. Overload pd.read_excel() to append ./src/ to path whenever it calls
                canteens.xlsx

    Problem 3.  Same issue as Problem 2 but with NTUcampus.jpg and pin.png

    Solution 3. Same solution as Solution 2 except:
                NTUcampus.jpg requires spoofing PIL's Image.open()
                pin.png requires spoofing pygame.image.load()
    """

    #Spoof Pandas' read_excel by redirecting function address
    original_read_excel = pd.read_excel
    def spoofed_read_excel(io, *args, **kwargs):
        if isinstance(io, str) and io == "canteens.xlsx":
            io = os.path.join(os.getcwd(), "src", "canteens.xlsx")
        return original_read_excel(io, *args, **kwargs)
    pd.read_excel = spoofed_read_excel

    #Spoof PIL's Image.open by redirecting function address
    original_open = Image.open
    def spoofed_image_open(io, mode="r", formats=None):
        targets = ['NTUcampus.jpg', 'pin.png']
        if isinstance(io, str) and io in targets:
            io = os.path.join("src", io)
        return original_open(io, mode, formats)
    Image.open = spoofed_image_open

    #Spoof pygame's image.load by redirecting function address
    original_pygame_load = pygame.image.load
    def spoofed_pygame_load(file, *args, **kwargs):
        targets = ['NTUcampus.jpg', 'pin.png']
        if isinstance(file, str) and os.path.basename(file) in targets:
            file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", os.path.basename(file))
        return original_pygame_load(file, *args, **kwargs)
    pygame.image.load = spoofed_pygame_load
    
    #Skips assignment.py's main() by redirecting stdout
    saved_stdin = builtins.input
    builtins.input = lambda _: "5" #Exit assignment.py's CLI interface
    with open(os.devnull, 'w') as f:
        save_stdout = sys.stdout
        sys.stdout = f
        try:
            from src import assignment #This is assignment.py
        finally:
            sys.stdout = save_stdout
            if __debug__: print("[DEBUG] assignment.py main() spoofed.")
    builtins.input = saved_stdin
    return assignment


class CanteenQuery:
    """This class handles the db Query Logic"""

    def __init__(self, path):
        """
        Loads the data from assignment.py
        """
        self.keywords = assignment.load_stall_keywords(path)
        self.prices = assignment.load_stall_prices(path)
        self.canteen_locations = assignment.load_canteen_location(path)
    
    def __normalize_query(self, key):
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

        #REGEX Cleaning (Documentation for each step in ./testbench/regextest.py)
        #Looks like a lot of step but this should be most optimised to cover all edge cases
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

        #Splits into data structure where AND groups are in a single list
        #For e.g. AB + C will be [[A,B],[C]] 
        for group in or_groups_intermediate:
            and_groups_intermediate = re.split(r'&', group)
            key_groups.append(and_groups_intermediate)

        return key_groups
    
    def __find_keywords(self, conditions):
        """
        Returns all stalls that matches and_group conditions from query
        Returns as list of dictionaries containing canteen, stall name, keywords and matched keywords
        """
        results = []
        
        for canteen_name, stalls in self.keywords.items():
            for stall_name, keywords_str in stalls.items():
                stall_keywords = {k.strip().upper() for k in keywords_str.split(',')}
                matched_group = None
                for and_group in conditions:
                    if all(req_key in stall_keywords for req_key in and_group):
                        matched_group = and_group
                        results.append({
                            "canteen": canteen_name,
                            "stall": stall_name,
                            "keywords": stall_keywords,
                            "matched": matched_group
                        })
        
        return results

    def search_by_keyword(self, key):
        """Return results by keyword"""

        if not isinstance(key, str): return None
        parsed_key = self.__normalize_query(key)
        results = self.__find_keywords(parsed_key)
        
        if __debug__:
            return [results, parsed_key]
        else:
            return results

    def search_by_price(self, min, max):
        """Return results by price within min, max (inclusive of both)"""
        
        results = []
        for canteen_name, stalls in self.prices.items():
            for stall_name, price in stalls.items():
                if min <= price <= max:
                    results.append({
                        "canteen": canteen_name,
                        "stall": stall_name,
                        "price": price
                    })
        return results

    def search_nearest_canteens(self, k):
        """
        Return k results by location
        Locations are sorted based on max(distance_to_A, distance_to_B)
        To ensure minimum time for both parties to reach the location
        """

        #Calls the location selector from assignment.py
        ax, ay = assignment.get_user_location_interface()
        bx, by = assignment.get_user_location_interface()

        results = []
        for canteen_name, location in self.canteen_locations.items():
            x, y = location
            distance_to_A = math.sqrt((x - ax)**2 + (y - ay)**2)
            distance_to_B = math.sqrt((x - bx)**2 + (y - by)**2)
            max_distance = max(distance_to_A, distance_to_B)
            results.append({
                "canteen": canteen_name,
                "distanceA": int(distance_to_A),
                "distanceB": int(distance_to_B),
                "max": int(max_distance)
            })
        results.sort(key=lambda v: v['max'])
        return results[:k]


class CurseMenu:
    """This class handles the CLI Terminal Interface using Curses"""

    def __init__(self, db):
        """References the Db as initialised by CanteenQuery"""
        self.db = db

    def __draw_menu(self, select_row, option):
        """Draws main option menu"""
        
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
        self.stdscr.bkgd(' ', curses.color_pair(2))
        self.stdscr.erase()
        h, w = self.stdscr.getmaxyx()
        self.__draw_art(h)

        title = "--- F&B RECOMMENDATION MENU ---"
        mark = "Written by R15 Yeo Shu Yi (U2524018L)"
        self.stdscr.attron(curses.A_BOLD)
        self.stdscr.addstr(1, w//2 - len(title)//2, title)
        self.stdscr.addstr(2, w//2 - len(mark)//2, mark)
        self.stdscr.attroff(curses.A_BOLD)
        self.stdscr.border(0)

        if __debug__:
            self.stdscr.addstr(h-2,2, "[DEBUG] Running in debug mode. Additional prints shown. Run python3 -O main.py to disable.")

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

    def __get_input_str(self, prompt, y, x):
        """
        Input for search_by_keyword.
        Input validation done backend through regex.
        """

        while True:
            self.stdscr.addstr(y+6, x, prompt)
            curses.echo()
            self.stdscr.addstr(y+1, x, 
                f"1. Conditions may utilize AND / OR operators (AND priority) together."
            )
            self.stdscr.addstr(y+2, x, 
                f"2. Space between 2 keywords treated as AND. All inputs are non case-sensitive."
            )
            self.stdscr.addstr(y+3, x, 
                f"3. Symbols, leading whitespaces / operators will be ignored."
            )
            self.stdscr.addstr(y+4, x, 
                f"E.g. MALAY SPICY OR CHINESE AND WESTERN will be treated as (MALAY & SPICY) + (CHINESE & WESTERN)"
            )
            self.stdscr.attron(curses.color_pair(1))
            user_input = self.stdscr.getstr(y+7, x, 80).decode('utf-8')
            self.stdscr.attroff(curses.color_pair(1))
            curses.noecho()
            if not user_input: 
                self.stdscr.addstr(y+2, x, "Input cannot be empty!")
                continue
            self.user_input = user_input
            break
    
    def __get_input_float(self, prompt, y, x, min=0):
            """
            Input for search_by_price.
            float > min
            """

            h, w = self.stdscr.getmaxyx()
            while True:
                self.stdscr.erase()
                title = "--- PRICE SEARCH ---"
                self.stdscr.attron(curses.A_BOLD)
                self.stdscr.addstr(1, w//2 - len(title)//2, title)
                self.stdscr.attroff(curses.A_BOLD)
                self.stdscr.border(0)
                self.stdscr.addstr(y, x, prompt)
                curses.echo()
                self.stdscr.attron(curses.color_pair(1))
                user_input = self.stdscr.getstr(y+1, x, 80).decode('utf-8')
                self.stdscr.attroff(curses.color_pair(1))
                curses.noecho()
                try:
                    user_value = float(user_input)
                    if user_value < min:
                        self.stdscr.addstr(y+2, x, f"Input must be more than ${min:.2f}!")
                        self.stdscr.refresh()
                        time.sleep(1)
                        continue
                    break
                except ValueError:
                    self.stdscr.addstr(y+2, x, "Input must be integer/float!")
                    self.stdscr.refresh()
                    time.sleep(1)
                    continue
            return user_value
    
    def __get_input_int(self, prompt, y, x):
            """
            Input for search_nearest_canteens.
            int > 0
            """

            h, w = self.stdscr.getmaxyx()
            while True:
                self.stdscr.erase()
                title = "--- LOCATION SEARCH ---"
                self.stdscr.attron(curses.A_BOLD)
                self.stdscr.addstr(1, w//2 - len(title)//2, title)
                self.stdscr.attroff(curses.A_BOLD)
                self.stdscr.border(0)
                self.stdscr.addstr(y, x, prompt)
                curses.echo()
                self.stdscr.attron(curses.color_pair(1))
                user_input = self.stdscr.getstr(y+1, x, 80).decode('utf-8')
                self.stdscr.attroff(curses.color_pair(1))
                curses.noecho()
                try:
                    user_value = int(user_input)
                    if user_value < 1:
                        self.stdscr.addstr(y+2, x, f"Input must be more than 0!")
                        self.stdscr.refresh()
                        time.sleep(1)
                        continue
                    break
                except:
                    self.stdscr.addstr(y+2, x, "Input must be integer!")
                    self.stdscr.refresh()
                    time.sleep(1)
                    continue
            return user_value
    
    def __draw_art(self, h):
        """Just a fun function to draw REP on the main menu."""

        logo = [
            "░▒▓███████▓▒░░▒▓████████▓▒░▒▓███████▓▒░  ",
            "░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ ",
            "░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ ",
            "░▒▓███████▓▒░░▒▓██████▓▒░ ░▒▓███████▓▒░  ",
            "░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░        ",
            "░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░        ",
            "░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░        "
        ]

        for i, line in enumerate(logo):
            self.stdscr.addstr(h//2 + i - 3, 10, line)

    def main_menu(self, stdscr):
        """Contains logic for each menu option."""

        self.stdscr = stdscr
        h, w = self.stdscr.getmaxyx()
        if w < 100 or h < 20:
            raise SystemError(
                f"[ERROR] Please expand your CLI to at least 20x100. "
                f"Currently {h}x{w}."
            )
        
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
        menu = ['Display Data', 'Keyword Search', 'Price Search', 'Location Search', 'Exit']
        current_row = 0

        #Main Menu
        while True:
            self.__draw_menu(current_row, menu)
        
            key = self.stdscr.getch()

            #Arrow Key Detection
            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
                current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                match current_row:
                    case 0: #List Data
                        #Case 0's code has been rewritten by Gemini to improve GUI interface
                        #Refer to submission for documentation
                        self.stdscr.erase()
                        title = "--- DATABASE DICTIONARIES ---"
                        self.stdscr.attron(curses.A_BOLD)
                        self.stdscr.addstr(1, w//2 - len(title)//2, title)
                        self.stdscr.attroff(curses.A_BOLD)
                        self.stdscr.border(0)

                        col1_width = 15
                        col2_width = w - col1_width - 8 # Leave some padding on the right

                        def format_dict(d):
                            """Formats the dictionary into a readable string without curly braces."""
                            if not isinstance(d, dict):
                                return str(d)
                            parts = []
                            for k, v in d.items():
                                if isinstance(v, dict):
                                    # Format nested dictionaries: "Canteen -> Stall: Value"
                                    sub_parts = [f"{sk}: {sv}" for sk, sv in v.items()]
                                    parts.append(f"{k} -> {', '.join(sub_parts)}")
                                else:
                                    parts.append(f"{k}: {v}")
                            return "  |  ".join(parts)

                        data = [
                            ("Keywords", format_dict(self.db.keywords)),
                            ("Prices", format_dict(self.db.prices)),
                            ("Locations", format_dict(self.db.canteen_locations))
                        ]
                        
                        start_y = 4
                        for idx, (category, content) in enumerate(data):
                            y = start_y + (idx * 4) # 3 rows for data + 1 row for the separator
                            
                            if y + 3 >= h - 1:
                                break # Prevent drawing out of bounds

                            # Wrap the text to fit the column width nicely
                            wrapped_lines = textwrap.wrap(content, width=col2_width)
                            
                            # Add category title on the first row
                            self.stdscr.addstr(y, 5, category.ljust(col1_width), curses.A_BOLD)
                            
                            # Print exactly 3 lines (filling with blanks if text is shorter)
                            for i in range(3):
                                self.stdscr.addstr(y + i, 5 + col1_width, " | ")
                                if i < len(wrapped_lines):
                                    self.stdscr.addstr(y + i, 5 + col1_width + 3, wrapped_lines[i])

                            # Draw the dotted separator underneath the 3 rows
                            self.stdscr.addstr(y + 3, 5, "-" * (col1_width + col2_width + 3), curses.A_DIM)

                        self.stdscr.addstr(h-2, 5, "Press any key to return...")
                        self.stdscr.refresh()
                        self.stdscr.getch()
                                           
                    case 1: #Search by Keyword
                        self.stdscr.erase()
                        title = "--- KEYWORD SEARCH ---"
                        self.stdscr.attron(curses.A_BOLD)
                        self.stdscr.addstr(1, w//2 - len(title)//2, title)
                        self.stdscr.attroff(curses.A_BOLD)
                        self.stdscr.border(0)
                        self.__get_input_str("Enter Search Query:", 4, 2)

                        if __debug__:
                            temporary_results = self.db.search_by_keyword(self.user_input)
                            results = temporary_results[0]
                        else:
                            results = self.db.search_by_keyword(self.user_input)
                        

                        self.stdscr.erase()
                        title = "--- SEARCH RESULTS ---"
                        self.stdscr.attron(curses.A_BOLD)
                        self.stdscr.addstr(1, w//2 - len(title)//2, title)
                        self.stdscr.attroff(curses.A_BOLD)
                        self.stdscr.border(0)

                        if __debug__:
                            debug_str = f"[DEBUG] Parsed Query: {temporary_results[1]}" 
                            self.stdscr.addstr(h-2,2, debug_str)

                        if not results:
                            self.stdscr.addstr(h//2, w//2 - 10, "No matches found.")
                        else:
                            header_str = f"{'CANTEEN'.ljust(25)} {'STALL'.ljust(27)} {'MATCHED'}"
                            self.stdscr.addstr(3, 4, header_str.ljust(w-8)) 
                            
                            for idx, match in enumerate(results):
                                y = 4 + idx
                                if y >= h - 3:
                                    self.stdscr.addstr(y, 4, "... more results hidden ...", curses.A_DIM)
                                    break
                                
                                c_name = match['canteen'][:24].ljust(25)
                                s_name = match['stall'][:24].ljust(25)
                                criteria = str(match['matched'])

                                row_str = f"{c_name} | {s_name} | {criteria}"
                                self.stdscr.addstr(y, 4, row_str)
                        self.stdscr.addstr(h-3, 5, "Press any key to return...")
                        self.stdscr.getch()
                    
                    case 2: #Search by Price
                        min = self.__get_input_float("Enter Minimum Price: ", 4, 2, 0.00)
                        max = self.__get_input_float("Enter Maximum Price: ", 4, 2, min)
                        results = self.db.search_by_price(min, max)

                        self.stdscr.erase()
                        title = "--- SEARCH RESULTS ---"
                        self.stdscr.attron(curses.A_BOLD)
                        self.stdscr.addstr(1, w//2 - len(title)//2, title)
                        self.stdscr.attroff(curses.A_BOLD)
                        self.stdscr.border(0)

                        if not results:
                            self.stdscr.addstr(h//2, w//2 - 10, "No matches found.")
                        else:
                            header_str = f"{'CANTEEN'.ljust(25)} {'STALL'.ljust(27)} {'PRICE'}"
                            self.stdscr.addstr(3, 4, header_str.ljust(w-8)) 
                            
                            for idx, match in enumerate(results):
                                y = 4 + idx
                                if y >= h - 3:
                                    self.stdscr.addstr(y, 4, "... more results hidden ...", curses.A_DIM)
                                    break
                                
                                c_name = match['canteen'][:24].ljust(25)
                                s_name = match['stall'][:24].ljust(25)
                                criteria = str(match['price'])

                                row_str = f"{c_name} | {s_name} | {criteria}"
                                self.stdscr.addstr(y, 4, row_str)
                        self.stdscr.addstr(h-3, 5, "Press any key to return...")
                        self.stdscr.getch()

                    case 3: #Search by Location
                        self.stdscr.erase()
                        stall_count = self.__get_input_int("Enter Number of Stalls: ", 4, 2)

                        self.stdscr.erase()
                        title = "--- LOCATION SEARCH ---"
                        self.stdscr.attron(curses.A_BOLD)
                        self.stdscr.addstr(1, w//2 - len(title)//2, title)
                        self.stdscr.attroff(curses.A_BOLD)
                        self.stdscr.border(0)

                        self.stdscr.addstr(4, 2, "Please select 2 locations on the map.")
                        self.stdscr.refresh()
                        time.sleep(1)

                        self.stdscr.erase()

                        results = self.db.search_nearest_canteens(stall_count)
                        title = "--- LOCATION SEARCH ---"
                        self.stdscr.attron(curses.A_BOLD)
                        self.stdscr.addstr(1, w//2 - len(title)//2, title)
                        self.stdscr.attroff(curses.A_BOLD)
                        self.stdscr.border(0)

                        if not results:
                            self.stdscr.addstr(h//2, w//2 - 10, "No matches found.")
                        else:
                            header_str = f"{'CANTEEN'.ljust(25)} {'DISTANCE TO USER A / m'.ljust(25)} {'DISTANCE TO USER B / m'.ljust(25)} {'MAX DISTANCE / m'.ljust(25)}"
                            self.stdscr.addstr(3, 4, header_str.ljust(w-8)) 
                            
                            for idx, match in enumerate(results):
                                y = 4 + idx
                                if y >= h - 3:
                                    self.stdscr.addstr(y, 4, "... more results hidden ...", curses.A_DIM)
                                    break
                                
                                c_name = match['canteen'][:24].ljust(25)
                                disA = str(match['distanceA']).ljust(23)
                                disB = str(match['distanceB']).ljust(23)
                                max_dis = str(match['max'])

                                row_str = f"{c_name} | {disA} | {disB} | {max_dis}"
                                self.stdscr.addstr(y, 4, row_str)
                        self.stdscr.addstr(h-3, 5, "Press any key to return...")
                        self.stdscr.getch()
                    
                    case 4: #Exit
                        self.stdscr.erase()
                        title = "--- THANK YOU! GOODBYE! ---"
                        self.stdscr.attron(curses.A_BOLD)
                        self.stdscr.addstr(1, w//2 - len(title)//2, title)
                        self.stdscr.attroff(curses.A_BOLD)
                        self.stdscr.border(0)
                        self.stdscr.refresh()
                        time.sleep(1)
                        self.stdscr.erase()
                        break


def main():
    """Main function for user interface"""

    #Db and Menu Init
    db = CanteenQuery(path=DATABASE_PATH)
    menu = CurseMenu(db)
    curses.wrapper(menu.main_menu)            


if __name__ == "__main__":
    if __debug__: print("[DEBUG] Program is in Debug mode. Run python3 -O main.py for Normal Mode.")
    assignment = import_assignmentpy()
    main()
