init:
	pip install -r requirements.txt

pkg-test:
	pip install -r requirements.pkg.txt
	python3 -m build
	python3 -m twine upload --repository testpypi dist/*

install-test:
	pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple monosi

