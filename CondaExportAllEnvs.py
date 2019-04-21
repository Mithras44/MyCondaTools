# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 18:48:30 2019

@author: Mithras44
@docstrings: Google

This can export all the conda environments into yaml files. You can run it as a script or from the command line. There are two variables you can change.

### export_folder

You can change the variable to set which folder within the user directory you wish to export the conda yaml files into.

You can also override the variable if running if using command line with --export_folder=/folder/subfolder argument.

### use_date_folders

You can set the boolean to True or False depending on if you want to export the conda yaml files into a sequential folders within today's date folder within the export_folder. This can be useful if you want to periodically run the script to create backups for conda environments.
This means the export folder would be /export_folder/{todays_date}/{sequential_number}/ within the user directory.

You can also override the variable if running if using command line with --use_date_folders=False argument.

Define folder path from command line with command: python CondaExportAllEnvs.py --export_folder=/folder/subfolder --use_date_folders=True
"""

import subprocess
import json
import argparse
from pathlib import Path
from datetime import datetime

export_folder = "/ACproject/MyCondaBackupEnvs"  # Change to desired export folder in user directory my_conda_backup_envs
 
use_date_folders = False # Change to add yaml files into date folders in the export folder


def cmd_export_folder(export_folder=export_folder, use_date_folders=use_date_folders):
    """Takes script default export folder but can be overwritten by argument from command line.

    Args:
        export_folder (str, optional): Folder within user directory to export conda yaml files into. Can be overridden by optional cmd argument --export_folder.
        use_date_folders (bool, optional): Whether to put conda yaml files into today's date folder within export folder. Can be overridden by optional cmd argument --use_date_folders.
    Returns:
        export_folder (str): String of folder (non full path) to export conda env yml files.
        use_date_folders (bool): Boolean for whether to use date folders within export folder.
    """
    cmd_use_date_folders = str(use_date_folders)

    parser = argparse.ArgumentParser(description="""Export all conda
                                      environments into .yml files to
                                      export_folder """)
    parser.add_argument('--export_folder', type=str, default=export_folder,
                        help=f"""folder to export to within user directory
                         (default: {export_folder})""")
    parser.add_argument('--use_date_folders', type=str, default=cmd_use_date_folders,
                        help="""Boolean whether to put yaml files in date folders""")
    args = parser.parse_args()
    export_folder = args.export_folder
    cmd_use_date_folders = args.use_date_folders
    if cmd_use_date_folders == 'True':
        use_date_folders = True
    elif cmd_use_date_folders == 'False':
        use_date_folders = False
    else:
        use_date_folders = use_date_folders
    return export_folder, use_date_folders


def create_export_folder_path(export_folder=export_folder, use_date_folders=use_date_folders):
    """Takes export folder argument and creates folder if it doesn't exist and returns full path.

    Args:
        export_folder (str, optional): Defaults to export_folder. Folder within user directory to export conda yaml files into.
        use_date_folders (bool, optional): Defaults to use_date_folders. True or False on whether to put conda yaml files into today's date folder within export folder.

    Returns:
        export_folder_path (str): Returns full folder path
    """

    print("use_date_folders : " + str(use_date_folders))
    home = Path.home()
    export_folder_list = list(export_folder.split('/'))
    export_folder_path = Path.joinpath(home, *export_folder_list)
    if use_date_folders is False:
        if not Path.exists(export_folder_path):
            Path.mkdir(export_folder_path, mode=0o777, parents=True)
        return export_folder_path

    elif use_date_folders is True:
        today = datetime.today().strftime("%Y-%m-%d")
        today_path = Path.joinpath(export_folder_path, today)

        if not Path.exists(today_path):
            export_folder_path = Path.joinpath(today_path, '01')
            Path.mkdir(export_folder_path, mode=0o777, parents=True)
            return export_folder_path

        elif Path.exists(today_path):
            folder_list = [str(folder.stem)
                           for folder in today_path.iterdir() if folder.is_dir()]
            highest_value = max(folder_list)
            new_highest_value = str(int(highest_value) + 1).zfill(2)
            export_folder_path = Path.joinpath(today_path, new_highest_value)
            Path.mkdir(export_folder_path, mode=0o777, parents=True)
            return export_folder_path


def conda_env_list():
    """Creates a list of all the conda environments.

    Returns:
        env_names_list (list): A list of al the conda environments.
    """

    command_output = subprocess.run(["conda", "env", "list", "--json"],
                                    universal_newlines=True,
                                    stdout=subprocess.PIPE)
    output = json.loads(command_output.stdout)
    output_envs = output['envs'][1:]
    env_names_list = []
    for env in output_envs:
        env = env.replace("\\", "/").split("/")[-1:]
        env_names_list += env
    env_names_list.append("base")
    return env_names_list


def export_envs(env_names_list, export_folder_path):
    """Creates yaml files of conda environments in export folder.

    Args:
        env_names_list (list): List of all the conda to export.
        export_folder_path (str): Full path of where the yaml files should be created.
    """

    print(export_folder_path)
    for env_name in env_names_list:
        command_run = subprocess.run(
            f"conda env export --name {env_name} > {env_name}_conda_env.yml",
            shell=True, universal_newlines=True, stderr=subprocess.PIPE,
            cwd=export_folder_path)
        if command_run.returncode != 0:
            print(env_name + " : " + command_run.stderr)
        else:
            print(env_name + " : done")
    print("Complete")


def main(export_folder=export_folder, use_date_folders=use_date_folders):
    """Main.

    Args:
        export_folder (str, optional): Defaults to export_folder. Folder within user directory to export conda yaml files into.
        use_date_folders (bool, optional): Defaults to use_date_folders. True or False on whether to put conda yaml files into today's date folder within export folder.
    """

    export_folder, use_date_folders = cmd_export_folder(
        export_folder, use_date_folders)
    export_folder_path = create_export_folder_path(
        export_folder, use_date_folders)
    env_names_list = conda_env_list()
    export_envs(env_names_list, export_folder_path)


if __name__ == "__main__":
    main(export_folder)
