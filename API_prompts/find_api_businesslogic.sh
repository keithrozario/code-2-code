#!/bin/bash
set -e # Exit immediately if any command fails.

echo "--- Business Logic Analysis Script ---"

# 1. Load configuration to get the repository path
source config.sh

# 2. Define the output file for this script
echo "DEBUG: Repository to analyze is [$REPO_PATH]"
echo "DEBUG: Output will be saved to [$OUTPUT_PATH/$API_BUSINESSLOGIC]"

# 3. Change directory to the repository to set the workspace
echo "DEBUG: Setting workspace to repository path..."
cd "$REPO_PATH" || exit 1

# 4. Construct the prompt to analyze business logic
PROMPT_TEXT="You are an expert business analyst and software architect. Your goal is to analyze the repository at '$REPO_PATH' and document its core business logic. Do not just describe what the code does; explain the business rules it enforces.

First, provide a high-level, plain-language summary of the end-to-end business process this function implements.

Then, detail the following specific rules by quoting or referencing the relevant code snippets:
1.  **Validation Rules:** What checks are performed on the input data before processing? (e.g., checking if an account is active, validating transaction limits).
2.  **Calculation/Transformation Logic:** What are the key calculations or data transformations? Explain the purpose of any complex loops or algorithms.
3.  **Conditional Logic (Edge Cases):** What are the major \`if/else\` branches, and what different business scenarios do they handle? (e.g., handling a new customer vs. a returning one).
4.  **Error Handling:** How are specific business errors (e.g., 'Insufficient Funds', 'Invalid User') identified and handled?

Provide a detailed breakdown of your analysis. Please structure your findings in a table format

Your response must begin directly with the Markdown table and contain no introductory sentences."

echo "DEBUG: Running analysis..."

# 5. Execute the command and save the output
gemini chat "$PROMPT_TEXT" > "$OUTPUT_PATH/$API_BUSINESSLOGIC"

echo
echo "✅ Done! Business logic report saved to '$OUTPUT_PATH/$API_BUSINESSLOGIC'."
