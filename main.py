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
        if __debug__: 
            print(f"[DEBUG] Query resolved as:\n{parsed_key}")
        

        return 0
    
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
    
    def search_by_location(self):
        assignment.get_user_location_interface()


def main():
    """Main function for user interface"""

    #Db Init
    db = CanteenQuery(path=DATABASE_PATH)

    while True:
        print(
            "========================\n"
            "F&B Recommendation Menu\n"
            "1 -- Display Data\n"
            "2 -- Keyword-based Search\n"
            "3 -- Price-based Search\n"
            "4 -- Location-based Search\n"
            "5 -- Exit Program\n"
            "========================"
        )

        while True:
            try:
                user_option = int(input("Enter option [1-5]: "))
                if not 0 < user_option < 6:
                    raise ValueError("Out of range.")
                break
            except ValueError:
                print("Please try again.")
    
        match user_option:
            case 1:
                print(
                    f"1 -- Display Data\n"
                    f"Keyword Dictionary: {db.keywords}\n"
                    f"Price Dictionary: {db.prices}\n"
                    f"Location Dictionary: {db.canteen_locations}\n"
                )
            case 2:
                user_option = input("Enter query: ")
                db.search_by_keywords(user_option)
            case 3:
                print("Hi!")
            case 4:
                db.search_by_location()
            case 5:
                print("Thank you, goodbye!")
                return(1)
            


if __name__ == "__main__":
    if __debug__: print("[DEBUG] Program is in Debug mode. Run python3 -O main.py for Normal Mode.")
    main()