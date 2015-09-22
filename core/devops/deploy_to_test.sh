#!/bin/bash

WORKING_DIR=/home/spb_test/workdir
TARGET_DIR=/home/spb_test/spb

#### CHECK FOR UPDATES
# We keep the date of the last project activity in a file. If the current
# last activity corresponds to the saved last activity, nothing has changed
# and we can quit the script.
PREVIOUS_LAST_UPDATED_AT=$(cat $TARGET_DIR/lastUpdatedAt)
LAST_UPDATED_AT=$(curl --silent https://api.github.com/repos/0x20/spb | python -mjson.tool | grep 'pushed_at' | awk '{print $2;}')
# Quit if no changes were made to the project
if [ "$LAST_UPDATED_AT" == "$PREVIOUS_LAST_UPDATED_AT" ]; then
  echo No changes.
  exit 1;
fi
# Store for next iteration
echo "$LAST_UPDATED_AT" > $TARGET_DIR/lastUpdatedAt

#### KILL THE CURRENTLY RUNNING PROCESS
# This command filters the PIDs from PS output ('grep -v grep' filters
# the PID of grep itself) and runs KILL with each PID found
echo Killing currently running python processes...
ps aux | grep 'bin/python ./' | grep -v grep | awk '{print $2;}' | xargs kill

#### UPDATE THE CODE
echo Downloading and updating the code...
# Download the code archive from GitLab
curl --silent -L https://github.com/0x20/spb/archive/master.zip > $WORKING_DIR/code.zip 
# Check the size of the downloaded file; if too small, the download
# failed and we should quit. We also remove the "lastUpdatedAt" file
# because this now has the current date in it, which would prevent
# a new download attempt before an actual change was committed.
minimumsize=10000
actualsize=$(wc -c "$WORKING_DIR/code.zip" | awk '{print $1;}')
if [ "$actualsize" -lt "$minimumsize" ]; then
  echo Download failed.
  rm $TARGET_DIR/lastUpdatedAt
  exit 2
fi
# Extract the files we need
unzip -d $WORKING_DIR $WORKING_DIR/code.zip > /dev/null
#--- Following line commented out: don't overwrite test config
#unzip -d $WORKING_DIR -j $WORKING_DIR/code.zip SmarterSpaceBrain.git/*.ini SmarterSpaceBrain.git/testdata/*.sql > /dev/null
#---
# Copy the files to the test installation
cp $WORKING_DIR/spb-master/core/*.py $TARGET_DIR/core/
cp $WORKING_DIR/spb-master/core/app_code/*.py $TARGET_DIR/core/app_code
cp $WORKING_DIR/spb-master/core/app_code/banktransactions/*.py $TARGET_DIR/core/app_code/banktransactions
cp $WORKING_DIR/spb-master/core/app_code/brain/*.py $TARGET_DIR/core/app_code/brain
cp $WORKING_DIR/spb-master/core/app_code/database/*.py $TARGET_DIR/core/app_code/database
cp $WORKING_DIR/spb-master/core/app_code/members/*.py $TARGET_DIR/core/app_code/members
cp $WORKING_DIR/spb-master/core/app_code/ui/*.py $TARGET_DIR/core/app_code/ui
cp $WORKING_DIR/spb-master/core/*.xml $TARGET_DIR/core
cp $WORKING_DIR/spb-master/core/dictionarydata/*.sql $TARGET_DIR/core/dictionarydata
cp $WORKING_DIR/spb-master/core/application_code/*.py $TARGET_DIR/core/application_code
cp $WORKING_DIR/spb-master/groundcontrol/*.js $TARGET_DIR/groundcontrol
cp $WORKING_DIR/spb-master/groundcontrol/*.css $TARGET_DIR/groundcontrol
cp $WORKING_DIR/spb-master/groundcontrol/*.html $TARGET_DIR/groundcontrol
cp $WORKING_DIR/spb-master/groundcontrol/*.map $TARGET_DIR/groundcontrol
#--- Following lines commented out: don't overwrite test config
#cp $WORKING_DIR/spb-master/core/*.ini $TARGET_DIR/core/
#cp $WORKING_DIR/spb-master/core/testdata/*.sql $TARGET_DIR/core/testdata/
#---
# Delete the files
rm -rf $WORKING_DIR/spb-master
#--- Following lines commented out: don't overwrite test config
# rm $WORKING_DIR/*.ini $WORKING_DIR/*.sql
#---
rm $WORKING_DIR/code.zip

#### UPDATE THE DATABASE
echo Updating the database...
cd $TARGET_DIR/core
./bin/run_liquibase.sh

#### RESTART THE SERVER
#echo Restarting the server...
./Brain_API.py > $WORKING_DIR/spb_logs.txt &

echo Done.
