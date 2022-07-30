$commonName = $args[0]
$outFile = $args[1]

Write-Output "Creating certificate for $commonName..."
$cert = New-SelfSignedCertificate -Subject "CN=$commonName" -DnsName "$commonName" -KeyAlgorithm RSA -KeyLength 2048 -CertStoreLocation "Cert:\LocalMachine\My" -NotBefore 2020-1-1 -NotAfter (Get-Date).AddYears(99)
Write-Output "Writing certificate to $outFile..."
Export-Certificate -Cert $cert -FilePath "$outFile"
Write-Output "Done."