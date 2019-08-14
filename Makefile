NAME := python-whmcs
BUILD_DIR := build
DOCS_DIR := docs
TESTS_DIR := tests


.PHONY: $(NAME) all install install-devel uninstall release check lint docs builddir clean distclean

all: builddir $(NAME)

$(NAME):
	python setup.py \
	    sdist -d $(BUILD_DIR) \
	    bdist -d $(BUILD_DIR) \
	    bdist_wheel -d $(BUILD_DIR) --py-limited-api cp37

install: $(NAME) | builddir uninstall
	find $(BUILD_DIR) -name "$(NAME)*.whl" | xargs pip install

install-devel: $(NAME) | builddir uninstall
	pip install -e .[devel]

uninstall:
	pip uninstall -y $(NAME)

release:
	python setup.py \
	    sdist -d $(BUILD_DIR) \
	    bdist -d $(BUILD_DIR) \
	    bdist_wheel -d $(BUILD_DIR) --py-limited-api cp37 \
	    upload -r beyondhosting

check:
	pytest \
		-rfE \
		--maxfail=10 \
		--show-capture=no \
		--tb=short \
		--cov=pywhmcs \
		--cov-report term-missing:skip-covered \
		$(TESTS_DIR)/

lint: $(NAME) | builddir
	pylint --rcfile=pylint.rc $(NAME)

docs:
	sphinx-build -nvT -b html $(DOCS_DIR) $(BUILD_DIR)/$(DOCS_DIR)

builddir:
	@mkdir -p build

clean:
	@- $(RM) -r $(BUILD)
	@- $(RM) -rf .mypy_cache
	@- $(RM) -rf .coverage
	@- $(RM) -rf .pytest_cache
	@- find . -name "*.pyc" | xargs $(RM) -rf
	@- find . -name "__pycache__" | xargs $(RM) -rf

distclean: clean
