#!/bin/bash
set -e

echo "--- Data Models & Schema Analysis ---"

source config.sh

echo "DEBUG: Repository to analyze is [$REPO_PATH]"
echo "DEBUG: Output will be saved to [$OUTPUT_PATH/$API_SCHEMA]"

# --- Change directory to the repository to set the workspace ---
echo "DEBUG: Setting workspace to repository path..."
cd "$REPO_PATH" || exit 1
# -----------------------------------------------------------------

PROMPT_TEXT="You are an expert code analyst. Analyze the repository at '$REPO_PATH'.

For each parameter in the request and response, document the following in a table:
- Name
- Data Type (string, integer, etc.)
- Description (in a business context)
- Optionality (mandatory or optional)


Provide a very detailed breakdown of your analysis. Please structure your findings clearly in a table format. 

Your response must begin directly with the Markdown table and contain no introductory sentences."

echo "DEBUG: Running analysis..."

gemini chat "$PROMPT_TEXT" > "$OUTPUT_PATH/$API_SCHEMA"

echo
echo "✅ Done! Report saved to '$OUTPUT_PATH/$API_SCHEMA'."
