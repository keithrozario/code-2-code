from string import Template

# User Journey Prompt

"""
The prompt below is entered into gemini-cli for generating a user-journey file. 
Args:
    codmod_detailed_relative_file_path: CodMod user_joiurney report relative file path
    codmod_data_relative_file_path: CodMod data report relative file path
    user_journey_name: The Name of the user journey
    absolute_file_path: The absolute file path for saving the user_journey file
"""

user_journey_prompt_string = """
    Look at the $codmod_detailed_relative_file_path file, and the $codmod_data_relative_file_path file. 
    These files represent a report for code in moneynote-api directory. 
    As a senior business analyst Document $user_journey_name. Document your results in an .md file with the following content:
---

**1. Detailed User Journeys and Flows**

*   **Objective:** To capture the step-by-step interactions a user has with the system to achieve a specific business goal.
*   **Requirements:**
    *   Document each distinct and significant user journey.
    *   For each journey, provide a clear, sequential description of user actions and system responses.
    *   Include decision points, alternative paths, and error handling scenarios within the flow.
    *   Visual representation (e.g., flowcharts, sequence diagrams) is highly encouraged to illustrate the flow.
    *   Clearly identify the start and end points of each journey.
    *   If multiple journeys lead to similar outcomes with variations, document these variations.

**2. Detailed Object Level Data Structures**

*   **Objective:** To meticulously document the structure and attributes of key data entities within the system.
*   **Requirements:**
    *   Identify and list all significant data entities (e.g., Customer, Order, Product, Invoice, User Account).
    *   For each entity, list all its data attributes as they exist in the code or database.
    *   For each attribute, capture:
        *   Attribute Name (exact name from code/database).
        *   Data Type (e.g., `string`, `integer`, `boolean`, `datetime`, `decimal`, `enum`, `complex_object`).
        *   Constraints or Properties (e.g., `NOT NULL`, `UNIQUE`, `PRIMARY KEY`, `FOREIGN KEY`, `maxLength`, `defaultValue`, `isEncrypted`).
        *   A brief description of what the attribute represents.
    *   Indicate relationships between entities where relevant (e.g., One-to-Many, Many-to-Many).

**3. Database Tables to be Updated**

*   **Objective:** To identify which database tables are directly impacted by user actions and system processes.
*   **Requirements:**
    *   For each documented user journey and major functional area, list the specific database tables that are:
        *   Read from (e.g., for data retrieval).
        *   Written to (e.g., `INSERT`, `UPDATE`, `DELETE` operations).
    *   Specify the typical operations performed on each table within the context of the documented functionality.

**4. Business Rules and Functionality (Detailed)**

*   **Objective:** To capture the explicit and implicit logic that governs the system's behavior and data integrity.
*   **Requirements:**
    *   Provide a detailed description of all identified business rules.
    *   For each rule, specify:
        *   **Rule Name/Identifier:** A concise name for the rule.
        *   **Description:** A clear explanation of the rule.
        *   **Triggering Event:** What action or condition initiates this rule?
        *   **Logic/Conditions:** The specific criteria, calculations, or conditional statements involved.
        *   **Outcome/Action:** What happens when the rule is met or violated?
    *   **Validations (Front-end and Back-end):**
        *   **Front-end Validations:** Detail any checks performed on the user interface to guide user input and provide immediate feedback (e.g., "required field," "email format," "numeric range").
        *   **Back-end Validations:** Detail any checks performed on the server-side to ensure data integrity, security, and adherence to business logic (e.g., "inventory check," "user permissions," "data consistency checks"). For each validation, describe the rule being enforced and the consequence of failure.

**5. Detailed Test Cases**

*   **Objective:** To create a comprehensive set of test cases that can verify the correct implementation of user journeys and business rules.
*   **Requirements:**
    *   Develop detailed test cases for each significant user journey and business rule.
    *   Each test case should include:
        *   **Test Case ID:** A unique identifier.
        *   **Feature/User Story/Rule Being Tested:** Clear reference to the item under test.
        *   **Preconditions:** Any setup required before executing the test.
        *   **Test Steps:** A precise, sequential list of actions to perform.
        *   **Test Data:** Specific input data required for the test.
        *   **Expected Result:** The anticipated outcome of performing the test steps with the given data.
    *   Include test cases for:
        *   **Happy Paths:** Valid scenarios.
        *   **Negative Paths:** Invalid inputs and error conditions.
        *   **Boundary Conditions:** Testing limits and edge cases of data inputs.
        *   **Error Handling:** Verifying how the system responds to exceptions and invalid states.

**6. State Any Assumptions**

*   **Objective:** To document any assumptions made during the extraction process due to ambiguity or lack of definitive information.
*   **Requirements:**
    *   List all assumptions clearly and concisely.
    *   For each assumption, explain the reasoning or the gap in information that led to it.
    *   These assumptions are critical for understanding the context and potential areas for further investigation.


    Generate the output to markedown, and save the file to the following absolute path $absolute_file_path file.
    Refer to the original code for further context
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