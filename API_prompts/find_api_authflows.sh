#!/bin/bash
set -e

echo "--- Authentication & Authorization Analysis ---"

source config.sh

echo "DEBUG: Repository to analyze is [$REPO_PATH]"
echo "DEBUG: Output will be saved to [$OUTPUT_PATH/$API_AUTHFLOWS]"

# --- Change directory to the repository to set the workspace ---
echo "DEBUG: Setting workspace to repository path..."
cd "$REPO_PATH" || exit 1
# -----------------------------------------------------------------

PROMPT_TEXT="You are an expert code analyst. Analyze the repository at '$REPO_PATH'.

Analyze the code that handles the \`POST /login\` endpoint. Provide a step-by-step explanation of the authentication process. Detail how the user's credentials are validated, how the session or JWT token is created, and what key information is included in the token payload.

Analyze the code for a protected endpoint, for example, \`PUT /accounts/{id}\`. Identify and describe any security checks, role validations, or permission checks that are performed before the main logic is executed. Quote the specific code annotations or functions (e.g., \`@PreAuthorize\`) used to enforce this.

Provide a very detailed breakdown of your analysis. Please structure your findings clearly in a table format.

Your response must begin directly with the Markdown table and contain no introductory sentences."

echo "DEBUG: Running analysis..."

gemini chat "$PROMPT_TEXT" > "$OUTPUT_PATH/$API_AUTHFLOWS"

echo
echo "✅ Done! Report saved to '$OUTPUT_PATH/$API_AUTHFLOWS'."
