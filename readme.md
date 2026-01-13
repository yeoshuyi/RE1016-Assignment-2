## CAA: 13-Jan-2025

### Acknowledgements
Written by Yeo Shu Yi, for RE1016 Individual Assignment.</br>
Much of this program is refactored from the original assignment.py. </br></br>

* **Dr. Ong Yew Soon** - Author of original assignment.py.

### File Management
- /src directory contains resources (E.g. images, excel file).
- /testbench directory contains test files for specific code sections.
- main.py is the main program.
- update.md contains commit history.
- requirements.txt contains PIP library requirements.

### Setup
1. Clone the repository:
   ```bash
   cd <REPO PATH>
   git clone https://github.com/yeoshuyi/RE1016-Assignment-2.git
2. Install PIP libraries with venv (optional):
   ```bash
   #OPTIONAL VENV SETUP
   python3 -m venv .venv
   source ./.venv/bin/activate #For UNIX systems

   #INSTALL LIBRARY
   python3 -m pip install -r requirements.txt
3. Run main.py:
   ```bash
   python3 -O main.py #Run without -O flag to see debug prints

### Changelog
Refer to changelog.md.
