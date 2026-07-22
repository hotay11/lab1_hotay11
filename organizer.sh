#!/bin/bash

# Check if archive directory exists, create it if not
if [ ! -d "archive" ]; then
    mkdir archive
fi

# Check if grades.csv exists
if [ ! -f "grades.csv" ]; then
    echo "Error: grades.csv does not exist."
    exit 1
fi

# Create timestamp
timestamp=$(date +"%Y%m%d-%H%M%S")

# Create new archived filename
archived_file="grades_${timestamp}.csv"

# Move grades.csv to archive with new name
mv grades.csv "archive/$archived_file"

# Create a new empty grades.csv file
touch grades.csv

# Log the archive operation
echo "Timestamp: $timestamp | Original: grades.csv | Archived: $archived_file" >> organizer.log

echo "Grades archived successfully."
echo "Archived file: archive/$archived_file"
