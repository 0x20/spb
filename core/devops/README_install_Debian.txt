What to install on a vanilla Debian Linux system to be able to run the SPB application:

Prepare the Debian environment: you need to install the following items:
- Java (in order to be able to run Liquibase. If you’re not intending to do that, you can skip installing java. You'll need it if you want to do any development work.)
- unzip and curl: the DevOps script uses unzip and curl. If you’re not intending to use that, you can skip installing unzip and curl. If you're only developing, you won't need this.
- python-dev, libpq-dev: enable PostgreSQL connectivity from python.
- python-pip: install the PIP package management system for python
- python-psycopg2: install the PostgreSQL connectivity package for python
- Virtualenv: install the Virtualenv package for python. If you’re not intending to use that, you can skip installing virtualenv.
Run the following commands, as root, on your Debian machine:
 apt-get install default-jre
 apt-get install unzip
 apt-get install curl
 apt-get install python-dev
 apt-get install libpq-dev
 apt-get install python-pip
 apt-get install python-psycopg2
 pip install virtualenv

Further prepare the environment. 
Run as yourself: 
 mkdir projects
 cd projects
 virtualenv SmarterSpaceBrain
 cd SmarterSpaceBrain
 bin/pip install flask
 bin/pip install psycopg2
 mkdir groundcontrol
 mkdir lib
 cd lib
 mkdir liquibase
 wget http://freefr.dl.sourceforge.net/project/liquibase/Liquibase%20Core/liquibase-3.3.3-bin.zip
 unzip liquibase-3.3.3-bin.zip -d liquibase-3.3.3-bin
 rm liquibase-3.3.3-bin.zip
 wget https://jdbc.postgresql.org/download/postgresql-9.4-1201.jdbc41.jar
 In SmarterSpaceBrain directory, create the following files:`
 1. bin/run_liquibase.sh  (!! make executable)
 #!/bin/sh
 export LIQUIBASE_HOME=./lib/liquibase/liquibase-3.3.3-bin/
 lib/liquibase/liquibase-3.3.3-bin/liquibase --changeLogFile=spb-db-changelog.xml --defaultSchemaName=space_brain update
 2. liquibase.properties  (!! edit to point to correct database server/instance)
driver=org.postgresql.Driver
classpath=lib/liquibase/postgresql-9.4-1201.jdbc41.jar
url=jdbc:postgresql://172.22.32.6:5432/braindb_test?searchpath=space_brain
username=***
password=***
 3. testdata/mockdata.sql
insert into space_brain.user (id, firstname, lastname, city, country, member)
          values (-1, ‘admin’, ‘admin’, 'Gent', 'Belgium', true);




