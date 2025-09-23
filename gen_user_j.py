from helper_funcs import get_md_analyzer_and_content
import subprocess
import os

def run_gemini_prompt(prompt: str)->bool:

    try:
        result = subprocess.run([
            'gemini',
            '-y',
            '-p',
            prompt
        ], capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing shell command: {e}")
        print(f"Stderr: {e.stderr}")
        return False
    
    return True


code_mod_report = "customized_report_money_note_detailed_journeys.md"

analyzer, content = get_md_analyzer_and_content(code_mod_report)
headers =  analyzer.identify_headers()['Header']


# The prompt specifies creating a new section called "User Journeys"
journey_header = [header for header in headers if "User Journeys" in header['text']][0]

# Find the next headers with -1 level of heading.
in_user_journey_section = False
start_level = 0
user_journey_header_texts = []
for header in headers:
    if header['text'] == "User Journeys":
        start_level = header['level']
        in_user_journey_section = True
        continue # skip next block and jump to next header
    
    if in_user_journey_section:
        if header['level'] == (start_level+1):
            user_journey_header_texts.append(header['text'])
        elif header['level'] <= start_level:
            in_user_journey_section = False
            break # we're done, avoid duplicate User Journey Sessions

print("Found the following user_journeys")
for user_journey_name in user_journey_header_texts:
    print(user_journey_name) 

for user_journey_name in user_journey_header_texts:
    file_name = f"{os.getcwd()}/user_journeys/{user_journey_name.replace(' ','_')}.md"
    prompt = f"""
    Look at the customized_report_money_note_detailed_journeys.md file, and the customized_report_money_note_data_layer.md file. 
    These files represent a report for code in moneynote-api directory. 
    As a senior business analyst Document {user_journey_name}. Document your results in an .md file with the following content:
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


    Generate the output to markedown, and save the file to the following absolute path {file_name} file.
    Refer to the original code for further context
    """
    while not os.path.exists(f"{file_name}"):
        print(f"\nNow creating for {user_journey_name}")
        run_gemini_prompt(prompt=prompt)
    print(f"Yay! File created: {file_name}")
    



# Run prompt for functional specificaiton introduction
file_name = f"{os.getcwd()}/functional_specs_introduction.md"
prompt = f"""
As a senior business analyst, craft out an introduction to a functional specification document, covering the following 3 areas. 

Purpose of the Document: Explains why this functional specification is needed.
Goals and Objectives: The high-level goals the system aims to achieve.
Scope: Defines what is included and excluded from the project.

Use the following files to guide you:

* customized_report_money_note_detailed_journeys.md
* customized_report_money_note_data_layer.md

and all user journey files in this folder.

Save the file to the following absolute path {file_name} file
"""

while not os.path.exists(file_name):
    run_gemini_prompt(prompt=prompt)
print(f"Yay! File created: {file_name}")
