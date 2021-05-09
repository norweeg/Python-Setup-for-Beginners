# Python Setup for Beginners

Python setup for absolute beginners.  The intension of this repository is to provide a simple script that will setup [Miniforge](https://github.com/conda-forge/miniforge), add the default [Anaconda](https://anaconda.org/) channel as a backup channel to [Conda Forge](https://conda-forge.org/), setup the Anaconda Navigator (conda GUI), and setup a general-usage Python environment equivalent to a base Anaconda installation.

## Requirements

* Windows 10 (64-bit)
* An active Internet Connection

## Usage

1. Download [setup_python_windows.ps1](setup_python_windows.ps1)
2. Right-click [setup_python_windows.ps1](setup_python_windows.ps1) and select "Run with Powershell"
3. When the installer is complete, you will find shortcuts to your Anaconda tools in the start menu

It is recommended that you avoid using `pip install some_package_name` to install additional modules as much as possible as pip is unaware of the existance of the Anaconda package manager, `conda`, and will happily clobber packages installed by `conda`, possibly breaking your environment.  Instead, try searching for the module you wish to install in the Anaconda Navigator, or search for it in the command line using `conda search some_package_name` and install with `conda install some_package_name`

## Resources

* [Conda Documentation](https://docs.conda.io/en/latest/)
* [Conda Cheat Sheet](https://docs.conda.io/projects/conda/en/latest/_downloads/843d9e0198f2a193a3484886fa28163c/conda-cheatsheet.pdf)
* [The Python Standard Library](https://docs.python.org/3/library/)
