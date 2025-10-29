#!/bin/bash

# Set the number of files to create
NUM_FILES=97

# Define possible file extensions and corresponding file types
declare -A FILE_TYPES=(
    ["docx"]="Q3_financial_report,ProjectProposal,Strategic_Plan,company-policy-2024,performance_review,NotesMeeting-032024"
    ["xlsx"]="budget_projection,employee_salary_data,inventory_list,Client-contacts,Q1_Revenue_Report,ProfitAnalysis"
    ["pptx"]="Marketing_Presentation,InvestorPitch,Company_Update,Sales_Strategy,Training-Slides,Product-Roadmap"
    ["vsdx"]="network_diagram,system_architecture,OfficeLayout,wireframe-design,app-architecture,Flowchart"
    ["pdf"]="Legal_Contract,Whitepaper,Annual_Report,UserGuide,ProjectDocumentation,policy-handbook"
    ["csv"]="customer_data,sales_leads,product_catalog,logistics-info,shipping_details,DataExport"
    ["txt"]="todo-list,random_notes,readme,debug_log,meeting-minutes,team_tasks"
    ["eml"]="internal_memo,CustomerComplaint,HR_Announcement,FollowUp,Email-thread,StaffUpdate"
)

# Convert associative array keys into an indexed array
EXTENSIONS=(${!FILE_TYPES[@]})

# Generate files
for ((i = 1; i <= NUM_FILES; i++)); do
    # Select a random file extension from the list
    EXTENSION=${EXTENSIONS[$RANDOM % ${#EXTENSIONS[@]}]}

    # Get a random filename from the list for the chosen type
    FILENAMES=(${FILE_TYPES[$EXTENSION]//,/ }) 
    FILENAME=${FILENAMES[$RANDOM % ${#FILENAMES[@]}]}

    # Apply random naming conventions
    case $((RANDOM % 6)) in
        0) FILENAME=$(echo "$FILENAME" | tr '[:lower:]' '[:upper:]') ;;   # ALL CAPS
        1) FILENAME=$(echo "$FILENAME" | tr '[:upper:]' '[:lower:]') ;;   # all lowercase
        2) FILENAME=$(echo "$FILENAME" | sed 's/_/ /g') ;;                # Spaces instead of underscores
        3) FILENAME=$(echo "$FILENAME" | sed 's/_/-/g') ;;                # Kebab-case
        4) FILENAME=$(echo "$FILENAME" | sed 's/_//g') ;;                 # No separators
        5) FILENAME=$(echo "$FILENAME" | awk '{print toupper(substr($0,1,1)) substr($0,2)}') ;; # Title Case
    esac

    # Only append a number ~20% of the time
    if (( RANDOM % 5 == 0 )); then
        FILENAME="${FILENAME}-${i}"
    fi

    # Add the file extension
    FILENAME="${FILENAME}.${EXTENSION}"

    # Generate a MASSIVE file size (between 20MB and 100MB)
    FILE_SIZE=$(( (20000 + RANDOM % 80000) * 1024 ))  # Multiply by 1000 to get MB-scale sizes

    # Fill the file with 'X'
    head -c "$FILE_SIZE" < /dev/urandom | tr -dc 'X' > "$FILENAME"

    echo "Created: $FILENAME ($((FILE_SIZE / 1024 / 1024)) KB)"
done

echo "All $NUM_FILES massive files have been successfully generated!"
