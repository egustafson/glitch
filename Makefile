.PHONY: all clean package test

all: clean test

clean:
	rm -rf `find . -type d -name __pycache__`
	rm -f  `find . -name '*.pyc'`
	rm -f  `find . -name '*.pyo'`

test:
	python -m unittest discover -v

package:
	echo "unimplemented"

docker:
	echo "unimplemented"

