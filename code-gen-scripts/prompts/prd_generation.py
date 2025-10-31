from string import Template

"""
Args:
    $absolute_file_path: Absolute file path of the output file
    $phase_number: Phase of the plan we are generating PRD for
    $example_prd_file_path: Example PRD File Path
"""

prd_prompt_string = """

You are a Senior Developer. Your task is to create a Product Requirement documentation for a backend API. 

The API is to be built in phases, and currently we're in Phase $phase_number. All previous phases have been committed are reside in the directory location $new_app_directory.

Refer to this directory to ensure we build on it.

## Context & Sources

Primary Source for Entities: @docs/api_design/api_definition.md @docs/api_detail_design.md which describes the backend APIs.
Source for Business Logic: @docs/user_journeys

The phases for the API build are in @docs/api_design/api_plan.md, look through the plan for Phase $phase_number

Example PRD (if needed): $example_prd_file_path

If the documentation is ambiguous or conflicting, refer to the application's source code as the ultimate source of truth for database interactions.

## Task & Instructions 

Create a PRD with the following format:

1) Goal & Scope : High-level overview of the Goal and Scope of this PRD, as the API is built in Phases this should be a short description (2-3 sentences)
2) Functional Specifications: The Functional Specifications of what is being built by the API
3) UI / UX Flow: Describes the expected UI/UX flow. However, we will only build the backend API
4) Technical Specifications: Describes the Technical Specification of the API
4.1 API Logic : For each api endpoint:
* Descibe the business logic. Include sample code is necessary.
* Include all request parameters in line with @docs/api_design/api_definition.md
* Include all possible responses and scenarios
* Include all database CRUD operations
* Include all database SQL Statements

5) Data Model: Define the Data Model that is affected here.
6) Test Cases: A detailed list of test cases pertaining to the api endpoints. Refer to @docs/user_journeys, and @docs/brds if necessary.
7) Risks & Mitigations
8) Open Questions
9) Task Seeds (for Agent Decomposition: Breakdown task to fine-grain operation

Document the output in markdown format. Save the file to the following absolute path $absolute_file_path.

Please generate the complete and final response without stopping or asking for confirmation to continue.

"""
prd_prompt_template = Template(prd_prompt_string)
