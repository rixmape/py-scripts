# Makefile to create batch files for Python scripts

# Directories
SCRIPT_DIR := scripts
BIN_DIR := bin
VENV_DIR := .venv

# Find all Python scripts in the scripts directory
PY_SCRIPTS := $(wildcard $(SCRIPT_DIR)/*.py)

# Define batch file paths in the bin directory
BAT_FILES := $(patsubst $(SCRIPT_DIR)/%.py, $(BIN_DIR)/%.bat, $(PY_SCRIPTS))

# Default target
all: $(BAT_FILES)

# Rule to convert a Python script to a batch file
$(BIN_DIR)/%.bat: $(SCRIPT_DIR)/%.py
	@echo Creating batch file for $<
	@mkdir -p $(BIN_DIR)
	@echo @echo off > $@
	@echo call "$(VENV_DIR)/Scripts/activate" >> $@
	@echo python "$<" %* >> $@
	@echo deactivate >> $@

# Clean up generated batch files
clean:
	@echo Cleaning up...
	@rm -f $(BIN_DIR)/*.bat
