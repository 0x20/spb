CORE

- clone the git repository
- in the "spb" directory, run "virtualenv core". 
  This will turn "core" into a virtualenv, to which you can add packages.
- activate the "core" virtualenv:
  source bin/activate
- in "core", install flask:
  pip install flask
- in "core", install psycopg2:
  pip install psycopg2
  (if you get a message that it needs a path to pg_config, run something like this (on MacOSX):
   export PATH="/Applications/Postgres.app/Contents/Versions/9.4/bin:$PATH"
   on Debian (Linux) it may be something else. The pg_config program is part of the PostgreSQL install)
- Using ./Brain_API  you should be able to start the core API.

POSTGRESQL

Don’t forget to install PostgreSQL on your PC. Use the properties in liquifies.properties to set up your database (DB name: smarterspacebrain, schema name: smarterspacebrain, role name: smarterspacebrain (pwd spbdev). If you choose different names, make sure to update liquibase.properties accordingly.

In order to update the database, execute:
  bin/run_liquibase.sh

(internally, this runs maven)
