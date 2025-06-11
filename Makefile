SHELL := /bin/bash
include .env
export PATH := /usr/local/bin:$(PATH)
export

ifeq ($(OS),Windows_NT)
    PYTHON := python.exe
    ACTIVATE_VENV := venv\Scripts\activate
else
    PYTHON := python3.12
    ACTIVATE_VENV := source venv/bin/activate
endif
PIP := $(PYTHON) -m pip

ifneq ("$(wildcard .env)","")
else
    $(shell cp ./doc/example-dot-env .env)
endif

.PHONY: check-python init

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


