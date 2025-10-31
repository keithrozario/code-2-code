from string import Template

# User Journey Prompt

"""
The prompt below is entered into gemini-cli for generating a user-journey file. 
Args:
    codmod_detailed_relative_file_path: CodMod user_joiurney report relative file path
    codmod_data_relative_file_path: CodMod data report relative file path
    user_journey_name: The Name of the user journey
    absolute_file_path: The absolute file path for saving the user_journey file
    source_code_directory: The relative source code directory
"""

user_journey_prompt_string = """
You are a senior business analyst. Your task is to create a comprehensive User Journey Analysis Document for `$user_journey_name`.

## Context & Sources

*   **Source for Code Analysis:** `$codmod_detailed_relative_file_path` and `$codmod_data_relative_file_path` (These are reports from a tool called CodMod).
*   **Definitive Reference for Implementation:** The $source_code_directory source code directory.

## Instructions

1.  Your task is to create a comprehensive analysis document by synthesizing information from the provided CodMod reports and the application source code.
2.  Do not capture functionality or data structures that are not documented in the system. Do not create new requirements or functionality.
3.  Only focus on the specific user journey you're given (`$user_journey_name`). Do not include details that are not related to this user journey.
4.  The primary objective is to ensure that all documented details are:
    *   **Accurate:** Directly traceable to the source code or analysis reports.
    *   **Comprehensive:** Covering all aspects of the user journey as defined in the structure below.
    *   **Clear:** Written in a way that is easy for both technical and non-technical stakeholders to understand.

## Analysis and Synthesis

*   **Analyze the Code Reports:** Use the CodMod reports to understand the high-level flows, data interactions, and business logic related to the user journey.
*   **Analyze the Source Code:** Refer to the $source_code_directory directory to extract precise details about data models, business rules, and step-by-step processes that the reports might not fully capture.
*   **Synthesize and Structure:** Generate the final document using the precise markdown structure provided below. Do not deviate from these sections.

## Document Structure to Generate

# User Journey Analysis: $user_journey_name

### 1.0 Detailed User Journeys and Flows
(Capture the step-by-step interactions a user has with the system to achieve the specific business goal of this journey. Document each distinct flow, including user actions, system responses, decision points, alternative paths, and error handling. Clearly identify start and end points.)

---

### 2.0 Detailed Object Level Data Structures
(Document the structure and attributes of key data entities involved in this journey. For each entity, list its attributes, data types, constraints (e.g., `NOT NULL`, `FOREIGN KEY`), and a brief description. Indicate relationships between entities.)

---

### 3.0 Database Tables to be Updated
(Identify which database tables are directly impacted by this user journey. List the tables that are read from and written to (`INSERT`, `UPDATE`, `DELETE`). Specify the operations performed on each table within the context of the journey.)

---

### 4.0 Business Rules and Functionality (Detailed)
(Capture the explicit and implicit logic governing the system's behavior for this journey. For each rule, specify its name, description, trigger, logic, and outcome. Detail both front-end and back-end validations.)

---

### 5.0 Test Cases
(Create a comprehensive set of test cases to verify the correct implementation of the user journey and its business rules. Each test case should include an ID, the feature being tested, preconditions, steps, test data, and expected results. Cover happy paths, negative paths, boundary conditions, and error handling.)

---

### 6.0 Assumptions
(Document any assumptions made during the analysis due to ambiguity or lack of definitive information. Explain the reasoning for each assumption.)

---

Create the document in markdown format, and output to `$absolute_file_path`.

Please generate the complete and final response without stopping or asking for confirmation to continue.

"""

# Functional Spec Introduction

"""
Args:
    application_directory: The relative directory of the source code of the existing application
    absolute_file_path: The absolute file path for saving the introduction for the functional specifications
"""

functional_specification_intro_prompt_string = f"""
As a senior business analyst, craft out an introduction to a functional specification document, covering the following 3 areas. 

Purpose of the Document: Explains why this functional specification is needed.
Goals and Objectives: The high-level goals the system aims to achieve.
Scope: Defines what is included and excluded from the project.

Use the following files to guide you:

* customized_report_money_note_detailed_journeys.md
* customized_report_money_note_data_layer.md

and all user journey files in this folder.

Save the file to the following absolute path $absolute_file_path file
"""

# BRD Doc Generation
"""
Args:
    $user_journey_absolute_path: Absolute path to the specific user_journey
    $application_directory: Path to the application directory
    $absolute_file_path: Absolute path of the file for output
"""


brd_prompt_string = f"""

You are a senior business analyst, write a detailed business requirement document that covers all the user journeys in the application.

## Context & Sources

Source for Business Logic: $user_journey_absolute_path
Source for Application logic and high level Business Requirements Documents: @docs/codmod_reports/**
Definitive Reference : $application_directory

Your task is to create a comprehensive Business Requirement Document (BRD) by analyzing and synthesizing information from two provided sources: 
1) User Journey Documentation
2) A application level report from a tool called CodMod
3) The source code of the application
4) Do not capture requirements that are not documented in the system, do not create new requirements.
5) Only focus on the specific uiser journey you're given. Do not include requirements that are not related to this user journey.

The primary objective is to ensure that all business requirements listed in the BRD:
    * Specific: Clearly and unambiguously state what needs to be accomplished.
    * Measurable: Define quantifiable criteria for success.
    * Agreed Upon: Frame the requirement in a way that is ready for stakeholder validation.
    * Realistic: The requirement must be achievable given the context of the existing system and project constraints.

All requirements must be traced by to the actual code that implements it, do not create new requirements.

Instructions:

Analyze the User Journey: Extract the "what" and "why" from the user's perspective. Identify user goals, actions, and expected outcomes. This will form the basis of the functional requirements.

Analyze the Code/System Summary: Understand the current system's capabilities, architecture, and constraints. This will ensure that the proposed requirements are realistic and will inform the non-functional requirements and technical constraints.

Synthesize and Structure: Generate the BRD using the precise markdown structure provided below. Do not deviate from these sections.

Formulate SMART Requirements: For every requirement in Section 5, write it as a clear, complete SMART statement.

Bad Example: "The user should be able to see their profile."

Good SMART Example: "The user profile page must display the user's full name, email, and profile picture within 1.5 seconds of page load. Success will be measured by a 99% success rate during User Acceptance Testing (UAT). This is achievable using the existing user database and is targeted for completion in the Q4 2025 development sprint."

BRD Structure to Generate
# Business Requirement Document: [Project Name]

## 1.0 Summary
(Provide a high-level overview of the project, its purpose, and the key business objectives it aims to achieve. Summarize the problem, the proposed solution, and the expected business value.) 

---

## 2.0 Project Scope
### 2.1 In-Scope
(Create a bulleted list of all major features, functionalities, and deliverables that are included in this project, derived directly from the user journey.)

### 2.2 Out-of-Scope
(Create a bulleted list of features or functionalities that are explicitly not part of this project to prevent scope creep.)

---

## 3.0 Business Requirements
(This is the most critical section. Analyze the provided documents to formulate the following requirements as SMART statements.)

BR-001: [Insert SMART requirement here] # or follow any requirements ID present in the the input files.
BR-002: [Insert SMART requirement here]
BR-003: [Insert SMART requirement here]

### 3.1 Functional Requirements
(List the specific functionalities the system must have. Each item must be a full SMART requirement.)

FR-001: [Insert SMART requirement here]
FR-002: [Insert SMART requirement here]
FR-003: [Insert SMART requirement here]

---
## 4.0 Assumptions, Constraints, and Dependencies
### 4.1 Assumptions
(List any assumptions being made that could impact the project if they turn out to be false.)

### 4.2 Dependencies
(List any external factors or other projects that this project depends on.)

Create the document in markdown format, and output to $absolute_file_path

Please generate the complete and final response without stopping or asking for confirmation to continue.
"""

user_journey_prompt_template = Template(user_journey_prompt_string)
functional_specification_intro_prompt_template = Template(functional_specification_intro_prompt_string)
brd_prompt_template = Template(brd_prompt_string)