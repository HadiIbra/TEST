#!/bin/bash

# Access the variables passed from Python and convert them to integers
numOfButtonAction="$1"
moveDirection="$2"

# Convert the string arguments to integers
numOfButtonAction=$(($numOfButtonAction))

# Print the variables ...
echo "move direction: $moveDirection"
echo "number of needed Button Actions: $numOfButtonAction"

############ TODO: implement ur code here #########