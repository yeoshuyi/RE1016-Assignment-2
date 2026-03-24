## CAA: 24-Mar-2026

### Authors
main.py by Yeo Shu Yi, for RE1016 Individual Assignment.</br>

* **Dr. Ong Yew Soon** - Author of original assignment.py and all files within /src.
* Refer to documentation.md for function documentation
* Refer to changelog.md to view changelog

### File Management
**No modifications done to assignment.py! main.py calls assignment.py as module**
```bash
#Ensure files are in ./src!
├── main.py                     #main program
├── Makefile                    #For automation via GNU make
├── CHANGELOG.md
├── DOCUMENTATION.md
├── README.md                   #This File
├── requirements.txt            #Install on BOTH Windows and Unix
├── requirements_windows.txt    #Install on Windows only
├── src                         #Clone all assignment files here, main.py will call them
│   ├── assignment.py
│   ├── canteens.xlsx
│   ├── __init__.py             #Blank file to allow calling /src/ as module
│   ├── NTUcampus.jpg
│   └── pin.png
└── testbench
    ├── querytest.py            #Test code for keyword query
    └── regextest.py            #Test code for regex filter
```

### Setup
> *Please ensure that you are running Python 3.13, as pygame and curses is not supported on 3.14 as of yet.*
For best user experienece, I recommend running the code from terminal in full screen. </br>

1. Clone the repository:</br>
```bash
cd <REPO PATH>
git clone https://github.com/yeoshuyi/RE1016-Assignment-2.git
cd RE1016-Assignment-2
```
2. Install PIP libraries with venv (optional):</br>
```bash
#OPTIONAL VENV SETUP (May differ based on OS)
python3 -3.13 -m venv .venv
source ./.venv/bin/activate || ./venv/Script/Activate

#INSTALL LIBRARY
python3 -m pip install -r requirements.txt

#ADDITIONAL STEP FOR WINDOWS USER (MUST USE PYTHON 3.13 / 3.12)
python3 -m pip install -r requirements_windows.txt
```
> requirements_windows.txt contains a curses wrapper for Windows, as it is not included in non-unix systems by default.
3. Run main.py:</br>
**Ensure CLI window is at least 20x100, or SystemError will be raised to avoid graphical glitches.**
```bash
python3 -OO main.py #Run without -OO flag to see debug prints

python3 -d -i -v main.py #Run with debug prints
```

### Alternate Setup
> *Alternatively, run make help, setup, clean, run and debug for automated processes with cross-compatability between Windows and Unix-like. Windows users will require a ported version of GNU make.*

### Common Issues
1. Terminal not found... (Make sure you run using python3 -O main.py in terminal with the right env!)
2. Curses not found... (On Windows, you need to pip install the curses-window library!)
3. pip install pygame or windows-curses not found... (Downgrade to Python 3.13!)
3. CLI must be at least 100x20... (Expand your terminal bigger before running!)
4. stdscr not found... (Some IDEs, when running through the run button instead of terminal, does not pass stdscr properly. Please run through terminal.)
5. canteens/NTUcampus/pin not found... (Either they are not cloned to /src properly, or something went horribly wrong with my import function import_assignmentpy()... please email me)

### Changelog
Refer to CHANGELOG.md.

### External Libraries
External libraries as per assignment requirements with no additions made.</br>
Curses library is in-built to unix-like systems, but will require wrapper on Windows.</br>
Refer to requirements.txt and requirements_windows for full list.</br>

### AI Usage
Generative AI (Gemini) has been used to rewrite Case 0 of the CurseMenu class to improve GUI Interface.
https://gemini.google.com/share/14079e20fc62
```python
case 0: #List Data
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
```