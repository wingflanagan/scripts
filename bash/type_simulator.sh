#!/bin/bash

# Wait for 3 seconds to allow you to focus on the target window
sleep 3

# Define the text to type, including newline (\n) and tab (\t)
text="RE: PRE-MEETING PREP MEETING FOLLOW UP TO SCHEDULE ACTUAL MEETING	LET'S GO AHEAD AND PUT A PIN IN THAT THOUGHT BUBBLE, CIRCLE BACK AFTER WE'VE HAD A CHANCE TO MARINATE ON IT, AND REALIGN OUR COLLECTIVE SYNERGY SO WE CAN LEVERAGE OUR CORE COMPETENCIES AND REFOCUS OUR BANDWIDTH ON THE PRIMARY ACTION ITEMS WE'VE STRATEGICALLY ROADMAPPED IN OUR MISSION-CRITICAL OBJECTIVES, ENSURING WE'RE ALL ROWING IN THE SAME DIRECTION TOWARDS LOW-HANGING FRUIT THAT MOVES THE NEEDLE AND OPTIMIZES SCALABLE VALUE-ADDS GOING FORWARD INTO THE NEXT QUARTER, OR WHENEVER WE DECIDE TO KICK THE CAN FURTHER DOWN THE ROAD.

PLEASE SEE ATTACHMENTS FOR FURTHER DETAILS.

THANKS,

John Flanagan
-----------------
Senior Software Developer
Lead Software Architect
Principal Engineer & Visionary Technologist
Chief Software Overlord
Omnipotent Technological Demigod"


# Iterate over each character in the text
for (( i=0; i<${#text}; i++ )); do
    char="${text:$i:1}"
    if [ "$char" = $'\n' ]; then
        xdotool key Return
    elif [ "$char" = $'\t' ]; then
        xdotool key Tab
    else
        xdotool type "$char"
    fi
    # Generate a random delay between 0.05 and 0.15 seconds (50-150 ms)
    delay=$(awk -v min=50 -v max=150 'BEGIN {srand(); print int(min+rand()*(max-min+1))}')
    sleep $(echo "scale=3; $delay/1000" | bc)
done
