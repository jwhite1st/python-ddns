.PHONY: clean clean-build clean-pyc test

clean: clean-build clean-pyc

full-test: lint test

ifeq ($(OS),Windows_NT)
    RM = del //Q //F
    RRM = rmdir //Q //S
else
    RM = rm -f
    RRM = rm -f -r
endif

clean-build:
	$(RM) -r build/
	$(RM) -r dist/
	$(RM) -r *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec $(RM) {} +
	find . -name '*.pyo' -exec $(RM) {} +
	find . -name '*~' -exec $(RM) {} +

build:
	python setup.py sdist bdist_wheel

check-dist:
	pip install twine wheel --quiet
	python setup.py egg_info
	make build
	twine check --strict dist/*

lint:
	black --check pddns
	pylint pddns
	flake8 --statistics --show-source --count pddns
	bandit -r pddns

test:
	py.test --cov pddns tests/ -vv