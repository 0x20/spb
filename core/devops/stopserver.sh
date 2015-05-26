#!/bin/bash

#### KILL THE CURRENTLY RUNNING PROCESS
# This command filters the PIDs from PS output ('grep -v grep' filters
# the PID of grep itself) and runs KILL with each PID found
echo Killing currently running python processes...
ps -a | grep 'bin/python ./' | grep -v grep | awk '{print $1;}' | xargs kill