#!/bin/bash
set -e

echo "--- Asynchronous Processing Analysis Script ---"

source config.sh

echo "DEBUG: Repository to analyze is [$REPO_PATH]"
echo "DEBUG: Output will be saved to [$OUTPUT_PATH/$API_ASYNC_PROCESSING]"

# --- FIX: Change directory to the repository to set the workspace ---
echo "DEBUG: Setting workspace to repository path..."
cd "$REPO_PATH" || exit 1
# -----------------------------------------------------------------

PROMPT_TEXT="You are an expert code analyst. Analyze the repository at '$REPO_PATH'.

Your task is to scan the entire repository for evidence of asynchronous processing. Look for:

1.  Usage of message queue clients (like RabbitMQ, Kafka, SQS).
2.  Usage of background job libraries (like Celery, Sidekiq).
3.  Framework-specific asynchronous annotations (like \`@Async\` in Spring).

For each instance you find, identify the function that produces the message/job and, if possible, the function that consumes/handles it. Please structure your findings clearly.

Your response must begin directly with the Markdown table and contain no introductory sentences."

echo "DEBUG: Running analysis..."

# The output path needs to be absolute
gemini chat "$PROMPT_TEXT" > "$OUTPUT_PATH/$API_ASYNC_PROCESSING"

echo
echo "✅ Done! Report saved to '$OUTPUT_PATH/$API_ASYNC_PROCESSING'."
