CORE

- clone the git repository
- in the "spb" directory, run "virtualenv core". 
  This will turn "core" into a virtualenv, to which you can add packages.
- activate the "core" virtualenv:
  source bin/activate
- in "core", install flask and simplejson:
  pip install flask simplejson
- in "core", install psycopg2:
  pip install psycopg2
  if you get a message that it needs a path to pg_config: 
      on MaxOSX:
          run something like this: export PATH="/Applications/Postgres.app/Contents/Versions/9.4/bin:$PATH"
      on Debian:
          sudo apt-get install libpq-dev python-dev
          (source: http://web.archive.org/web/20140615091953/http://goshawknest.wordpress.com/2011/02/16/how-to-install-psycopg2-under-virtualenv/)
- Using ./Brain_API  you should be able to start the core API.

POSTGRESQL

Don’t forget to install PostgreSQL on your PC. Use the properties in liquibase.properties to set up your database (DB name: smarterspacebrain, schema name: smarterspacebrain, role name: smarterspacebrain (pwd spbdev). If you choose different names, make sure to update liquibase.properties accordingly.
      on MacOSX:
          The easiest way is to download Postgres.app from http://www.postgresql.org/download/macosx/
          Alternatively, if you use fink, macports or homebrew, you can use these package managers to install postgresql
      on Debian:
          sudo apt-get install postgresql
          sudo -su postgres psql
            CREATE USER smarterspacebrain WITH PASSWORD 'spbdev';
            CREATE DATABASE smarterspacebrain OWNER smarterspacebrain;
            \c smarterspacebrain
            SET ROLE smarterspacebrain;
            CREATE SCHEMA smarterspacebrain;
            \q
          if you want postgresql to listen on other interfaces that 'localhost', edit
              the file '/etc/postgresql/9.3/main/postgresql.conf'. Locate the line that
              starts with 'listen_addresses' and add the required interface to the list
              for example: listen_addresses = 'localhost,172.22.32.4'
          now edit pg_hba.conf (/etc/postgresql/9.3/main/pg_hba.conf) and insert the line
              "local  smarterspacebrain  smarterspacebrain  password"
              insert it above the line "local all all peer" (!)
              if you want to allow access from another interface, you'll have to add additional lines:
              "host  smarterspacebrain  smarterspacebrain  172.22.32.4/24  password"
          sudo service postgresql restart

In order to update the database, execute:
  bin/run_liquibase.sh

(internally, this runs maven)
