
PYTHON = python3
MAIN = main.py

run:
	$(PYTHON) $(MAIN) config.txt

debug:
	$(PYTHON) -m pdb $(MAIN)

install:
    pip install -r requirements.txt

lint:
	flake8 . --exclude=venv,__pycache__,build,dist,*.egg-info
	mypy . --exclude '(^|/)\venv(/|$$)'

lint-strict:
	flake8 . --exclude=venv,__pycache__,build,dist,*.egg-info
	mypy . --exclude '(^|/)\venv(/|$$)' --strict

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +

.PHONY: run debug install lint lint-strict clean