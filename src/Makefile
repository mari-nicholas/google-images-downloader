TEST_PATH=./Test

test:
	pytest $(TEST_PATH)

install:
	pip3 install -r requirements.txt

lint:
	flake8 --exclude=$(TEST_PATH)/*