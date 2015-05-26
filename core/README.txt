How to install a dev environment on your PC:

  Apart from python itself, you need some libraries etc. What you need is
  listed in devops/README_install script for Debian

!! I initially used python VirtualEnvs to start development. You don't really need this though. But there are some pieces still left of this in the code. 

Don’t forget to install PostgreSQL on your PC. Use the properties in liquifies.properties to set up your database (DB name: smarterspacebrain, schema name: smarterspacebrain, role name: smarterspacebrain (pwd spbdev). If you choose different names, make sure to update liquibase.properties accordingly.

In order to update the database, execute:
  bin/run_liquibase.sh

(internally, this runs maven)
