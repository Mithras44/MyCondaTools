# MyCondaTools
Tools for Conda Environments Anaconda https://www.anaconda.com/ 

Make sure you have the latest version of conda installed: `conda update conda`

## CheckCondaEnv

This is a function you can import into the beginning of a script to make sure you are running it in the right conda environment. Just provide it the name of the environment it should be in and it will raise a warning if it isn’t in the right one. Might need to change the warning messages if it’s run in a corporate organisation.

## CondaExportAllEnvs

This can export all the conda environments into yaml files. You can run it as a script and change the `export_folder` variable to which folder in the user directory you wish to export them into. Alternatively you can run it from the command line where the `export_folder` will be the default export folder but you can override it by providing it with a `--export_folder=/folder/subfolder` argument.
