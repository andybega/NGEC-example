# PowerShell script to reset the environment
$ErrorActionPreference = "Stop"

Remove-Item -Path "uv.lock" -Force -ErrorAction SilentlyContinue
Remove-Item -Path ".venv" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path ".python-version" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "pyproject.toml" -Force -ErrorAction SilentlyContinue
