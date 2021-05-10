# allow powershell to execute scripts.  executed in child shell intentionally.
& powershell -ExecutionPolicy RemoteSigned -NonInteractive -Command {Set-ExecutionPolicy RemoteSigned -Scope CurrentUser}

$installer_url = "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Windows-x86_64.exe"
$installer_filename = $installer_url.split('/')[-1]
$install_params = '/S', "/D=`"$HOME\Miniforge3`"", '/InstallationType=JustMe', '/RegisterPython=0', '/AddToPath=1'

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

# Run config and environment setup script
Write-Host "Setting up conda environments"
& python .\scripts\setup_environment.py

# Activate anaconda environment and setup shortcuts to Jupyter, etc.
Write-Host "Installing Shortcuts"
& conda activate anaconda
& python .\scripts\download_icon.py "https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/1767px-Jupyter_logo.svg.png" "$env:_CONDA_ROOT\envs\anaconda\Menu\jupyter.ico"
& python .\scripts\download_icon.py "https://github.com/nteract/nteract/raw/main/applications/desktop/static/icon.png" "$env:_CONDA_ROOT\envs\anaconda\Menu\nteract.ico"
& python .\scripts\download_icon.py "https://raw.githubusercontent.com/jupyterlab/jupyterlab_app/master/dist-resources/icon.svg" "$env:_CONDA_ROOT\envs\anaconda\Menu\jupyter_lab.ico"

Copy-Item -Path ".\shortcuts\Windows\*" -Destination "$env:_CONDA_ROOT\envs\anaconda\Menu\"
& python .\scripts\create_shortcuts.py
Write-Host "Installation and setup complete!"
