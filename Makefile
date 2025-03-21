.PHONY: init
init:
	pyenv install --skip-existing 3.13.2
	pyenv local dragon-3.13
	pip3 install --upgrade pip
	pip3 install -r requirements.txt

.PHONY: init-local
init-local:
	pyenv install --skip-existing 3.13.2
	pyenv virtualenv 3.13.2 dragon-3.13 || true
	pyenv local dragon-3.13
	pip3 install --upgrade pip
	pip3 install pip-tools setuptools

.PHONY: requirements
requirements: requirements.txt

requirements.txt: pyproject.toml
	pip-compile --upgrade --extra dev --output-file=$@ pyproject.toml --no-strip-extras

.PHONY: deploy
deploy:
	rsync -avz --delete . dragon@192.168.1.38:/home/dragon/code