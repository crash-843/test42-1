MANAGE=django-admin.py

test:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=test42.settings $(MANAGE) test homepage

coverage:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=test42.settings coverage run --source='test42.apps.homepage' manage.py test homepage

run:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=test42.settings $(MANAGE) runserver

syncdb:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=test42.settings $(MANAGE) syncdb --noinput
