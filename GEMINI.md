# Project: Money-note rewrite

## Introduction

The project will re-write money note from Java to a new tech stack written below.

In version 1 we will retain all functionality in moneynote and only perform a technical re-write.

## Tech Stack

* The backend is API driven, written in Python using Fast API.
* The Database is a SQLite3 file named `moneynote.db`
* The Database will implement exactly the data model used in the old version.
* The frontend will be implemented react-js
* Any authentication of the user will be done by an API gateway, we will not perform authentication in code here.
* The api will write directly into the database
* There will always be a JWT token in the request, requests without JWT tokens will be rejected by the API Gateway.

## App

* The app is in the `./app` directory. 

## Database

* Reimplement the database in SQLite3 by implementing the models in code.
* The database is in `./app/db/moneynote.db` there is only one database, use this.
* The database definition is in `./technical_design/database_design/database_schema.md`

## Backend
* The backend is API driven, written in Python and based on Fast API
* Use `uv` for the package management, namely
  * Use `uv add` instead of pip install
  * Assume that you are already in the virtual environment
* Execute test by `PYTHONPATH=. pytest` command

# Task Master AI - Agent Integration Guide`

## Daily Development Workflow
task-master list                                   # Show all tasks with status
task-master next                                   # Get next available task to work on
task-master show <id>                             # View detailed task information (e.g., task-master show 1.2)
task-master set-status --id=<id> --status=done    # Mark task complete

# Task Management
task-master add-task --prompt="description" --research        # Add new task with AI assistance
task-master expand --id=<id> --research --force              # Break task into subtasks
task-master update-task --id=<id> --prompt="changes"         # Update specific task
task-master update --from=<id> --prompt="changes"            # Update multiple tasks from ID onwards
task-master update-subtask --id=<id> --prompt="notes"        # Add implementation notes to subtask

# Analysis & Planning
task-master analyze-complexity --research          # Analyze task complexity
task-master complexity-report                      # View complexity analysis
task-master expand --all --research                # Expand all eligible tasks
### Core Files

- `.taskmaster/tasks/tasks.json` - Main task data file (auto-managed)
- `.taskmaster/config.json` - AI model configuration (use `task-master models` to modify)
- `.taskmaster/docs/prd.txt` - Product Requirements Document for parsing
- `.taskmaster/tasks/*.txt` - Individual task files (auto-generate from tasks.json)

### Directory Structure

```
project/
├── .taskmaster/
│   ├── tasks/              # Task files directory
│   │   ├── tasks.json      # Main task database
│   │   ├── task-1.md      # Individual task files
│   │   └── task-2.md
│   ├── docs/              # Documentation directory
│   │   ├── prd.txt        # Product requirements
│   ├── reports/           # Analysis reports directory
│   │   └── task-complexity-report.json
│   ├── templates/         # Template files
│   │   └── example_prd.txt  # Example PRD template
│   └── config.json        # AI models & settings
├── .claude/
│   ├── settings.json      # Claude Code configuration
│   └── commands/         # Custom slash commands
├── .env                  # API keys
├── .mcp.json            # MCP configuration
└── CLAUDE.md            # This file - auto-loaded by Claude Code
```
### Task ID Format

- Main tasks: `1`, `2`, `3`, etc.
- Subtasks: `1.1`, `1.2`, `2.1`, etc.
- Sub-subtasks: `1.1.1`, `1.1.2`, etc.

### Task Status Values

- `pending` - Ready to work on
- `in-progress` - Currently being worked on
- `done` - Completed and verified
- `deferred` - Postponed
- `cancelled` - No longer needed
- `blocked` - Waiting on external factors

### Task Fields

```json
{
  "id": "1.2",
  "title": "Implement user authentication",
  "description": "Set up JWT-based auth system",
  "status": "pending",
  "priority": "high",
  "dependencies": ["1.1"],
  "details": "Use bcrypt for hashing, JWT for tokens...",
  "testStrategy": "Unit tests for auth functions, integration tests for login flow",
  "subtasks": []
}
