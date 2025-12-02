# get-spo-lists.ps1

$adminUrl = "https://7vhr6d-admin.sharepoint.com"
$clientId = "bb9fc6c0-bd3f-4d27-b740-229edf0c808d"   # your AzureAppId from registration

Write-Host "Connecting to admin site $adminUrl..." -ForegroundColor Cyan

# 1) Connect once to the admin center
Connect-PnPOnline -Url $adminUrl -ClientId $clientId -Interactive

# 2) Get all tenant sites (skip personal OneDrive host)
$sites = Get-PnPTenantSite | Where-Object {
    $_.Url -notlike "*-my.sharepoint.com*" # skip OneDrive personal host
}

$results = @()

foreach ($site in $sites) {
    try {
        Write-Host "Checking site: $($site.Url)" -ForegroundColor Yellow
        
        # 3) Connect to each site using the SAME app registration
        Connect-PnPOnline -Url $site.Url -ClientId $clientId -Interactive

        # 4) Get lists from that site
        $lists = Get-PnPList | Select Title, RootFolder, ItemCount

        foreach ($list in $lists) {
            $results += [PSCustomObject]@{
                SiteUrl   = $site.Url
                ListName  = $list.Title
                ListUrl   = $list.RootFolder.ServerRelativeUrl
                ItemCount = $list.ItemCount
            }
        }
    }
    catch {
        Write-Warning "Failed to get lists for $($site.Url): $_"
    }
}

# 5) Export to CSV
$csvPath = Join-Path $PSScriptRoot "AllSharePointLists.csv"
$results | Export-Csv -Path $csvPath -NoTypeInformation -Encoding UTF8

Write-Host "Done. Exported $($results.Count) list records to $csvPath" -ForegroundColor Green
