## CAA: 03-Feb-2026

### Acknowledgements
Written by Yeo Shu Yi, for RE1016 Individual Assignment.</br>

* **Dr. Ong Yew Soon** - Author of original assignment.py.

### File Management
**No modifications done to assignment.py! main.py calls assignment.py as module**
- main.py is the main program.
- assignment.py is the provided module.
- changelog.md contains commit history.
- requirements.txt contains PIP library requirements.
- requirements_windows.txt contains additional libraries for windows users.

### Setup
1. Clone the repository:</br>
```bash
cd <REPO PATH>
git clone https://github.com/yeoshuyi/RE1016-Assignment-2.git
cd RE1016-Assignment-2
```
2. Install PIP libraries with venv (optional):</br>
```bash
#OPTIONAL VENV SETUP (May differ based on OS)
python3 -m venv .venv
source ./.venv/bin/activate

#INSTALL LIBRARY
python3 -m pip install -r requirements.txt

#ADDITIONAL STEP FOR WINDOWS USER
python3 -m pip install -r requirements_windows.txt
```
> requirements_windows.txt contains a curses wrapper for Windows, as it is not included in non-unix systems by default.
3. Run main.py:</br>
**Ensure CLI window is at least 20x100, or SystemError will be raised to avoid graphical glitches.**
```bash
python3 -O main.py #Run without -O flag to see debug prints
```
### Changelog
Refer to changelog.md.

### External Libraries
External libraries as per assignment requirements with no additions made.</br>
Curses library is in-built to UNIX systems, but will require wrapper on Windows.</br>
Refer to requirements.txt for full list.</br>

