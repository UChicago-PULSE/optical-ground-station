"""Shared constants for the PULSE-A interface."""

MAX_DATA_POINTS = 100 # Max points to store and plot for LIVE data
MAX_TABLE_ROWS = 50 # Max rows for telemetry table

# Define available LIVE data sources for plotting and storage
LIVE_DATA_SOURCES = ["Sensor_A", "Sensor_B", "Sensor_C", "Temp", "None"]

# Prefix for identifying CSV file sources in dropdowns (No longer used for ./data/)
# CSV_SOURCE_PREFIX = "CSV: " # Keep commented or remove

# Prefix for identifying sources loaded from archive directories
ARCHIVE_SOURCE_PREFIX = "Archive: "