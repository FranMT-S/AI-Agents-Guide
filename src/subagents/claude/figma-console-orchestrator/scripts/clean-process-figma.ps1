$ports = 9225..9232
foreach ($port in $ports) {
    $_pids = netstat -ano | findstr :$port
    if ($_pids) {
        $_pid = $_pids.Split(' ') | Select-Object -Last 1
        Write-Host "Killing process on port $port with PID $_pid"
        taskkill /F /PID $_pid

    }
}

