$ports = 9225..9232
foreach ($port in $ports) {
    $pids = netstat -ano | findstr :$port
    if ($pids) {
        $pid = $pids.Split(' ') | Select-Object -Last 1
        Write-Host "Killing process on port $port with PID $pid"
        taskkill /F /PID $pid
    }
}
