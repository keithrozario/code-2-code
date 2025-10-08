#!/bin/bash
set -e # Exit immediately if any command fails.

echo "--- Final API Inventory Script ---"

# 1. Load configuration
source config.sh

echo "DEBUG: Workspace is [$WORKSPACE_PATH]"
echo "DEBUG: Repository to analyze is [$REPO_PATH]"
echo "DEBUG: Output will be saved to [$OUTPUT_PATH/$API_INVENTORY_FILE]"

# 2. CRITICAL STEP: Change into the repository folder.
# This sets the correct workspace for the Gemini CLI.
echo "DEBUG: Changing directory to the repository path..."
cd "$REPO_PATH" || exit 1
echo "DEBUG: Current directory is now [$(pwd)]"

# 3. Construct the prompt to analyze the CURRENT directory.
PROMPT_TEXT="You are an expert code analyst. Analyze the current working directory and generate a comprehensive API inventory, grouped by functionality. For each group, provide a one-sentence description, followed by a Markdown table with columns for: \`HTTP Method\`, \`Endpoint Path\`, and \`Description\`.

Your response must begin directly with the Markdown table and contain no introductory sentences."

echo "DEBUG: Running analysis..."

# 4. Execute the command and save the output to the correct, absolute path.
gemini chat "$PROMPT_TEXT" > "$WORKSPACE_PATH/$API_INVENTORY_FILE"

echo
echo "✅ Done! API inventory saved successfully to '$OUTPUT_PATH/$API_INVENTORY_FILE'."
