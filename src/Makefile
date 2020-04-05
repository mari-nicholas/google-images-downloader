TEST_PATH=./Test

.PHONY: test

test:
	pytest --cov-report term --cov=. $(TEST_PATH)

install:
	pip3 install -r requirements.txt

lint:
	flake8 --per-file-ignores='Input.py:E501' --ignore=E266,N802,N803,N806,N812 --exclude=$(TEST_PATH)/* .