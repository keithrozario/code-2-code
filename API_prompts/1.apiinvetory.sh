#!/bin/bash

# This script first establishes a workspace and then runs the Gemini CLI
# to analyze a specific repository within that workspace.

echo "--- Gemini API Inventory Generator ---"
echo

# 1. Ask for the top-level workspace directory.
echo "First, let's define the workspace. This should be the parent directory."
read -p "Enter the absolute path to your main projects folder (e.g., /Users/himakunisetty/Documents/Gemini Code Assist): " WORKSPACE_PATH

# 2. Ask for the specific repository folder path.
echo
echo "Now, which project do you want to analyze?"
read -p "Enter the absolute path to the repository folder (e.g., /Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4): " REPO_PATH

# 3. Validate paths and change to the workspace directory.
if [ -z "$WORKSPACE_PATH" ] || [ ! -d "$WORKSPACE_PATH" ]; then
    echo "Error: Please provide a valid workspace directory."
    exit 1
fi
if [ -z "$REPO_PATH" ] || [ ! -d "$REPO_PATH" ]; then
    echo "Error: Please provide a valid repository directory."
    exit 1
fi

echo "Setting workspace to: $WORKSPACE_PATH"
cd "$WORKSPACE_PATH" || exit 1

# 4. Construct the prompt for the Gemini CLI.
PROMPT_TEXT="You are an expert code analyst. Analyze the repository located at the absolute path '$REPO_PATH'.

Your task is to identify all API endpoints and group them by their likely business functionality (e.g., 'Account Management').

For each functionality group, provide a one-sentence description, followed by a Markdown table listing its APIs with columns for: \`HTTP Method\`, \`Endpoint Path\`, and \`Description\`."

echo
echo "Running analysis on '$REPO_PATH'... This may take some time."

# 5. Execute the Gemini CLI command. The output file will be saved in the workspace.
gemini chat "$PROMPT_TEXT" > api_inventory.md

echo
echo "✅ Done! API inventory saved to '$WORKSPACE_PATH/api_inventory.md'"
