# MyCondaTools

Tools for Conda Environments Anaconda <https://www.anaconda.com/>

Make sure you have the latest version of conda installed: `conda update conda`

## CheckCondaEnv

This is a function you can import into the beginning of a script to make sure you are running it in the right conda environment. Just provide it the name of the environment it should be in and it will raise a warning if it is not in the right one. Might need to change the warning messages if it is run in a corporate organisation.

## CondaExportAllEnvs

This can export all the conda environments into yaml files. You can run it as a script or from the command line. There are two variables you can change.

To use from command line you can use the command line change the working directory to MyCondaTools and input: `python CondaExportAllEnvs.py` . You also have the option of adding two arguments to override the default varialbes:

### export_folder

You can change the variable to set which folder within the user directory you wish to export the conda yaml files into.

You can also override the variable if running if using command line with `--export_folder=/folder/subfolder` argument.

### use_date_folders

You can set the boolean to True or False depending on if you want to export the conda yaml files into a sequential folders within today's date folder within the export_folder. This can be useful if you want to periodically run the script to create backups for conda environments.
This means the export folder would be `/export_folder/{today's_date}/{sequential_number}/` within the user directory.

You can also override the variable if running if using command line with `--use_date_folders=False` argument.
