#!/bin/bash

# Set transport mode to HTTP
export SONARQUBE_TRANSPORT=http

# Set the custom port
export SONARQUBE_HTTP_PORT=9090

# Allow all interfaces to listen
export SONARQUBE_HTTP_HOST=0.0.0.0

# SonarQube connection details
export SONAR_HOST_URL=http://your-sonarqube-server:9000
export SONAR_TOKEN=your-sonar-token

# Set the storage path
export STORAGE_PATH=/apps/opt/addvol/sonar-mcp/storage

# Print out the environment variables for verification
echo "Transport Mode: $SONARQUBE_TRANSPORT"
echo "Port: $SONARQUBE_HTTP_PORT"
echo "Host: $SONARQUBE_HTTP_HOST"
echo "SonarQube URL: $SONAR_HOST_URL"
echo "Storage Path: $STORAGE_PATH"

# Start the MCP server
java -jar sonarqube-mcp-server.jar
