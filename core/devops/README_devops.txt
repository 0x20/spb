How to install & run the continuous deployment script (Mac OS X):

- unzip the SmarterSpaceBrain_empty_<system>.zip in the location where you want the testinstall to be.
  This file contains a VirtualEnv that is pre-populated with a number of files that are should not
  be changed as part of the deployment, such as liquibase.properties and dbconfig.ini.
  These files should be set up to contain data that is valid for their respective environments.
- put the deploy_to_test.sh script somewhere in a directory. It will put temporary files in this
  directory when it runs, so it is best to isolate it into its own directory.
- test the script by running it manually,

Remarks:
- Currently, the script will kill all python processes when it runs. If you have other python
  processes running on your system, they will be killed as well.
- Currently, the zipped VirtualEnv is MacOSX specific; it contains links to mac-specific python
  library locations. A linux-specific VirtualEnv will be provided later.