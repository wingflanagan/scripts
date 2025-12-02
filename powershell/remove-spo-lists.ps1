# delete-selected-lists.ps1
# Safely delete only a specific set of lists on a specific site.

# ================== CONFIG ==================

# Tenant root web URL
$webUrl  = "https://7vhr6d.sharepoint.com"

# ClientId from Register-PnPEntraIDAppForInteractiveLogin output
$clientId = "bb9fc6c0-bd3f-4d27-b740-229edf0c808d"

# Safety: start as $true for DRY RUN (no deletions)
$DryRun = $false

# Lists you actually want to delete
# Titles must match the list display name in SharePoint
$listsToDelete = @(
    "GoF---Yourself"
    "Musical Questions"
    "my test list"
    "test FAQ 2"
    "test list 001"
    "WhyOhWhy"
)

# ================== SCRIPT ==================

Write-Host "Connecting to $webUrl ..." -ForegroundColor Cyan
Connect-PnPOnline -Url $webUrl -ClientId $clientId -Interactive

Write-Host "Loaded $($listsToDelete.Count) lists to delete." -ForegroundColor Cyan

foreach ($title in $listsToDelete) {
    Write-Host ""
    Write-Host "Processing list '$title'..." -ForegroundColor Yellow

    # Get list by title
    $list = Get-PnPList -Identity $title -ErrorAction SilentlyContinue

    if ($null -eq $list) {
        Write-Warning "  !! List '$title' not found on $webUrl. Skipping."
        continue
    }

    $url = $list.RootFolder.ServerRelativeUrl

    if ($DryRun) {
        Write-Host "  DRY RUN: Would delete list '$title' (Url: $url)" -ForegroundColor Magenta
    }
    else {
        Write-Host "  Deleting list '$title' (sending to Recycle Bin)..." -ForegroundColor Red
        # Use Id to be extra precise
        Remove-PnPList -Identity $list.Id -Recycle -Force
        Write-Host "  Deleted (recycled) '$title'." -ForegroundColor Green
    }
}

Write-Host ""
if ($DryRun) {
    Write-Host "DRY RUN completed. No lists were actually deleted. Set `$DryRun = `$false to commit." -ForegroundColor Magenta
} else {
    Write-Host "Done. Selected lists have been deleted (to Recycle Bin)." -ForegroundColor Green
}
