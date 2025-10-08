#!/bin/bash
set -e

echo "--- Data Models & Schema Analysis ---"

source config.sh

echo "DEBUG: Repository to analyze is [$REPO_PATH]"
echo "DEBUG: Output will be saved to [$OUTPUT_PATH/$API_DATAMODELS]"

# --- Change directory to the repository to set the workspace ---
echo "DEBUG: Setting workspace to repository path..."
cd "$REPO_PATH" || exit 1
# -----------------------------------------------------------------

PROMPT_TEXT="You are an expert code analyst. Analyze the repository at '$REPO_PATH'.

Analyze the repository wide codebase, focusing on the data models, entities, or schema definition files (e.g., files using JPA annotations, SQLAlchemy models, or plain SQL DDL).

Your task is to generate the database schema for all the tables.

For each table, create a Markdown table with the following columns:
- \`Column Name\`
- \`Data Type\`
- \`Constraints\` (e.g., PRIMARY KEY, NOT NULL, FOREIGN KEY to another_table(id))
- \`Description\` (The business purpose of the column)

Provide a very detailed breakdown of your analysis. Please structure your findings clearly in a table format

Your response must begin directly with the Markdown table and contain no introductory sentences." 

echo "DEBUG: Running analysis..."

gemini chat "$PROMPT_TEXT" > "$OUTPUT_PATH/$API_DATAMODELS"

echo
echo "✅ Done! Report saved to '$OUTPUT_PATH/$API_DATAMODELS'."
