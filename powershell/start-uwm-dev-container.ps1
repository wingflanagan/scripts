# Starts the uwm-dev container with Codex login persistence and port mapping.
# Usage:  .\start-uwm-dev-container.ps1 [-Image uwm-dev] [-Name uwm-dev]

param(
  [string]$Image = "uwm-dev",
  [string]$Name  = "uwm-dev",
  [switch]$Recreate,
  [switch]$HostNetwork # Note: only works on Linux hosts; Podman/Docker on Windows may not support
)

$ErrorActionPreference = 'Stop'

function Ensure-Dir([string]$Path) {
  if (-not (Test-Path -LiteralPath $Path)) { New-Item -ItemType Directory -Path $Path | Out-Null }
}

$HostHome   = $env:USERPROFILE
$HostCodex  = Join-Path $HostHome '.codex'
Ensure-Dir $HostCodex

# Build volume args (Windows path quoting)
$volHome  = ('{0}:/mnt/home:rw' -f $HostHome)
$volCodex = ('{0}:/home/jflana/.codex:rw' -f $HostCodex)

# If container exists, start/attach; else run new container
$exists = $false
& podman container exists $Name | Out-Null
if ($LASTEXITCODE -eq 0) { $exists = $true }
if ($exists) {
  if ($Recreate) {
    Write-Host "Removing existing container '$Name' ..."
    & podman rm -f $Name | Out-Null
  } else {
    Write-Host "Starting existing container '$Name' ..."
    & podman start -ai $Name
    exit $LASTEXITCODE
  }
}

Write-Host "Creating and starting container '$Name' from image '$Image' ..."
$netArgs = @()
if ($HostNetwork) { $netArgs = @('--network','host') }
& podman run -it `
  --name $Name `
  @netArgs `
  $(if (-not $HostNetwork) { '-p 1455:1455' }) `
  -v $volHome `
  -v $volCodex `
  $Image bash

exit $LASTEXITCODE
