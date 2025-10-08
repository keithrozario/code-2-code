#!/bin/bash
set -e

echo "--- Analyze APIs in more detail ---"

source config.sh

echo "DEBUG: Repository to analyze is [$REPO_PATH]"
echo "DEBUG: Output will be saved to [$OUTPUT_PATH/$API_ANALYZE]"

# --- Change directory to the repository to set the workspace ---
echo "DEBUG: Setting workspace to repository path..."
cd "$REPO_PATH" || exit 1
# -----------------------------------------------------------------

PROMPT_TEXT="You are an expert code analyst. Analyze the repository at '$REPO_PATH'.

First, identify the names of the primary data classes, structs, or models used in the request and response of this function.

For each parameter in the request and response, document the following in a table:
- Name
- Data Type (string, integer, etc.)
- Description (in a business context)
- Optionality (mandatory or optional)

Provide a very detailed breakdown of your analysis. Please structure your findings clearly in a table format" 

echo "DEBUG: Running analysis..."

# --- FIX: Use the correct output variable defined in your config.sh ---
gemini chat "$PROMPT_TEXT" > "$OUTPUT_PATH/$API_ANALYZE"

echo
# --- FIX: Use the correct output variable in the final message ---
echo "✅ Done! Report saved to '$OUTPUT_PATH/$API_ANALYZE'."
