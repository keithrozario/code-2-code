import os

# Base Directories
WORKING_DIRECTORY = os.getcwd()
SOURCE_CODE_DIRECTORY = os.path.join(WORKING_DIRECTORY, "moneynote-api")
DOCS_DIRECTORY = os.path.join(WORKING_DIRECTORY, "docs")
NEW_APP_DIRECTORY = os.path.join(WORKING_DIRECTORY, "new_app")

# Codmod Reports
CODMOD_REPORT_PATH = os.path.join(DOCS_DIRECTORY, "codmod_reports", "customized_report_money_note_detailed_journeys.md")
CODMOD_DATA_REPORT_PATH = os.path.join(DOCS_DIRECTORY, "codmod_reports", "customized_report_money_note_data_layer.md")

# User Journeys
USER_JOURNEY_DIRECTORY_PATH = os.path.join(DOCS_DIRECTORY, "user_journeys")

# BRDs
BRDS_DIRECTORY_PATH = os.path.join(DOCS_DIRECTORY, "brds")

# Functional Specs
FUNCTIONAL_SPECS_PATH = os.path.join(DOCS_DIRECTORY, "functional_specs_introduction.md")

# Context Docs
ARCHITECTURE_PRINCIPLES_PATH = os.path.join(DOCS_DIRECTORY, "context_docs", "architecture_principles.md")

# Database Paths
DATABASE_DEFINITION_PATH = os.path.join(DOCS_DIRECTORY, "database_design", "database_definition.md")
DATABASE_ERD_PATH = os.path.join(DOCS_DIRECTORY, "database_design", "database_erd.md")

# API Design Paths
API_DEFINITION_PATH = os.path.join(DOCS_DIRECTORY, "api_design", "api_definition.md")
API_DEPENDENCIES_PATH = os.path.join(DOCS_DIRECTORY, "api_design", "api_dependencies.md")
API_PLAN_PATH = os.path.join(DOCS_DIRECTORY, "api_design", "api_plan.md")
API_DETAIL_DESIGN_PATH = os.path.join(DOCS_DIRECTORY, "api_design", "api_detail_design.md")

# PRD Paths
PRDS_DIRECTORY = os.path.join(DOCS_DIRECTORY, "prds")
EXAMPLE_PRD_PATH = os.path.join(PRDS_DIRECTORY, "example.md")

# Taskmaster Paths
TASKMASTER_STATUS_FILE = os.path.join(WORKING_DIRECTORY, ".taskmaster", "current_status.md")
TASKMASTER_JSON_FILE = os.path.join(WORKING_DIRECTORY, ".taskmaster", "tasks", "tasks.json")
