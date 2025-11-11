# Minimal makefile for Sphinx documentation

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = python -msphinx
SPHINXPROJ    = saviialib
SOURCEDIR     = .
BUILDDIR      = _build

PACKAGE_NAME  = saviia-lib

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


# Review the lint integration
lint:
	ruff check . --fix
	ruff format .

# Uninstall the package
uninstall:
	pip uninstall $(PACKAGE_NAME) -y || true