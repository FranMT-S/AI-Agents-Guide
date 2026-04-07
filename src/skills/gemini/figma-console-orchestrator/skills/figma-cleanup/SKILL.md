---
name: figma-cleanup
description: Cleans up orphaned Figma Desktop Bridge WebSocket connections by identifying and killing processes locking the required port range (9223-9232). Use when 'All WebSocket ports 9223-9232 are in use' errors occur.
---

# Figma Cleanup

Use this skill when you encounter "All WebSocket ports 9223-9232 are in use" or connection errors with the Figma Desktop Bridge plugin.

## Cleanup Procedure

1. **Identify** active processes locking the ports:
   Run `netstat -ano | findstr :922` to see which PIDs are using the ports.

2. **Terminate** the offending processes:
   Use `taskkill /F /PID <pid>` for each PID identified.

3. **Verify** and **Reconnect**:
   Check if the port range is free and attempt to reconnect in Figma.

## Reusable Script

Use the provided `scripts/cleanup_figma.ps1` for an automated cleanup process.
