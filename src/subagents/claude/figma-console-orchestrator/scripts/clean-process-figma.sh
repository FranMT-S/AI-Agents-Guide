#!/bin/bash

# Define the port range
START_PORT=9225
END_PORT=9232

echo "Checking for processes locking ports $START_PORT to $END_PORT..."

# Iterate through the port range
for port in $(seq $START_PORT $END_PORT); do
    # Find PIDs using the port
    pids=$(lsof -t -i:$port 2>/dev/null)
    
    if [ -n "$pids" ]; then
        echo "Killing following PIDs using port $port: $pids"
        kill -9 $pids 2>/dev/null
    fi
done

echo "Clean up process completed."
