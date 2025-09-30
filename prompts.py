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

# Data Layer

"""
Args:
    application_directory: The relative directory of the source code of the existing application
    absolute_file_path: The absolute file path for saving the introduction for the functional specifications
"""

database_specification_prompt_string = f"""
Look through @docs/** folder, these files describe an application in the $application_directory. Document the database tables and elements of this database in a markdown file.

Create a separate section for each database table. For each column of each table, document the following:
* Name: The Name of the column
* Description: A description of the data stored in this column
* Current Data type: The existing datatype in the current application
* SQLite Data type: provide a SQLite3 type and description. Refer to "https://www.sqlite.org/datatype3.html" for more information on SQLite3 datatypes. Estimate based on what the current datatype is based on the current data type.
* Key Type: Documents if this column is a Primary or Foreign Key

If you need, you can reference the source code in the $application_directory.

Save the file to the following absolute path $absolute_file_path.

"""


# Api Layer

## API Definition
"""
Args:
    application_directory: The relative directory of the source code of the existing application
    absolute_file_path: The absolute file path for saving the introduction for the functional specifications
"""

api_specification_prompt_string = f"""
Look through @docs/** folder, these files describe an application in the $application_directory. Document All the API calls:

For each API call include the following information:
* All Request Parameter in the path paremeter, query string parameter or body parameter
* All Response parameters in the body
* Any headers that should be set in the request
* Any headers that should be expected in the response

For each parameter in the request and response document the:
* Name: The Name of the parameter
* Description: A description of the parameter from a business context
* Type: In the path, url or body
* Data type: The datatype of the parameter
* Type: One of Path, QueryString, Body
* Optionality: If the parameter is optional or mandatory

If you need, you can reference the source code in the $application_directory.
"""

## API Dependencies
"""
Args:
    application_directory: The relative directory of the source code of the existing application
    absolute_file_path: The absolute file path for saving the introduction for the functional specifications
    user_journey_absolute_directory: The relative path to the user journeys
    api_definition_absolute_path: relative path to the api_definition
"""

api_dependency_prompt_string = f"""
The api definition file $api_definition_absolute_path defines a list of API endpoints

For each endpoint look at the parameters it consumes as input and output to determine what dependencies are needed by this api. 

For example:
* a user must be created before a user can login. Hence any login api depends on the user creation.
* a transaction must be created before it can be reversed. Hence a reversal api depends on a transaction creation api.

Document all the dependencies for each api endpoint in markdown format. Save the file to the following absolute path $absolute_file_path.

Please generate the complete and final response without stopping or asking for confirmation to continue.
"""

## API Plan
"""
Args:
    absolute_file_path: The absolute file path for saving the introduction for the functional specifications
    api_definition_absolute_path : The absolute path of the API definition file
    api_dependency_absolute_path : The absolute path of the api dependency file
"""

api_plan_prompt_string = f"""
The api definition file $api_definition_absolute_path defines a list of API endpoints

The api dependency file $api_dependency_absolute_path defines the dependencies between the endpoints.

Using these two input file create a plan to build the backend API endpoints, listing out each API that has to be built in order. To ensure that an API endpoint is only built AFTER it's dependencies are built.

Create the plan in markdown format, and output to $absolute_file_path

Please generate the complete and final response without stopping or asking for confirmation to continue.
"""


## Templates
user_journey_prompt_template = Template(user_journey_prompt_string)
functional_specification_intro_prompt_template = Template(functional_specification_intro_prompt_string)
database_specification_prompt_template = Template(database_specification_prompt_string)
api_specification_prompt_template = Template(api_specification_prompt_string)
api_dependency_prompt_template = Template(api_dependency_prompt_string)
api_plan_prompt_template = Template(api_plan_prompt_string)