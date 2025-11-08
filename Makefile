SHELL := /bin/bash
REPO_NAME := agentic-ai-workflow

ifeq ($(OS),Windows_NT)
	PYTHON = python.exe
	ACTIVATE_VENV = venv\Scripts\activate
else
	PYTHON = python3.13
	ACTIVATE_VENV = source venv/bin/activate
endif
PIP = $(PYTHON) -m pip

-include .env

.PHONY: check-python init

# Default target executed when no arguments are given to make.
all: help

analyze:
	cloc . --exclude-ext=svg,json,zip --vcs=git

# ---------------------------------------------------------
# Python
# ---------------------------------------------------------
check-python:
	@command -v $(PYTHON) >/dev/null 2>&1 || { echo >&2 "This project requires $(PYTHON) but it's not installed.  Aborting."; exit 1; }

init:
	mkdir -p .pypi_cache && \
	make check-python
	npm install && \
	$(PYTHON) -m venv venv && \
	$(ACTIVATE_VENV) && \
	PIP_CACHE_DIR=.pypi_cache $(PIP) install --upgrade pip && \
	PIP_CACHE_DIR=.pypi_cache $(PIP) install -r requirements.txt


