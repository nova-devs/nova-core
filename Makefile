.PHONY: environment
build:
	@pip install -r requirements.txt

.PHONY: build-image
image:
	@docker image build -t {{YOUR_REGISTRY}} .

.PHONY: push-image
push:
	@docker image push {{YOUR_REGISTRY}}

.PHONY: migrate
migrate:
	@python manage.py migrate

.PHONY: messages
messages:
	@python manage.py compilemessages

.PHONY: dump-menu
dump-menu:
	@python manage.py dumpdata --indent 2 account.menu > account/fixtures/menu.json \
	 && python manage.py dumpdata --indent 2 account.module > account/fixtures/module.json \
	 && python manage.py dumpdata --indent 2 account.modulemenu > account/fixtures/modulemenu.json

.PHONY: load-menu
load-menu:
	@python manage.py loaddata nova/fixtures/module.yaml \
	 && python manage.py loaddata nova/fixtures/menu.yaml \
	 && python manage.py loaddata nova/fixtures/module_menu.yaml

.PHONY: makemessages
makemessages:
	@python manage.py makemessages --ignore=cache --ignore=venv --locale pt_BR

.PHONY: celery
celery:
	@celery --app=nova worker --loglevel INFO -B
