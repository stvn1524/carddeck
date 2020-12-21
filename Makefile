lint:
	pylint --rcfile=./pylintrc ./carddeck
test:
	pytest tests/ --cov ./carddeck --cov-fail-under 100 --cov-config=./.coveragerc
