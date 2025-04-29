# Minimal makefile for Sphinx documentation

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = python -msphinx
SPHINXPROJ    = rcer_iot_client_pkg
SOURCEDIR     = .
BUILDDIR      = _build

PACKAGE_NAME  = rcer-iot-client

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile install-deps install dev test lint format build upload release uninstall check test-install

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Install basic dependencies
install-deps:
	pip3 install .

# Install development requirements
dev:
	pip3 install .[dev]

# Run all tests in the project
test:
	python3 tests/run_tests.py

# Review the lint integration
lint:
	ruff check . --fix
	ruff format .

# Build compiled package
build:
	rm -rf dist/ build/ *.egg-info
	python3 -m build

# Upload to PyPi
upload:
	twine upload dist/*

# Make a new release
release: 
	make build upload

# Uninstall the package
uninstall:
	pip uninstall $(PACKAGE_NAME) -y || true


# All together: uninstall, install, and verify
test-install: uninstall install check