#!/bin/bash
set -e

echo "--- Non-Functional Requirements ---"

source config.sh

echo "DEBUG: Repository to analyze is [$REPO_PATH]"
echo "DEBUG: Output will be saved to [$OUTPUT_PATH/$API_NFR]"

# --- Change directory to the repository to set the workspace ---
echo "DEBUG: Setting workspace to repository path..."
cd "$REPO_PATH" || exit 1
# -----------------------------------------------------------------

PROMPT_TEXT="You are an expert code analyst. Analyze the repository at '$REPO_PATH'.

Perform a repository-wide search for clues related to non-functional requirements.

1.  **Search documentation:** Look for keywords like 'performance', 'latency', 'scalability', 'security standards', 'SLO', or 'SLA' in all documentation files (e.g., \`.md\`, \`.txt\`).
2.  **Analyze configurations:** Analyze infrastructure and application configuration files (e.g., \`pom.xml\`, \`application.properties\`, \`Dockerfile\`) for settings related to request timeouts, database connection pool sizes, and cache configurations.

Provide a very detailed breakdown of your analysis. Please structure your findings clearly in a table format" 

echo "DEBUG: Running analysis..."

# --- FIX: Use the correct output variable defined in your config.sh ---
gemini chat "$PROMPT_TEXT" > "$OUTPUT_PATH/$API_NFR"

echo
# --- FIX: Use the correct output variable in the final message ---
echo "✅ Done! Report saved to '$OUTPUT_PATH/$API_NFR'."
