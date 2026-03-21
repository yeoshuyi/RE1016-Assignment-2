# Functional Documentation for main.py

## Library Imports
```python
import re               #For REGEX Filtering
import os               #For File Path
import sys              #For stdout Redirection
import builtins         #For Redefining stdin using Lambda
import curses           #For UNIX-Style CLI
import time             #For Loop Delay
import math             #For Sqrt Function
import pygame           #For Redefining pygame.image.load
import pandas as pd     #For Redefining pd.readexcel
from PIL import Image   #For Redefining Image.open
```

## Support for import assignment
### Motivation
Based on the assignment requirements, the pre-written parts of assignment.py program should not be editted. Taking this one step further, I decided not to touch assignment.py at all, but rather call the module through the following:
```python
def import_assignment.py():
    #Some Logic
    import src\assignment
    #More Logic
    return assignment
```
However, this has posed a few problems, namely:
* The default CLI in assignment.py runs within a main() loop, that is not protected by \_\_name\_\_ guards. Thus, when import assignment is executed, the default CLI shows up instead of the Curses CLI implemented in main.py.
* All file paths within assignment.py are hardcoded. This poses an issue as assignment.py is now within the src directory. Since main.py is in a different directory, the default path used by each of the file management functions in pygame, NumPy and PIL does not work.

>*My workarounds for these issues involve modifying global namespace functions, which I highly do not recommend. However in this case, I could not think of a better solution. To make things better, I made sure that the redefinitions should only target specific inputs.*

### Implementation for Issue #1
To solve the first issue, we implement the following:
```python
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
```
builtins.input interfaces with the stdin stream, but is redefined to just be the character '5'. When assignment.py is imported, the following chunk of code runs:
```python
while loop:

    # Truncated

    option = int(input("Enter option [1-5]: "))

    # Truncated

    elif option == 5:
        # exit the program
        print("Exiting F&B Recommendation")
        loop = False
```
Since input has been shadowed to return the literal character 5 within main.py, assignment.py exits its main loop immediately and returns to main.py, effectively bypassing the default CLI.

### Implementation for Issue #2

> *My workarounds for these issues involve modifying global namespace functions, which I highly do not recommend. However in this case, I could not think of a better solution. To make things better, I made sure that the redefinitions should only target specific inputs.*
To solve the second issue, we implement the following:
```python
original_pygame_load = pygame.image.load
def spoofed_pygame_load(file, *args, **kwargs):
    targets = ['NTUcampus.jpg', 'pin.png']
    if isinstance(file, str) and os.path.basename(file) in targets:
        file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", os.path.basename(file))
    return original_pygame_load(file, *args, **kwargs)
pygame.image.load = spoofed_pygame_load
```
Pygame's original load function is shadowed by the spoofed version, which redirects any arguments "NTUcampus.jpg" and "pin.png" to the actual directory location using os.path (os.path is used to ensure cross compatability with Windows). The same logic is used to handle PIL and NumPy equivalent load functions.

## REGEX Cleaning for Key-based Search
### Cleaning

> *To be honest, with the time taken to write this regex filter, I could have probably just written a proper lexer/tokenizer*
Based on the rules:
    1.  Any leading/trailing AND, OR, /s is ignored.
    2.  Any non-alphanumeric symbols is ignored.
    3.  In all cases "Foo AND OR AND AND OR... Bar", logic is resolved to a single AND
        as long as a single "AND" is present. 
    4.  If no "AND" present, in the case of "Foo OR OR... Bar", logic is resolved to a single OR.
    5.  In all cases "Foo AND Bar OR Buz AND Qux", AND takes priority as (Foo & Bar) + (Buz & Qux).
    6.  Cases like the restaurant "ANDES" will not be resolved as AND, as only /bAND/b is accepted.

Logic has been minimized and tested over many edge cases within /testbench/regextest.py
No known issues to date

```python
key = key.upper()
key = re.sub(r'[^a-zA-Z0-9\s]+', '', key) #rmv all non alphanumeric
key = re.sub(r'\s+',' ', key) #trim all \s+ to just \s
key = re.sub(r'\bAND\b', '&', key) #convert all word AND to &
key = re.sub(r'\bOR\b', '@', key) #convert all word OR to @
key = re.sub(r'(?<![@&])\s+(?![@&])', '&', key) #convert all space that is not beside &/@ into &
key = re.sub(r'\s+','', key) #remove all \s
key = re.sub(r'^[@&]+|[@&]+$', '', key) #remove all leading/trailing @&
key = re.sub(r'[\s@]*&[\s@&]*', '&', key) #replace all series of any @@&&&@&@&@ to & as long as 1 & present
key = re.sub(r'[@]*@[@]*', '@', key) #replace all series of @@@@@ to just @

key_groups_intermediate = re.split(r'@', key) #split into sum of products
key_groups = []
```
>*While the logic seems over-complicated, this has been severely optimized to cover all edge cases. Further simplification usually leads to some edge cases failing.*

## MakeFile
Handles Unix / Windows compatability for requirements installation.
```Makefile
ifeq ($(OS), Windows_NT)
    VENV_PATH = .venv\Scripts
    PYTHON = $(VENV_PATH)\python.exe
    PIP = $(VENV_PATH)\pip.exe
    RM = del /Q
    FIX_PATH = $(subst /,\,$1)
    EXTRA_INSTALL = $(PIP) install -r requirements_windows.txt
else
    VENV_PATH = .venv/bin
    PYTHON = ./$(VENV_PATH)/python
    PIP = ./$(VENV_PATH)/pip
    RM = rm -rf
    FIX_PATH = $1
    EXTRA_INSTALL = 
endif
```