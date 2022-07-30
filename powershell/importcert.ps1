$fileName = $args[0]

Write-Output "installing $fileName as root certificate..."
Import-Certificate -CertStoreLocation cert:\LocalMachine\Root -FilePath "$fileName"
Write-Output "Done"