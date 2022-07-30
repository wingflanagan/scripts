<#
.SYNOPSIS
Executes a ScriptBlock in a new elevated instance of powershell, using `gsudo`.

.DESCRIPTION
Serializes a scriptblock and executes it in an elevated powershell. 
The ScriptBlock runs in a different process, so it can´t read/write variables from the invoking scope.
If you reference a variable in a scriptblock using the `$using:variableName` it will be replaced with it´s serialized value.
The elevated command can accept input from the pipeline with $Input. It will be serialized, so size matters.
The script result is serialized, sent back to the non-elevated instance, and returned.
Optionally you can check for "$LastExitCode -eq 999" to find out if gsudo failed to elevate (UAC popup cancelled) 

.PARAMETER ScriptBlock
Specifies a ScriptBlock that will be run in an elevated PowerShell instance. '
e.g. { Get-Process Notepad }

.PARAMETER ArgumentList
An list of elements that will be accesible inside the script as: $args

.PARAMETER NoElevate
A test mode where the command is executed out-of-scope but without real elevation: The serialization/marshalling is still done.

.INPUTS
You can pipe any object to Invoke-Gsudo. It will be serialized and available in the userScript as $Input.

.OUTPUTS
Whatever the scriptblock returns. Use explicit "return" in your scriptblock. 

.EXAMPLE
PS> Get-Process notepad | Invoke-gsudo { Stop-Process }

PS> Invoke-gsudo { return Get-Content 'C:\My Secret Folder\My Secret.txt'}

PS> $a=1; $b = Invoke-gsudo { $using:a+10 }; Write-Host "Sum returned: $b";
Sum returned: 11

.LINK
https://github.com/gerardog/gsudo

    #>
[CmdletBinding(DefaultParameterSetName = 'None')]
param
(
    # The script block to execute in an elevated context.
    [Parameter(Mandatory = $true, Position = 0)]
    [System.Management.Automation.ScriptBlock]
    $ScriptBlock,

    # Optional argument list for the program or the script block.
    [Parameter(Mandatory = $false, Position = 1)]
    [System.Object[]]
    $ArgumentList,

    [Parameter(ValueFromPipeline)]
    [pscustomobject]
    $InputObject,

	[Parameter()]
	[switch]
	$LoadProfile = $false,
	
	#test mode
	[Parameter()]
	[switch]
	$NoElevate = $false
)

# Replaces $using:variableName with the serialized value of $variableName.
# Credit: https://stackoverflow.com/a/60583163/97471
Function Serialize-Scriptblock
{ 	
    param(
        [scriptblock]$Scriptblock
    )
    $rxp = '(?<!`)\$using:(?<var>\w+)'
    $ssb = $Scriptblock.ToString()
    $cb = {
        $v = (Get-Variable -Name $args[0].Groups['var'] -ValueOnly)
		if ($v -eq $null)
		{ '$null' }
		else 
		{ 
			"`$([System.Management.Automation.PSSerializer]::Deserialize([System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('{0}'))))" -f [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes([System.Management.Automation.PSSerializer]::Serialize($v)))
		}		
    }
    $sb = [RegEx]::Replace($ssb, $rxp, $cb, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase);
	return $sb;
}

Function Deserialize-Scriptblock
{
    param(
		[string]$sb
    )
    [Scriptblock]::Create($sb).GetNewClosure()
}

$expectingInput = $myInvocation.expectingInput;
$debug = if ($PSBoundParameters['Debug']) {$true} else {$false};
$userScriptBlock = Serialize-Scriptblock $ScriptBlock
$InputArray = $Input
$location = (Get-Location).Path;

if($PSBoundParameters["ErrorAction"]) {
	#Write-Verbose -verbose "Received ErrorAction $($PSBoundParameters["ErrorAction"])"
	$errorAction = $PSBoundParameters["ErrorAction"] | Out-String
} else {
	#Write-Verbose -verbose "ErrorActionPreference is $ErrorActionPreference"
	$errorAction = $ErrorActionPreference | Out-String
}

$remoteCmd = Serialize-Scriptblock {
	$InputObject = $using:InputArray;
	$argumentList = $using:ArgumentList;
	$expectingInput = $using:expectingInput;
	$sb = [Scriptblock]::Create($using:userScriptBlock);
	Set-Location $using:location;
	$ErrorActionPreference=$using:errorAction;

	if ($expectingInput) { 
		try { 
			($InputObject | Invoke-Command $sb -ArgumentList $argumentList)
		} catch {throw $_} 
	} else { 
		try{
			(Invoke-Command $sb -ArgumentList $argumentList)
		} catch {throw $_} 
	} 
}

if ($Debug) {
	Write-Debug "User ScriptBlock : $userScriptBlock"
	Write-Debug "Full Script to run on the isolated instance: { $remoteCmd }" 
} 

if($NoElevate) { 
	# We could invoke using Invoke-Command:
	#		$result = $InputObject | Invoke-Command (Deserialize-Scriptblock $remoteCmd) -ArgumentList $ArgumentList
	# Or run in a Job to ensure same variable isolation:

	$job = Start-Job -ScriptBlock (Deserialize-Scriptblock $remoteCmd) -errorAction $errorAction | Wait-Job; 
	$result = Receive-Job $job -errorAction $errorAction
} else {
	$pwsh = ("""$([System.Diagnostics.Process]::GetCurrentProcess().MainModule.FileName)""") # Get same running powershell EXE.
	
	if ($host.Name -notmatch 'consolehost') { # Workaround for PowerShell ISE, or PS hosted inside other process
		if ($PSVersionTable.PSVersion.Major -le 5) 
			{ $pwsh = "powershell.exe" } 
		else 
			{ $pwsh = "pwsh.exe" }
	} 
	
	$windowTitle = $host.ui.RawUI.WindowTitle;

	$dbg = if ($debug) {"--debug "} else {" "}
	$NoProfile = if ($gsudoLoadProfile -or $LoadProfile) {""} else {"-NoProfile "}
	
	$arguments = "-d $dbg--LogLevel Error $pwsh -nologo $NoProfile-NonInteractive -OutputFormat Xml -InputFormat Text -encodedCommand IAAoACQAaQBuAHAAdQB0ACAAfAAgAE8AdQB0AC0AUwB0AHIAaQBuAGcAKQAgAHwAIABpAGUAeAAgAA==".Split(" ")

	# Must Read: https://stackoverflow.com/questions/68136128/how-do-i-call-the-powershell-cli-robustly-with-respect-to-character-encoding-i?noredirect=1&lq=1
	$result = $remoteCmd | & gsudo.exe $arguments *>&1
	
	$host.ui.RawUI.WindowTitle = $windowTitle;
}

ForEach ($item in $result)
{
	if (
	$item.Exception.SerializedRemoteException.WasThrownFromThrowStatement -or
	$item.Exception.WasThrownFromThrowStatement
	)
	{
		throw $item
	}
	if ($item -is [System.Management.Automation.ErrorRecord])
	{ 
		Write-Error $item
	}
	else 
	{ 
		Write-Output $item; 
	}
}

# SIG # Begin signature block
# MIIk+gYJKoZIhvcNAQcCoIIk6zCCJOcCAQExDzANBglghkgBZQMEAgEFADB5Bgor
# BgEEAYI3AgEEoGswaTA0BgorBgEEAYI3AgEeMCYCAwEAAAQQH8w7YFlLCE63JNLG
# KX7zUQIBAAIBAAIBAAIBAAIBADAxMA0GCWCGSAFlAwQCAQUABCAz7JjDLkVzlIX8
# hWn4IEadUf8iyqJkJ568HsjAC2ttOqCCCfMwggTeMIIDxqADAgECAhBrMmoPAyjT
# eh1TC/0jvUjiMA0GCSqGSIb3DQEBCwUAMH4xCzAJBgNVBAYTAlBMMSIwIAYDVQQK
# ExlVbml6ZXRvIFRlY2hub2xvZ2llcyBTLkEuMScwJQYDVQQLEx5DZXJ0dW0gQ2Vy
# dGlmaWNhdGlvbiBBdXRob3JpdHkxIjAgBgNVBAMTGUNlcnR1bSBUcnVzdGVkIE5l
# dHdvcmsgQ0EwHhcNMTUxMDI5MTEzMDI5WhcNMjcwNjA5MTEzMDI5WjCBgDELMAkG
# A1UEBhMCUEwxIjAgBgNVBAoMGVVuaXpldG8gVGVjaG5vbG9naWVzIFMuQS4xJzAl
# BgNVBAsMHkNlcnR1bSBDZXJ0aWZpY2F0aW9uIEF1dGhvcml0eTEkMCIGA1UEAwwb
# Q2VydHVtIENvZGUgU2lnbmluZyBDQSBTSEEyMIIBIjANBgkqhkiG9w0BAQEFAAOC
# AQ8AMIIBCgKCAQEAt9uo2MjjvNrag7q5v9bVV1NBt0C6FwxEldTpZjt/tL6Qo5QJ
# pa0hIBeARrRDJj6OSxpk7A5AMkP8gp//Si3qlN1aETaLYe/sFtRJA9jnXcNlW/JO
# CyvDwVP6QC3CqzMkBYFwfsiHTJ/RgMIYew4UvU4DQ8soSLAt5jbfGz2Lw4ydN57h
# BtclUN95Pdq3X+tGvnYoNrgCAEYD0DQbeLQox1HHyJU/bo2JGNxJ8cIPGvSBgcdt
# 1AR3xSGjLlP5d8/cqZvDweXVZy8xvMDCaJxKluUf8fNINQ725LHF74eAOuKADDSd
# +hRkceQcoaqyzwCn4zdy+UCtniiVAg3OkONbxQIDAQABo4IBUzCCAU8wDwYDVR0T
# AQH/BAUwAwEB/zAdBgNVHQ4EFgQUwHu0yLduVqcJSJr4ck/X1yQsNj4wHwYDVR0j
# BBgwFoAUCHbNywf/JPbFze27kLzihDdGdfcwDgYDVR0PAQH/BAQDAgEGMBMGA1Ud
# JQQMMAoGCCsGAQUFBwMDMC8GA1UdHwQoMCYwJKAioCCGHmh0dHA6Ly9jcmwuY2Vy
# dHVtLnBsL2N0bmNhLmNybDBrBggrBgEFBQcBAQRfMF0wKAYIKwYBBQUHMAGGHGh0
# dHA6Ly9zdWJjYS5vY3NwLWNlcnR1bS5jb20wMQYIKwYBBQUHMAKGJWh0dHA6Ly9y
# ZXBvc2l0b3J5LmNlcnR1bS5wbC9jdG5jYS5jZXIwOQYDVR0gBDIwMDAuBgRVHSAA
# MCYwJAYIKwYBBQUHAgEWGGh0dHA6Ly93d3cuY2VydHVtLnBsL0NQUzANBgkqhkiG
# 9w0BAQsFAAOCAQEAquU/dlQCTHAOKak5lgYPMbcL8aaLUvsQj09CW4y9MSMBZp3o
# KaFNw1D69/hFDh2C1/z+pjIEc/1x7MyID6OSCMWBWAL9C2k7zbg/ST3QjRwTFGgu
# mw2arbAZ4p7SfDl3iG8j/XuE/ERttbprcJJVbJSx2Df9qVkdtGOy3BPNeI4lNcGa
# jzeELtRFzOP1zI1zqOM6beeVlHBXkVC2be9zck8vAodg4uoioe0+/dGLZo0ucm1P
# xl017pOomNJnaunaGc0Cg/l0/F96GAQoHt0iMzt2bEcFXdVS/g66dvODEMduMF+n
# YMf6dCcxmyiD7SGKG/EjUoTtlbytOqWjQgGdvDCCBQ0wggP1oAMCAQICEDJcbDIm
# CXB3pEFdnhPyvOMwDQYJKoZIhvcNAQELBQAwgYAxCzAJBgNVBAYTAlBMMSIwIAYD
# VQQKDBlVbml6ZXRvIFRlY2hub2xvZ2llcyBTLkEuMScwJQYDVQQLDB5DZXJ0dW0g
# Q2VydGlmaWNhdGlvbiBBdXRob3JpdHkxJDAiBgNVBAMMG0NlcnR1bSBDb2RlIFNp
# Z25pbmcgQ0EgU0hBMjAeFw0yMTA0MTkwOTE3NDFaFw0yMjA0MTkwOTE3NDFaMHYx
# CzAJBgNVBAYTAkFSMRUwEwYDVQQHDAxCdWVub3MgQWlyZXMxHjAcBgNVBAoMFU9w
# ZW4gU291cmNlIERldmVsb3BlcjEwMC4GA1UEAwwnT3BlbiBTb3VyY2UgRGV2ZWxv
# cGVyLCBHZXJhcmRvIEdyaWdub2xpMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB
# CgKCAQEA/UruzLY61/fw2msZLO8ezkgQx12hKNwbN0btnEvsSopnQt8h/pGXLPiR
# bZeVAhj1zLOtd2yMwOzZ9ExUDNxLu0sSLXlj202sGg9bOZku8wkx+rPlFHzCN8x/
# zZ95tAf2YvLrLSLDh2C7Gs1Etyh3jG2sfFtMvc59AFhnD06ACL+7yXO/XqSq0uzT
# 4rsYwoNCQLx/T1xN/bhhMGHKKa7AnEq1ACiiwMAjy9VYVL8luOdLw9SLomUb4oEF
# Dn4LLi2CdAUI+nBrT4MI+cL1mk6yNAPow7GJwdw0t7jmk6wvZmrseaOWArJjyGGC
# BshnXrdPP0UW7Wy1RrmRGhLgLPRqEwIDAQABo4IBijCCAYYwDAYDVR0TAQH/BAIw
# ADAyBgNVHR8EKzApMCegJaAjhiFodHRwOi8vY3JsLmNlcnR1bS5wbC9jc2Nhc2hh
# Mi5jcmwwcQYIKwYBBQUHAQEEZTBjMCsGCCsGAQUFBzABhh9odHRwOi8vY3NjYXNo
# YTIub2NzcC1jZXJ0dW0uY29tMDQGCCsGAQUFBzAChihodHRwOi8vcmVwb3NpdG9y
# eS5jZXJ0dW0ucGwvY3NjYXNoYTIuY2VyMB8GA1UdIwQYMBaAFMB7tMi3blanCUia
# +HJP19ckLDY+MB0GA1UdDgQWBBRTRkQ7CWslQRbJtXHr+lSAzTHL6TAdBgNVHRIE
# FjAUgRJjc2Nhc2hhMkBjZXJ0dW0ucGwwSwYDVR0gBEQwQjAIBgZngQwBBAEwNgYL
# KoRoAYb2dwIFAQQwJzAlBggrBgEFBQcCARYZaHR0cHM6Ly93d3cuY2VydHVtLnBs
# L0NQUzATBgNVHSUEDDAKBggrBgEFBQcDAzAOBgNVHQ8BAf8EBAMCB4AwDQYJKoZI
# hvcNAQELBQADggEBAFpj51kCRxCLSNb4k3QFTAg6ZYl64/RGA6oDTwEvgicdpsqv
# 1hXtukw7+j6LWElyjqMbftbdCiAEB5HTRckE+MG6nC+bOFAJyLu/gQCKl7bCLXYO
# fUSypFX9o2T7gIZCFSO3OSvqw1uHCZvRTO80bO4FuO0+n3c1ftTJ+SwtJ1XeAQ53
# 8BbSKNR0AUegAyt7ylEUuo8/AS8Gl4RBD8gNbHgza74AYwh/qElrnxtlsGFU1GJe
# NJo1XshiwbllKDhLqAuaJWF09dde2f+LUteof/wj3qlNe9XKY9LghVShcddj4l9v
# uTjHDkRfDXQKX1qNYdxLqerpM/1vvnBCcoRa5w0xghpdMIIaWQIBATCBlTCBgDEL
# MAkGA1UEBhMCUEwxIjAgBgNVBAoMGVVuaXpldG8gVGVjaG5vbG9naWVzIFMuQS4x
# JzAlBgNVBAsMHkNlcnR1bSBDZXJ0aWZpY2F0aW9uIEF1dGhvcml0eTEkMCIGA1UE
# AwwbQ2VydHVtIENvZGUgU2lnbmluZyBDQSBTSEEyAhAyXGwyJglwd6RBXZ4T8rzj
# MA0GCWCGSAFlAwQCAQUAoHwwEAYKKwYBBAGCNwIBDDECMAAwGQYJKoZIhvcNAQkD
# MQwGCisGAQQBgjcCAQQwHAYKKwYBBAGCNwIBCzEOMAwGCisGAQQBgjcCARUwLwYJ
# KoZIhvcNAQkEMSIEIKbRYfAOpQj2dsAW0md1H8dVs1w6FXo3/hOuf5bMzbFYMA0G
# CSqGSIb3DQEBAQUABIIBAAblYwSGCsePGIcvwO99wa1VV2SETtgcbTcludnh7zYL
# CcBl2k1b8QmwYeiqmfy1IgPMYHvgxLyufvrf3bI9qT+uVeNL9p97TZeLtRz63bik
# DTdQzumB9MbWxRYb4mibTsWD5UhZonOTrI2jQBTKufni5E73l0HzOY9qPfCTdOFb
# +y81zYyADTpIKwH1y4xFEI+OtXnR5Y8hcxOb90ERaptEQUOQVyFQEODBXgcb81Bt
# SKKVWSilXvIL0tQF1ND2Q16KZ2ar2nKgtpY/wnkYUndFLtVDPYoDNtOf0UhzTxxn
# 9GylQ6KMZvSkCQmKBVL2yjP6lBVVP70/vP1vaVe9eHChghgaMIIYFgYKKwYBBAGC
# NwMDATGCGAYwghgCBgkqhkiG9w0BBwKgghfzMIIX7wIBAzENMAsGCWCGSAFlAwQC
# AjCBvgYLKoZIhvcNAQkQAQSgga4EgaswgagCAQEGCyqEaAGG9ncCBQELMCEwCQYF
# Kw4DAhoFAAQUCjNByWSVfLMSicZ5keLu0fXVfPICBwqofA+YLR0YDzIwMjIwMzI1
# MTI0MDI5WjADAgEBoFSkUjBQMQswCQYDVQQGEwJQTDEhMB8GA1UECgwYQXNzZWNv
# IERhdGEgU3lzdGVtcyBTLkEuMR4wHAYDVQQDDBVDZXJ0dW0gVGltZXN0YW1wIDIw
# MjGgghMjMIIGlTCCBH2gAwIBAgIRAPFkJYwJtuJ74g4yYI5L9KgwDQYJKoZIhvcN
# AQEMBQAwVjELMAkGA1UEBhMCUEwxITAfBgNVBAoTGEFzc2VjbyBEYXRhIFN5c3Rl
# bXMgUy5BLjEkMCIGA1UEAxMbQ2VydHVtIFRpbWVzdGFtcGluZyAyMDIxIENBMB4X
# DTIxMDUxOTA1NDI0NloXDTMyMDUxODA1NDI0NlowUDELMAkGA1UEBhMCUEwxITAf
# BgNVBAoMGEFzc2VjbyBEYXRhIFN5c3RlbXMgUy5BLjEeMBwGA1UEAwwVQ2VydHVt
# IFRpbWVzdGFtcCAyMDIxMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA
# 1WG+gAC93YRj7hJlmB14VItG+saRFhq6PR58vjQY9ui/eIJiPJDjVWHbtgs/QX7Z
# Isr5OPtzBQ65KL2WUPFg3Jhl5bV+MQMDwHI1xG14BGdHsRD+QHtm5MCpU4slFwmq
# tA/SRGiubeCqu6x+653SneZF+ygEXDBVhDfopFdXIBpSoKpiUk5NAb24G3Ou6KJS
# IbaIXBJLWWRbreVScUydTirEUdxVJjfuEKwJNESL+HcNmeLFopam3QWgUv+Yai7e
# fLKbYjkZMZ4o6991Z74iz9vsG1skDOZPwIKyo/JZOgOQvFf3UoY+pf06qkTMpBgC
# jpougnLxm1A4mzypI5cZQC3eJhyxbo1qBPdRonClCn1ZC7BaqZW/3Tz10I8Nkwpm
# WwHoA0JbAKaZ3YvVFGcR7z3K8sstBModcuBp+179bxMJ8AYrGYwe9jMvJM1ENII8
# T9ur4QZLxdgonNep1QB8chjj5tGNL+5RZnEsmFVoNSeemGW/kACWQi+wSfQgUiaQ
# FzRsXDVETdG2gAZWUx5922wTzgYTkmPb2xsC9+JzpkxaURuZj+h0FV3PxDvXI/Oe
# mvWrngxss9oXJTCGYoxhGua8GnBrT8NR81qYDQDiNuAoQwUUPGJg9tyDda5i5cwj
# LEWfcBWCLzQ7TCVTEkIAtPl0ARTznuvZD8MYDzTeAgsCAwEAAaOCAWIwggFeMAwG
# A1UdEwEB/wQCMAAwHQYDVR0OBBYEFMVHEk5yV7ZEFGuIcRoUrDG5P7oIMB8GA1Ud
# IwQYMBaAFL5UAi+/QGxzQ86sCSVOnkNEGu7gMA4GA1UdDwEB/wQEAwIHgDAWBgNV
# HSUBAf8EDDAKBggrBgEFBQcDCDAzBgNVHR8ELDAqMCigJqAkhiJodHRwOi8vY3Js
# LmNlcnR1bS5wbC9jdHNjYTIwMjEuY3JsMG8GCCsGAQUFBwEBBGMwYTAoBggrBgEF
# BQcwAYYcaHR0cDovL3N1YmNhLm9jc3AtY2VydHVtLmNvbTA1BggrBgEFBQcwAoYp
# aHR0cDovL3JlcG9zaXRvcnkuY2VydHVtLnBsL2N0c2NhMjAyMS5jZXIwQAYDVR0g
# BDkwNzA1BgsqhGgBhvZ3AgUBCzAmMCQGCCsGAQUFBwIBFhhodHRwOi8vd3d3LmNl
# cnR1bS5wbC9DUFMwDQYJKoZIhvcNAQEMBQADggIBADdzzDC3wl+J5qp0rB1Nq2YR
# P3ZKq3UmC7yN1PYuPYcbPovvaKOZiZeLqzy2SdMSM+gewhxQTVvXRcIGoZxTF4k+
# 0Jz7meQgMHy//Qn7AC913Z0tAFpZfuyEqJkaPHedW36Rx7dz948fQuiJodQO9yUq
# fdAqtDaj6pxH5a1cWF/rGGtkjvbxrETGLIVO7sxNVeXGFlqBVDGgx6cELh+AzV4m
# Tug+3/EBlp1zR17ukt0pWmAxuGKMe0iFtbUL9I7JJhdb3TX6MVQMpkBkXTS7BswF
# 5+jjwFIsNcUOjNaqYyuFJyk1IhSX74A1209XL62LCa8mwf+NbKPg7ALdMoysW6Uu
# Yj+0qcch7J3IdFXCOeLCH9Cuun+CyRqHAaQ0ym1NQDqtzrx21aiO1cKrPkxgru0y
# qq0y9jUE0QwMR5LKOxbR/ONUdgNpb2EhQ3xsfOwdTbz1mFN5mPxkbJkMfkYAPD5f
# +zb6e2QGPgFPJg1a9il6xT+Lp6bMFQUJR8bSDsc+o3sn3SyBtqBSZZd4qXAEh2r/
# 6G2BLfxdRkZSfphSELSg2ncVAZn4UZYCIGLxBLbiRhER7sXzA9uoy5osbvEkzxkU
# XKPkeQXYLvqhW58pin7lzuLEfeiWKmjjsYpXDf8a+5rNd4ku8KgDaXdrcSmYz8t8
# HVp4lUHLi+8glw9rhHNtMIIGuTCCBKGgAwIBAgIRAOf/acc7Nc5LkSbYdHxopYcw
# DQYJKoZIhvcNAQEMBQAwgYAxCzAJBgNVBAYTAlBMMSIwIAYDVQQKExlVbml6ZXRv
# IFRlY2hub2xvZ2llcyBTLkEuMScwJQYDVQQLEx5DZXJ0dW0gQ2VydGlmaWNhdGlv
# biBBdXRob3JpdHkxJDAiBgNVBAMTG0NlcnR1bSBUcnVzdGVkIE5ldHdvcmsgQ0Eg
# MjAeFw0yMTA1MTkwNTMyMDdaFw0zNjA1MTgwNTMyMDdaMFYxCzAJBgNVBAYTAlBM
# MSEwHwYDVQQKExhBc3NlY28gRGF0YSBTeXN0ZW1zIFMuQS4xJDAiBgNVBAMTG0Nl
# cnR1bSBUaW1lc3RhbXBpbmcgMjAyMSBDQTCCAiIwDQYJKoZIhvcNAQEBBQADggIP
# ADCCAgoCggIBAOkSHwQ17bldesWmlUG+imV/TnfRbSV102aO2/hhKH9/t4NAoVoi
# pzu0ePujH67y8iwlmWuhqRR4xLeLdPxolEL55CzgUXQaq+Qzr5Zk7ySbNl/GZloF
# iYwuzwWS2AVgLPLCZd5DV8QTF+V57Y6lsdWTrrl5dEeMfsxhkjM2eOXabwfLy6UH
# 2ZHzAv9bS/SmMo1PobSx+vHWST7c4aiwVRvvJY2dWRYpTipLEu/XqQnqhUngFJtn
# jExqTokt4HyzOsr2/AYOm8YOcoJQxgvc26+LAfXHiBkbQkBdTfHak4DP3UlYolIC
# ZHL+XSzSXlsRgqiWD4MypWGU4A13xiHmaRBZowS8FET+QAbMiqBaHDM3Y6wohW07
# yZ/mw9ZKu/KmVIAEBhrXesxifPB+DTyeWNkeCGq4IlgJr/Ecr1px6/1QPtj66yvX
# l3uauzPPGEXUk6vUym6nZyE1IGXI45uGVI7XqvCt99WuD9LNop9Kd1LmzBGGvxuc
# Oo0lj1M3IRi8FimAX3krunSDguC5HgD75nWcUgdZVjm/R81VmaDPEP25Wj+C1rei
# cY5CPckLGBjHQqsJe7jJz1CJXBMUtZs10cVKMEK3n/xD2ku5GFWhx0K6eFwe50xL
# UIZD9GfT7s/5/MyBZ1Ep8Q6H+GMuudDwF0mJitk3G8g6EzZprfMQMc3DAgMBAAGj
# ggFVMIIBUTAPBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQWBBS+VAIvv0Bsc0POrAkl
# Tp5DRBru4DAfBgNVHSMEGDAWgBS2oVQ5AsOgP46KvPrU+Bym0ToO/TAOBgNVHQ8B
# Af8EBAMCAQYwEwYDVR0lBAwwCgYIKwYBBQUHAwgwMAYDVR0fBCkwJzAloCOgIYYf
# aHR0cDovL2NybC5jZXJ0dW0ucGwvY3RuY2EyLmNybDBsBggrBgEFBQcBAQRgMF4w
# KAYIKwYBBQUHMAGGHGh0dHA6Ly9zdWJjYS5vY3NwLWNlcnR1bS5jb20wMgYIKwYB
# BQUHMAKGJmh0dHA6Ly9yZXBvc2l0b3J5LmNlcnR1bS5wbC9jdG5jYTIuY2VyMDkG
# A1UdIAQyMDAwLgYEVR0gADAmMCQGCCsGAQUFBwIBFhhodHRwOi8vd3d3LmNlcnR1
# bS5wbC9DUFMwDQYJKoZIhvcNAQEMBQADggIBALiTWXfJTBX9lAcIoKd6oCzwQZOf
# ARQkt0OmiQ390yEqMrStHmpfycggfPGlBHdMDDYhHDVTGyvY+WIbdsIWpJ1BNRt9
# pOrpXe8HMR5sOu71AWOqUqfEIXaHWOEs0UWmVs8mJb4lKclOHV8oSoR0p3GCX2tV
# O+XF8Qnt7E6fbkwZt3/AY/C5KYzFElU7TCeqBLuSagmM0X3Op56EVIMM/xlWRaDg
# Rna0hLQze5mYHJGv7UuTCOO3wC1bzeZWdlPJOw5v4U1/AljsNLgWZaGRFuBwdF62
# t6hOKs86v+jPIMqFPwxNJN/ou22DqzpP+7TyYNbDocrThlEN9D2xvvtBXyYqA7jh
# YY/fW9edUqhZUmkUGM++Mvz9lyT/nBdfaKqM5otK0U5H8hCSL4SGfjOVyBWbbZlU
# IE8X6XycDBRRKEK0q5JTsaZksoKabFAyRKJYgtObwS1UPoDGcmGirwSeGMQTJSh+
# WR5EXZaEWJVA6ZZPBlGvjgjFYaQ0kLq1OitbmuXZmX7Z70ks9h/elK0A8wOg8oiN
# Vd3o1bb59ms1QF4OjZ45rkWfsGuz8ctB9/leCuKzkx5Rt1WAOsXy7E7pws+9k+jr
# ePrZKw2DnmlNaT19QgX2I+hFtvhC6uOhj/CgjVEA4q1i1OJzpoAmre7zdEg+kZcF
# IkrDHgokA5mcIMK1MIIFyTCCBLGgAwIBAgIQG7WPJSrfIwBJKMmuPX7tJzANBgkq
# hkiG9w0BAQwFADB+MQswCQYDVQQGEwJQTDEiMCAGA1UEChMZVW5pemV0byBUZWNo
# bm9sb2dpZXMgUy5BLjEnMCUGA1UECxMeQ2VydHVtIENlcnRpZmljYXRpb24gQXV0
# aG9yaXR5MSIwIAYDVQQDExlDZXJ0dW0gVHJ1c3RlZCBOZXR3b3JrIENBMB4XDTIx
# MDUzMTA2NDMwNloXDTI5MDkxNzA2NDMwNlowgYAxCzAJBgNVBAYTAlBMMSIwIAYD
# VQQKExlVbml6ZXRvIFRlY2hub2xvZ2llcyBTLkEuMScwJQYDVQQLEx5DZXJ0dW0g
# Q2VydGlmaWNhdGlvbiBBdXRob3JpdHkxJDAiBgNVBAMTG0NlcnR1bSBUcnVzdGVk
# IE5ldHdvcmsgQ0EgMjCCAiIwDQYJKoZIhvcNAQEBBQADggIPADCCAgoCggIBAL35
# ePjm1YAMZJ2GG5ZkZz8iOh51AX3v+1xnjMnMXGupkea5QuUgS5vam3u5mV3Zm4BL
# 14RAKyfT6Lowuz4JGqdJle8rQCTCl8en7psl76gKAJeFWqqd3CnJ4jUH63BNStbB
# s1a4oUE4m9H7MX+P4F/hsT8PjhZJYNcGjRj5qiYQqyrT0NFnjRtGvkcw1S5y0cVj
# 2udjeUR+S2MkiYYuND8pTFKLKqfA4pEoibnAW/kd2ecnrf+aApfBxlCSmwIsvam5
# NFkKv4RK/9/+s5/r2Z7gmCPspmt3FirbzK07HKSH3EZzXhliaEVX5JCCQrtC1vBh
# 4MGjPWajXfQY7ojJjRdFKZkydQIx7ikmyGsC5rViRX83FVojaInUPt5OJ7DwQAy8
# TRfLTaKzHtAGWt32k89XdZn1+oYaZ3izv5b+NNy951JW5bPldXvXQZEF3F1p45UN
# Q7n8g5Y5lXtsgFpPE3LG130pekS6UqQq1UFGCSD+IqC2WzCNvIkM1ddw+IdS/drv
# rFEuB7NO/tAJ2nDvmPpW5m3btVdL3OUsJRXIni54TvjanJ6GLMpX8xrlyJKLGoKW
# esO8UBJp2A5aRos66yb6I8m2sIG+QgCk+Nb+MC7H0kb25Y51/fLMudCHW8wGEGC7
# gzW3XmfeR+yZSPGkoRX+rYxijjlVTzkWubFjnf+3AgMBAAGjggE+MIIBOjAPBgNV
# HRMBAf8EBTADAQH/MB0GA1UdDgQWBBS2oVQ5AsOgP46KvPrU+Bym0ToO/TAfBgNV
# HSMEGDAWgBQIds3LB/8k9sXN7buQvOKEN0Z19zAOBgNVHQ8BAf8EBAMCAQYwLwYD
# VR0fBCgwJjAkoCKgIIYeaHR0cDovL2NybC5jZXJ0dW0ucGwvY3RuY2EuY3JsMGsG
# CCsGAQUFBwEBBF8wXTAoBggrBgEFBQcwAYYcaHR0cDovL3N1YmNhLm9jc3AtY2Vy
# dHVtLmNvbTAxBggrBgEFBQcwAoYlaHR0cDovL3JlcG9zaXRvcnkuY2VydHVtLnBs
# L2N0bmNhLmNlcjA5BgNVHSAEMjAwMC4GBFUdIAAwJjAkBggrBgEFBQcCARYYaHR0
# cDovL3d3dy5jZXJ0dW0ucGwvQ1BTMA0GCSqGSIb3DQEBDAUAA4IBAQBRwqFYFiIQ
# i/yGMdTCMtNc+EuiL2o+TfirCB7t1ej65wgN7LfGHg6ydQV6sQv613RqAAYfpM6q
# 8mt92BHAEQjUDk1hxTqo+rHh45jq4mP9QfWTfQ28XZI7kZplutBfTL5MjWgDEBbV
# 8dAEioUz+TfnWy4maUI8us281HrpTZ3a50P7Y1KAhQTEJZVV8H6nnwHFWyj44M6G
# cKYnOzn7OC6YU2UidS3X9t0iIpGW691o7T+jGZfTOyWI7DYSPal+zgKNBZqSpydu
# RbKcYoY3DaQzjteoTtBKF0NMxfGnbNIeWGwUUX6KVKH27595el2BmhaQD+G78UoA
# +fndvu2q7M4KMYID8TCCA+0CAQEwazBWMQswCQYDVQQGEwJQTDEhMB8GA1UEChMY
# QXNzZWNvIERhdGEgU3lzdGVtcyBTLkEuMSQwIgYDVQQDExtDZXJ0dW0gVGltZXN0
# YW1waW5nIDIwMjEgQ0ECEQDxZCWMCbbie+IOMmCOS/SoMA0GCWCGSAFlAwQCAgUA
# oIIBVzAaBgkqhkiG9w0BCQMxDQYLKoZIhvcNAQkQAQQwHAYJKoZIhvcNAQkFMQ8X
# DTIyMDMyNTEyNDAyOVowNwYLKoZIhvcNAQkQAi8xKDAmMCQwIgQgG1m/6OV3K6z2
# Q7t5rLSOgVh4TyHFVK4TR206Gj4FxdMwPwYJKoZIhvcNAQkEMTIEMPxNzSnEHbAg
# m4g84az6VCSoGww0qLcjkZ1hZCywyPHkmqNiK3hmzobGpjxKJpA2OTCBoAYLKoZI
# hvcNAQkQAgwxgZAwgY0wgYowgYcEFNMRxpUxG4znP9W1Uxis31mK4ZsTMG8wWqRY
# MFYxCzAJBgNVBAYTAlBMMSEwHwYDVQQKExhBc3NlY28gRGF0YSBTeXN0ZW1zIFMu
# QS4xJDAiBgNVBAMTG0NlcnR1bSBUaW1lc3RhbXBpbmcgMjAyMSBDQQIRAPFkJYwJ
# tuJ74g4yYI5L9KgwDQYJKoZIhvcNAQEBBQAEggIAiLNr4stij6uFD6yi9Akl0EgY
# jnmw50D36oecUOWphXHzJ8jOkLYHmow4cv/qLMyYULSacWoog1Nf9zdbUA1k0Pl/
# JE9G1w/WVsjjkReutzBrNOoQ+ud8OobDKOz6SKVn5oi1226ZHPWHtOYOicCvyMKv
# DvFKeBAQzMGK5ip2TnGYM07C0ANV3xMO4a700l2UbhugfBeKVPnO9OjN5+Q1ijBL
# cdar/ixRn5L8SdEsKhJZtQnXSpWIsVI/i/zJa44f402WQo5gFlEyHN60ReRboqNV
# PqeTEaKmkPyOeI21vvTu4CjjBZGJfYwIdwltAEbYnzy7zKq4yf484vroMvNC10Lz
# hTItTs5N/c5Kv9xT9sXfGuVSrHdz6BjjZ4dNX/44eNRP7A7SH1Kh79pEzJyLtP0z
# AqU9+c6eV7Ruu6RNUl3VqGT5DzwINFOv9JE7SKxjI5w6mRylGjB7YySSIXzroUaW
# OjGP8yWnic/mzZwBQSC4orgJOZ633s8CcQfyAGjMIELemu9i83vg5frpdsrrw+3Y
# KtU5j3Rgi98pdSxU/7DMn+A4CbQGc2QDtEPEL2wUbCmyU0vPmwaMcZfoLotxgMyd
# J3gNwIw98jxeUz4nXzCIAt7/tTkq8DkMUXgbED9kZENchaHudYnFnxmmaaC5QbDV
# RIu9bdEGlqZZd5eT+p8=
# SIG # End signature block
