param(
    [string]$Url = "http://127.0.0.1:8765/test/mcp-event"
)

$payload = @{
    source = "listener-playground"
    kind = "mcp-test-event"
    message = "hello from PowerShell"
    sentAt = (Get-Date).ToUniversalTime().ToString("o")
}

Invoke-RestMethod `
    -Method Post `
    -Uri $Url `
    -ContentType "application/json" `
    -Body ($payload | ConvertTo-Json)
