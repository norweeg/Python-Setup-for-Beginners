# allow powershell to execute scripts.  executed in child shell intentionally.
& powershell -ExecutionPolicy RemoteSigned -NonInteractive -Command {Set-ExecutionPolicy RemoteSigned -Scope CurrentUser}


$core_count = (Get-WmiObject -class Win32_processor).NumberOfCores
$installer_url = "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Windows-x86_64.exe"
$installer_filename = $installer_url.split('/')[-1]
$install_params = '/S', "/D=`"$HOME\Miniforge3`"", '/InstallationType=JustMe', '/RegisterPython=0', '/AddToPath=1'
$install_pkgs = "jupyterlab-python-file jupyterlab-variableinspector nb_conda_kernels jupyterlab_code_formatter"

# Download and run installer silently
Write-Host "Downloading Miniforge installer..."
Invoke-WebRequest $installer_url -OutFile $installer_filename
Write-Host "Installing Miniforge from $installer_filename"
Start-Process -Wait -FilePath $installer_filename -ArgumentList $install_params
Remove-Item $installer_filename

# Reload Path after install
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User") + ";$HOME\Miniforge3\Scripts"
# Setup shells to be able to use conda, no matter how you launch them
Write-Host "Configuring conda..."
& conda init cmd.exe powershell

# Activate Conda in base environment
(& conda shell.powershell hook) | Out-String | Invoke-Expression

# Configure conda
& conda config --system --append channels defaults
& conda config --system --set channel_priority strict
& conda config --system --set pip_interop_enabled true
Invoke-Expression "& conda config --system --set execute_threads $core_count"
Invoke-Expression "& conda config --system --set verify_threads  $core_count"

# Install the anaconda navigator and start menu shortcuts
Write-Host "Setting up conda environments..."
& conda update --yes --name base --all
& conda install --yes --name base anaconda-navigator console_shortcut powershell_shortcut menuinst

# Create conda environment "anaconda" for Anaconda metapackage install
& conda create --yes --name anaconda anaconda
& conda update --yes --name anaconda --all
Invoke-Expression "& conda install --yes --name anaconda $install_pkgs"
& conda clean --yes --all
