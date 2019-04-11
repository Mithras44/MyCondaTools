

def check_conda_env(expected_env: str):
    """Checks that the expected conda environment is the same as the current
     conda environment

    Args:
        expected_env (str): What the conda env should be for this python
         script.
    """

    import subprocess
    import warnings
    import json
    command_output = subprocess.run(["conda", "info", "--json"],
                                    universal_newlines=True,
                                    stdout=subprocess.PIPE)
    curent_env = json.loads(command_output.stdout)['active_prefix_name']
    if expected_env == curent_env:
        print(f"""It's all ok, we're using the right conda environment:
             {expected_env}""")
    if expected_env != curent_env:
        warning_message = f"""Oh no, the conda environment you want is:
             {expected_env} but the current environment is: {curent_env}"""
        print(warning_message)
        warnings.warn(warning_message, Warning, stacklevel=2)
