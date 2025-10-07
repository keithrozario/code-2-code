#!/bin/bash

# This script loads variables from config.sh and saves the output
# to the folder where the script was originally executed.

EXECUTION_PATH=$(pwd)
# --------------------------------------------------------------------

# Load the configuration file.
source config.sh

# -------------------------------------------------------------

echo "--- API Inventory Generator ---"
echo "Script is running from: $EXECUTION_PATH"
echo "Setting workspace to: $WORKSPACE_PATH"
echo "Analyzing Repository: $REPO_PATH"
echo

# Change into the workspace directory for the Gemini CLI to function correctly.
cd "$WORKSPACE_PATH" || exit 1

# Ask for the sub-folders to scan within the repository.
#echo "Enter the specific sub-folders to scan within the repo (e.g., src/main/java):"
#read -p "> " FOLDERS_TO_SCAN

# Construct the prompt using the variables from the config file.
PROMPT_TEXT="You are an expert code analyst. Analyze the repository at '$REPO_PATH'.

Constraint: Focus your analysis ONLY on the sub-directories: '$FOLDERS_TO_SCAN'.

Your task is to generate a complete inventory of all defined API endpoints..." # (rest of prompt)

echo "Running analysis..."

# --- FIX: Use the captured execution path for the output file ---
gemini chat "$PROMPT_TEXT" > "$EXECUTION_PATH/$API_INVENTORY_FILE"
# -----------------------------------------------------------------

echo
echo "✅ Done! API inventory saved to '$EXECUTION_PATH/$API_INVENTORY_FILE'."
