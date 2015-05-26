#!/bin/sh
export LIQUIBASE_HOME=./lib/liquibase/liquibase-3.3.3-bin/
lib/liquibase/liquibase-3.3.3-bin/liquibase --changeLogFile=spb-db-changelog.xml --defaultSchemaName=smarterspacebrain update