# Usage:
#   .\start-vm-and-tunnel.ps1 -Vmx "C:\VMs\DevBox\DevBox.vmx" -User jflana
# Optional:
#   -IdentityFile "C:\Users\John\.ssh\id_rsa"
# Notes:
#   -T ws = Workstation; add -T fusion on macOS, but you're on Windows here.

param(
  [string]$Vmx = "C:\Users\John Flanagan\uwmc-dev_vm\uwmc-dev.vmx",
  [string]$User = "jflana",
  [string]$IdentityFile = ""
)

$vmrun = "C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe"

# Start headless
& $vmrun -T ws start "$Vmx" nogui | Out-Null

# Get IP when Tools is ready
$ip = & $vmrun -T ws getGuestIPAddress "$Vmx" -wait
if (-not $ip) { Write-Error "Could not get guest IP."; exit 1 }
Write-Host "Guest IP: $ip"

# Wait for SSH to actually be listening
$timeoutSec = 120
$stopWatch = [Diagnostics.Stopwatch]::StartNew()
while ($stopWatch.Elapsed.TotalSeconds -lt $timeoutSec) {
  if (Test-NetConnection -ComputerName $ip -Port 22 -InformationLevel Quiet) { break }
  Start-Sleep -Seconds 2
}
if (-not (Test-NetConnection -ComputerName $ip -Port 22 -InformationLevel Quiet)) {
  Write-Error "SSH never came up on $ip:22 within $timeoutSec seconds."
  exit 1
}

# Build your tunnels here. Add/remove to taste.
$ports = @(
  1455,        # Codex callback
  27017,       # MongoDB
  3000,        # MERN dev / SAM local API (watch for conflicts)
  8000,        # DynamoDB Local
  4321,        # SPFx gulp serve
  35729        # LiveReload
)
$tunnelArgs = @()
foreach ($p in $ports) {
  $tunnelArgs += "-L${p}:localhost:${p}"
}

# Safer known_hosts handling: accept-new so the changing IP doesn’t nag you
$sshExe = "ssh"
$commonArgs = @(
  "-o","StrictHostKeyChecking=accept-new",
  "-o","ExitOnForwardFailure=yes",
  "-N"                                   # no remote command; pure tunnels
) + $tunnelArgs

if ($IdentityFile -ne "") {
  $commonArgs = @("-i", $IdentityFile) + $commonArgs
}

Write-Host "Opening SSH tunnels to $User@$ip ..."
# This stays attached; Ctrl+C to close tunnels. If you want it backgrounded, use Start-Process.
& $sshExe @commonArgs "$User@$ip"
