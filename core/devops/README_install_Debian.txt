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
 apt-get install git
 apt-get install python-dev
 apt-get install libpq-dev
 apt-get install python-pip
 pip install virtualenv

Further prepare the environment. 
Run as yourself:
 git clone https://github.com/0x20/spb    # clone the repo to recreate the dir structure locally
 cd spb                                   # go into the newly created dir structure
 virtualenv core                          # make 'core' into a virtual environment
 cd core                                  # enter the virtual environment
 source bin/activate                      # activate the virtual environment
 pip install --upgrade pip                # update to the latest version
 pip install flask
 pip install psycopg2
 pip install simplejson
 pip install apscheduler

Edit the file liquibase.properties to point to your dev database:
 driver=org.postgresql.Driver
 classpath=lib/liquibase/postgresql-9.4-1201.jdbc41.jar
 url=jdbc:postgresql://172.22.32.6:5432/braindb_test?searchpath=space_brain
 username=***
 password=***

Edit the file main.ini if needed

Edit the file devops/deploy_to_test.sh if needed





