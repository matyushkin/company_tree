# company-tree

Simple tree for some big company with five levels of departments structure. Tree is based in Django with [django-mptt](https://django-mptt.readthedocs.io/en/latest/) library. A special Python script has been written to populate the database. Regarding the structure of the company, a general case is assumed: the same employee can work in several departments, while there can be several employees at each level. Since the database works with a very large number of records, in order to avoid excessive use of browser memory, employee data is not loaded immediately, but asynchronously - when the corresponding department block is opened. For communication between the server part and the frontend, web socket technology is used.

To start up:

`docker-compose -f local.yml build`

`docker-compose -f local.yml up`
s
To create django super user:

`docker-compose -f local.yml run --rm django python manage.py createsuperuser`

To populate database:

`docker-compose -f local.yml run --rm django python manage.py runscript generator`
