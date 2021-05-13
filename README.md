# Python Setup for Beginners

Python setup for absolute beginners.  The intension of this repository is to provide a simple script that will setup [Miniforge](https://github.com/conda-forge/miniforge), add the default [Anaconda](https://anaconda.org/) channel as a backup channel to [Conda Forge](https://conda-forge.org/), setup the Anaconda Navigator (conda GUI), and setup a general-usage Python environment equivalent to a base Anaconda installation.

## Requirements

* Windows 10 (64-bit)
* An active Internet Connection

## Usage

1. Download [setup_python_windows.ps1](setup_python_windows.ps1)
2. Right-click [setup_python_windows.ps1](setup_python_windows.ps1) and select "Run with Powershell"
3. When the installer is complete, you will find shortcuts to your Anaconda tools in the start menu

### Tips for Maintaining Your Python Environments

* Install **NOTHING** additional in the environment named `base`.  `base` should only ever be used to maintain other environments as it contains the `conda` command.  If you break the `base` environment, you will have to uninstall everything and start over
* Treat the environment `anaconda` like an exploritory/learning environment.  It has packages for most anything you could ever want, however, the more you install beyond that, the bigger it gets, which increases the chances that the modules you want to install will conflict with modules you already have.  Either clone this environment with `conda create --clone anaconda --name new_enviornment_name addional_module_to_install another_module_to_install` or, even better, create a whole new environment with just the modules you need with `conda create --name new_environment_name module_to_install another_module_to_intall`
* When you open a command prompt, you will notice that it says `(base)` before the command prompt.  This indicates that the `base` conda environment is active.  To change which environment is active in a command prompt, use `conda activate name_of_your_environment`, after which you will see the name of the environment you just activated before the prompt instead
* The Jupyter application installed in the `anaconda` environment is configured to be able to launch sessions for *any* of your conda environments.  All you need to be able to launch a jupyter session in another conda environment is to install the package `ipykernel` in it with `conda install -n name_of_other_environment ipykernel`.  After which you will see it as an option when you create a new notebook the next time you start Jupyter.
* This setup is based on Anaconda, a Python distribution which uses the `conda` package manager to install python modules rather than the `pip` package manager.  While `pip` is universal to python and able to be used instead of `conda`, it is discouraged.  I recommend that you avoid using `pip install some_package_name` to install additional modules as much as possible as  `pip` is unaware of the existance `conda` and will happily clobber packages installed by `conda`, possibly breaking your environment.  Instead, try searching for the module you wish to install in the Anaconda Navigator, or search for it in the command line using `conda search some_package_name` and install with `conda install some_package_name`.  Use `pip` only as a last resort to install something that isn't able to be installed with conda, preferably after intalling any dependencies for it with `conda` first.  I have not found much was not available using `conda`, so you probably won't ever need `pip` at all!
* To update everything installed in an environment, run `conda update --name your_environment_name --all`.  This will update all modules installed in an environment to the latest version compatible with everything else in your environment.
* See the `conda` documentation and cheat sheet in the resources below for more information about managing environments using `conda`

## Resources

* [Conda Documentation](https://docs.conda.io/en/latest/)
* [Conda Cheat Sheet](https://docs.conda.io/projects/conda/en/latest/_downloads/843d9e0198f2a193a3484886fa28163c/conda-cheatsheet.pdf)
* [The Python Standard Library](https://docs.python.org/3/library/)
