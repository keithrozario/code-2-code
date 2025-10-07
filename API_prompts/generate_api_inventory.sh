#!/bin/bash

# This script loads all variables from config.sh and runs the analysis.
# It is NOT interactive.

# Load the configuration file. Make sure config.sh is in the same directory.
source config.sh

# -------------------------------------------------------------

echo "--- API Inventory Generator ---"
echo "Workspace: $WORKSPACE_PATH"
echo "Repository: $REPO_PATH"
echo

# 1. Change into the workspace directory defined in config.sh
cd "$WORKSPACE_PATH" || exit 1

# 2. Construct the prompt using variables from the config file.
PROMPT_TEXT="You are an expert code analyst. Analyze the repository at '$REPO_PATH' and generate a comprehensive API inventory, grouped by functionality.

For each functionality group, provide a one-sentence description, followed by a Markdown table listing its APIs with columns for: \`HTTP Method\`, \`Endpoint Path\`, and \`Description\`."

echo "Running analysis..."

# 3. Execute the command, using the output file name from the config.
gemini chat "$PROMPT_TEXT" > "$API_INVENTORY_FILE"

echo
echo "✅ Done! API inventory saved to '$WORKSPACE_PATH/$API_INVENTORY_FILE'."
