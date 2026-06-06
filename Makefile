.PHONY: test bench clean

PYTHON ?= python3
CORPUS ?= /Users/srini/Brain/raw

test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests

bench:
	PYTHONPATH=src $(PYTHON) -m poscachebench run \
		--corpus "$(CORPUS)" \
		--out results/benchmark.json \
		--csv results/benchmark.csv \
		--report results/report.md \
		--max-docs 40 \
		--chunk-size 96 \
		--budgets 0.10,0.25,0.50

clean:
	rm -f results/benchmark.json results/benchmark.csv results/report.md

