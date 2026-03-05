## CAA: 28-Feb-2026

### Acknowledgements
Written by Yeo Shu Yi, for RE1016 Individual Assignment.</br>

* **Dr. Ong Yew Soon** - Author of original assignment.py.
* Refer to documentation.md for function documentation
* Refer to changelog.md to view changelog

### File Management
**No modifications done to assignment.py! main.py calls assignment.py as module**
```bash
#Ensure files are in ./src!
├── changelog.md
├── documentation.md
├── main.py                     #main program
├── readme.md
├── requirements.txt            #Install on BOTH Windows and Unix
├── requirements_windows.txt    #Install on Windows only
├── old                         #Old files, ignore please
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
source ./.venv/bin/activate

#INSTALL LIBRARY
python3 -m pip install -r requirements.txt

#ADDITIONAL STEP FOR WINDOWS USER (MUST USE PYTHON 3.13 / 3.12)
python3 -m pip install -r requirements_windows.txt
```
> requirements_windows.txt contains a curses wrapper for Windows, as it is not included in non-unix systems by default.
3. Run main.py:</br>
**Ensure CLI window is at least 20x100, or SystemError will be raised to avoid graphical glitches.**
```bash
python3 -O main.py #Run without -O flag to see debug prints
```

### Common Issues
1. Terminal not found... (Make sure you run using python3 -O main.py in terminal with the right env!)
2. Curses not found... (On Windows, you need to pip install the curses-window library!)
3. pip install pygame or windows-curses not found... (Downgrade to Python 3.13!)
3. CLI must be at least 100x20... (Expand your terminal bigger before running!)
4. stdscr not found... (Some IDEs, when running through the run button instead of terminal, does not pass stdscr properly. Please run through terminal.)
5. canteens/NTUcampus/pin not found... (Either they are not cloned to /src properly, or something went horribly wrong with my import function import_assignmentpy()... please email me)

### Changelog
Refer to changelog.md.

### External Libraries
External libraries as per assignment requirements with no additions made.</br>
Curses library is in-built to UNIX systems, but will require wrapper on Windows.</br>
Refer to requirements.txt for full list.</br>

