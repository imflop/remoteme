PROJECT_NAME ?= mamps

all:
	@echo "make devenv		- Создаём и устанавливаем виртуальное окружение для разработки"
	@echo "make test		- Запуск тестов"
	@exit 0

devenv:
	rm -rf .venv
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

test:
	.venv/bin/pytest