#!/bin/bash

WORKING_DIR=/home/joris/projects/workdir
TARGET_DIR=/home/joris/projects/SmarterSpaceBrain_test

#### CHECK FOR UPDATES
# We keep the date of the last project activity in a file. If the current
# last activity corresponds to the saved last activity, nothing has changed
# and we can quit the script.
PREVIOUS_LAST_UPDATED_AT=$(cat $TARGET_DIR/lastUpdatedAt)
LAST_UPDATED_AT=$(curl --silent --header "PRIVATE-TOKEN: gKz_xrRMsyKSSzrygDVs" "https://gitlab.com/api/v3/projects/255188" | python -mjson.tool | grep 'last_activity_at' | awk '{print $2;}')
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
#ps aux | grep 'bin/python ./' | grep -v grep | awk '{print $2;}' | xargs kill
pkill python

#### UPDATE THE CODE
echo Downloading and updating the code...
# Download the code archive from GitLab
curl --silent 'https://gitlab.com/jvanloov/SmarterSpaceBrain/repository/archive.zip?private_token=gKz_xrRMsyKSSzrygDVs' > $WORKING_DIR/code.zip 
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
unzip -d $WORKING_DIR -j $WORKING_DIR/code.zip SmarterSpaceBrain.git/*.py SmarterSpaceBrain.git/*.xml SmarterSpaceBrain.git/groundcontrol/*.* > /dev/null
#--- Following line commented out: don't overwrite test config
#unzip -d $WORKING_DIR -j $WORKING_DIR/code.zip SmarterSpaceBrain.git/*.ini SmarterSpaceBrain.git/testdata/*.sql > /dev/null
#---
# Copy the files to the test installation
cp $WORKING_DIR/*.py $TARGET_DIR
cp $WORKING_DIR/*.xml $TARGET_DIR
cp $WORKING_DIR/*.js $TARGET_DIR/groundcontrol
cp $WORKING_DIR/*.css $TARGET_DIR/groundcontrol
cp $WORKING_DIR/*.html $TARGET_DIR/groundcontrol
cp $WORKING_DIR/*.map $TARGET_DIR/groundcontrol
#--- Following lines commented out: don't overwrite test config
#cp $WORKING_DIR/*.ini $TARGET_DIR
#cp $WORKING_DIR/*.sql $TARGET_DIR/testdata/
#---
# Delete the files
rm $WORKING_DIR/*.py $WORKING_DIR/*.xml
rm $WORKING_DIR/*.js $WORKING_DIR/*.css $WORKING_DIR/*.html $WORKING_DIR/*.map
#--- Following lines commented out: don't overwrite test config
# rm $WORKING_DIR/*.ini $WORKING_DIR/*.sql
#---
rm $WORKING_DIR/code.zip

#### UPDATE THE DATABASE
echo Updating the database...
cd $TARGET_DIR
./bin/run_liquibase.sh

#### RESTART THE SERVER
echo Restarting the server...
./Brain_API.py &

echo Done.
