.PHONY: install test run clean

install:
	pip install -r requirements.txt
	python -m pip install -e .

test:
	python -m pytest tests/ -v

run-simulate:
	python -m simulator.main --simulate --target /tmp/ransom_sim_test

run-dry:
	python -m simulator.main --target /tmp/ransom_sim_test

run-full-test:
	mkdir -p /tmp/ransom_sim_test
	echo "test content" > /tmp/ransom_sim_test/test.txt
	python -m simulator.main --simulate --target /tmp/ransom_sim_test

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf reports/*.json reports/*.txt
	rm -rf /tmp/ransom_sim_backup_*
