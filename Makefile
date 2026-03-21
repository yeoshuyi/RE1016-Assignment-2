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
.PHONY: help run debug setup clean

help:
	@echo "Usage:"
	@echo "	make setup	- Create .venv and Install Requirements"
	@echo "	make run	- Run Program"
	@echo "	make debug	- Run in Debug Mode"
	@echo "	make clean 	- Remove Temporary Files and .venv"

run:
	$(PYTHON) -OO main.py

debug:
	$(PYTHON) -d -W error -i -v -X dev main.py 

setup:
	python3 -m venv .venv || python -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(EXTRA_INSTALL)

clean:
	$(RM) __pycache__
	$(RM) src/__pycache__
	$(RM) .venv