NAME := python-whmcs
BUILD_DIR := build
DOCS_DIR := docs
TESTS_DIR := tests


.PHONY: $(NAME) all install install-devel uninstall check lint docs builddir clean distclean

all: builddir $(NAME)

$(NAME):
	python setup.py bdist_wheel

install: $(NAME) | builddir uninstall
	find dist/ -name "$(NAME)*.whl" | xargs -I FOO pip install FOO

install-devel: $(NAME) | builddir uninstall
	pip install -e .[devel]

uninstall:
	pip uninstall -y $(NAME)

check: $(NAME) | builddir
	nosetests -v \
	    --logging-format="[%(asctime)s][%(levelname)-8s][%(name)s:%(funcName)s:%(lineno)d]: %(message)s" \
	    --logging-datefmt="%Y-%m-%dT%H:%M:%S%Z" \
	    --logging-level=DEBUG \
	    --logging-filter=$(NAME),tests,py.warnings \
	    --with-coverage \
	    --cover-package=$(NAME) \
	    --cover-min-percentage=66 \
	    --no-byte-compile \
	    --with-id \
	    $(TESTS_DIR)

lint: $(NAME) | builddir
	pylint $(NAME) --rcfile=pylint.rc

docs:
	# Interpret warnings as errors
	sphinx-build -nvT -b html $(DOCS_DIR) $(BUILD_DIR)/$(DOCS_DIR)
	# Normal build
	# sphinx-build -b html $(DOCS_DIR) $(BUILD_DIR)/$(DOCS_DIR)

builddir:
	@mkdir -p build

clean:
	@- $(RM) -r build
	@- $(RM) -r dist
	@- find . -name "*.egg-info" | xargs $(RM) -rf
	@- find . -name "*.pyc" | xargs $(RM) -rf
	@- find . -name ".coverage" | xargs $(RM) -rf
	@- find . -name ".mypy_cache" | xargs $(RM) -rf
	@- find . -name "__pycache__" | xargs $(RM) -rf

distclean: clean
