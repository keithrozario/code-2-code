#!/bin/bash

# This script interactively prompts the user for paths and then
# generates a config.sh file for the API analysis tools.

echo "--- Configuration Setup for API Analysis ---"
echo

# 1. Prompt for the workspace path.
read -p "Enter the absolute path for your main workspace (e.g., /Users/himakunisetty/Documents/Gemini Code Assist): " WORKSPACE_PATH

# 2. Prompt for the repository path.
read -p "Enter the absolute path to the repository you want to analyze: " REPO_PATH

# 3. Define the output filenames.
API_INVENTORY_FILE="api_inventory.md"
API_DEPENDENCY_FILE="api_dependency_map.md"

# 4. Write the variables to a new config.sh file.
# The `>` operator creates or overwrites the file.
cat > config.sh << EOL
#!/bin/bash

# -- Paths --
export WORKSPACE_PATH="$WORKSPACE_PATH"
export REPO_PATH="$REPO_PATH"

# -- Output Files --
export API_INVENTORY_FILE="$API_INVENTORY_FILE"
export API_DEPENDENCY_FILE="$API_DEPENDENCY_FILE"
EOL

echo
echo "✅ Configuration saved successfully to 'config.sh'!"
