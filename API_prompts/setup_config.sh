#!/bin/bash

# This script interactively prompts the user for paths and then
# generates a config.sh file for the API analysis tools.

echo "--- Configuration Setup for API Analysis ---"
echo

# This line automatically finds the folder where this config file is.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 1. Prompt for the workspace path.
read -p "Enter the absolute path for your main workspace: " WORKSPACE_PATH

# 2. Prompt for the repository path.
read -p "Enter the absolute path to the repository you want to analyze: " REPO_PATH

# 3. Define the output filenames.
API_INVENTORY_FILE="api_inventory.md"
API_DEPENDENCY_FILE="api_dependency_map.md"
API_ASYNC_PROCESSING="api_async_processing.md"
API_NFR="api_nfr.md"
API_BUSINESSLOGIC="api_businesslogic.md"
API_DATAMODELS="api_datamodels.md"
API_SCHEMA="api_schema.md"
API_AUTHFLOWS="api_authflows.md"
API_ANALYZE="api_analyze.md"

# 4. Write the variables to a new config.sh file.
cat > config.sh << EOL
#!/bin/bash

# -- Paths --
export WORKSPACE_PATH="$WORKSPACE_PATH"
export REPO_PATH="$REPO_PATH"
export OUTPUT_PATH="$SCRIPT_DIR"

# -- Output Files --
export API_INVENTORY_FILE="$API_INVENTORY_FILE"
export API_DEPENDENCY_FILE="$API_DEPENDENCY_FILE"
export API_ASYNC_PROCESSING="$API_ASYNC_PROCESSING"
export API_NFR="$API_NFR"
export API_BUSINESSLOGIC="$API_BUSINESSLOGIC"
export API_DATAMODELS="$API_DATAMODELS"
export API_SCHEMA="$API_SCHEMA"
export API_AUTHFLOWS="$API_AUTHFLOWS"
export API_ANALYZE="$API_ANALYZE"
EOL

echo
echo "✅ Configuration saved successfully to 'config.sh'!"
