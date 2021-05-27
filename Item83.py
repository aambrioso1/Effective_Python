"""
Item 83: Use Virtual Environments for Isolated and Reproducible Dependencies
No code

Virtual environments all you to use pip install may different versions of the same package
on the same machine without conflicts.
Virtual environments are basically enabled with activate and disabled with deactivate.
You can use python -m pip freeze to save dependencies and python -m pip install -r requirements.txt
to install dependencies into another environment. 

Commands
Show a description of a package including dependencies
$ python -m pip show package_name

Where is you Python located?
$ which python

Which version of Python are you using?
$ python --version

Check if installation worked
$ python -c 'import pytz'

Create a virtual environment
$ python -m venv yourproject

Activate the environment

Linux
$source bin/activate

Windows
$ .\myproject\scripts\activate

After activation the path to Python command-line tool is moved to with the virtual environment.

The virtual environment will start with only pip and setuptools installed.

To return to the default system use:
# deactivate

Reproducing dependencies

Save all the dependencies of a virtual environment to a file:
$ python -m pip freeze > requirements.txt

Install these requirement into a new virtual environment:

$ python -m pip install -r path_to_requirements.txt







"""
