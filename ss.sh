#!/bin/bash

# Define the command name pattern to manage
COMMAND_PATTERN="nessus*"

# Define the desired nice value (lowest priority) and CPU limit
NICE_VALUE=19
CPU_LIMIT=30

# Get PIDs of all processes matching the specified pattern
PIDS=$(pgrep -f $COMMAND_PATTERN)

# Check if any PIDs were found
if [ -n "$PIDS" ]; then
  for PID in $PIDS; do
    if [ -n "$PID" ]; then
      # Log the PID and applied settings
      echo "Applying settings to PID $PID" >> /var/log/manage_cpu_limit.log
      # Adjust priority to the lowest (highest nice value)
      sudo renice -n $NICE_VALUE -p $PID >> /var/log/manage_cpu_limit.log 2>&1
      # Apply CPU limit
      sudo cpulimit -p $PID -l $CPU_LIMIT >> /var/log/manage_cpu_limit.log 2>&1 &
    fi
  done
else
  echo "No processes found for command pattern: $COMMAND_PATTERN" >> /var/log/manage_cpu_limit.log
fi
