TEST_PATH=./Test
DOC = doxygen
DOCFLAGS = 
DOCCONFIG = 

.PHONY: test

test:
	pytest --cov-report term --cov=. $(TEST_PATH)

docs:
	$(DOC) $(DOCFLAGS) $(DOCCONFIG)
	cd latex && $(MAKE)

install:
	pip3 install -r requirements.txt

lint:
	flake8 --per-file-ignores='Input.py,SearchQuery.py:E501' --ignore=E266,N802,N803,N806,N812,W504 --exclude=$(TEST_PATH)/* .

