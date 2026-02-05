# Change DNS to Google Public DNS
# Run this script as Administrator

Write-Host "Current DNS Configuration:" -ForegroundColor Yellow
Get-DnsClientServerAddress -AddressFamily IPv4

Write-Host "`nChanging DNS to Google Public DNS (8.8.8.8, 8.8.4.4)..." -ForegroundColor Cyan

# Get active network adapter
$adapter = Get-NetAdapter | Where-Object {$_.Status -eq "Up"} | Select-Object -First 1

if ($adapter) {
    Write-Host "Setting DNS for adapter: $($adapter.Name)" -ForegroundColor Green
    Set-DnsClientServerAddress -InterfaceAlias $adapter.Name -ServerAddresses ("8.8.8.8","8.8.4.4")
    
    Write-Host "`nNew DNS Configuration:" -ForegroundColor Yellow
    Get-DnsClientServerAddress -InterfaceAlias $adapter.Name -AddressFamily IPv4
    
    Write-Host "`nFlushing DNS cache..." -ForegroundColor Cyan
    ipconfig /flushdns
    
    Write-Host "`nDNS configuration updated successfully!" -ForegroundColor Green
    Write-Host "You can now test the database connection again." -ForegroundColor Green
} else {
    Write-Host "No active network adapter found!" -ForegroundColor Red
}

Write-Host "`nTo revert to automatic DNS, run:" -ForegroundColor Yellow
Write-Host "Set-DnsClientServerAddress -InterfaceAlias '$($adapter.Name)' -ResetServerAddresses" -ForegroundColor White
