.PHONY: help lint test test-with-coverage deploy

help:
	@echo "    lint"
	@echo "        Check code style and formatting."
	@echo "    test"
	@echo "        Run unit tests."
	@echo "    test-with-coverage"
	@echo "        Run test using tox and check coverage."
	@echo "    deploy"
	@echo "        Deploy using serverless."

lint:
	flake8 aws_stripe_etl test

test:
	py.test

test-with-coverage:
	tox

deploy:
	cd stripe_pipeline && serverless deploy
