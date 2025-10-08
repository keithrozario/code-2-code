#!/bin/bash

# This script reads the config file and the API inventory, then runs
# prompts to map upstream and downstream dependencies for each API.

# Load the configuration file to get all the paths and filenames.
source config.sh

# -------------------------------------------------------------

echo "--- API Dependency Mapper ---"

# Define the absolute path to the input file from your config
INPUT_FILE="$WORKSPACE_PATH/$API_INVENTORY_FILE"
OUTPUT_FILE="$WORKSPACE_PATH/$API_DEPENDENCY_FILE"

echo "Reading from: $INPUT_FILE"
echo "Writing to: $OUTPUT_FILE"

if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file '$INPUT_FILE' not found. Please ensure it was created successfully."
    exit 1
fi

# Set the workspace and clear the output file
cd "$WORKSPACE_PATH" || exit 1
echo "# API Dependency Map" > "$OUTPUT_FILE"

# This command parses the Markdown table from the input file.
# It extracts the Endpoint Path (column 3) and Source Location (column 5).
awk -F'|' 'NR > 2 {gsub(/`/, ""); gsub(/ /, "", $3); gsub(/ /, "", $5); if (length($3)>1) print $3 "|" $5}' "$INPUT_FILE" | while IFS='|' read -r ENDPOINT_PATH SOURCE_LOCATION; do

    # --- Construct and run the prompts for each API ---
    echo "Analyzing dependencies for: $ENDPOINT_PATH"

    {
        echo "--------------------------------------------------"
        echo "### Dependencies for: \`$ENDPOINT_PATH\`"
        echo ""

        # Prompt for Upstream Dependencies
        UPSTREAM_PROMPT="Analyze the function at the source location \`$REPO_PATH/$SOURCE_LOCATION\`. List all outgoing HTTP client requests (e.g., calls using 'fetch', 'axios', 'requests.get') made within this function. Provide the destination URL if possible."

        echo "**Upstream Dependencies (Calls made BY this API):**"
        gemini chat "$UPSTREAM_PROMPT"
        echo ""

        # Prompt for Downstream Consumers
        DOWNSTREAM_PROMPT="Perform a repository-wide string search within '$REPO_PATH' for the endpoint path \`$ENDPOINT_PATH\`. List the file paths that contain this string, as these are potential callers."

        echo "**Downstream Consumers (Potential callers OF this API):**"
        gemini chat "$DOWNSTREAM_PROMPT"
        echo ""
    } >> "$OUTPUT_FILE"

done

echo
echo "✅ Done! API dependency map saved to '$OUTPUT_FILE'."
