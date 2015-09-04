Quick Django tutorial.

Installing:

To install Djano, just do:
  PIP install Django

Within the Django folder you find a directory for each module and some files in the main dir. In "manage.py" you can edit the global settings, as well as adding new modules (either own or third party). This is also the script you need to run and has some extra functionalities:

manage.py syncdb	-	syncs the data models with the database. With Django you define data structures inside the framework and sync changes into the database. More about that later, but you use this command when you changed something in the data models.

manage.py runserver	-	Starts the Django framework just as "Brain_API.py" does for Flask.

manage.py startapp	-	Creates a new module (or app) in the main directory. In order to properly add it to the program, add it to manage.py's 'INSTALLED_APPS' list.

Django comes with an admin panel, which can be found at: http://127.0.0.1:8000/admin/
Each module can be added to the panel by creating an admin.py file in the module. Standard it houses user and group management.

------

There are some differences between Flask and Django that make learning Django a bit harder from the start but will be easier to use later on. Luckily we already have some work done in Flask which I ported over to Django.

TODO:
Change user accounts (https://docs.djangoproject.com/en/1.8/ref/contrib/auth/#django.contrib.auth.models.User)
