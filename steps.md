## Step 1: 

codmod create full -c moneynote-api/ \
--format markdown \
-o customized_report_money_note_detailed_journeys.md \
--context-file context-file.md

codmod create data-layer -c moneynote-api/ \
--format markdown \
-o customized_report_money_note_data_layer.md

## Step 3:

For each user journey:

Look at the customized_report_money_note_detailed_journeys.md file, and the customized_report_money_note_data_layer.md file. These files represent a report for code in moneynote-api directory. As a senior business analyst Document "Journey 5: Supporting Multiple Currencies". Document your results in an .md file with the following content:

* Detailed user journey and flows. If there are multiple journeys include one section for each journey.
* Detailed object level data structures. For each data structure, capture the data attributes as present in code or the database.
* Database tables to be updated
* API Calls that are made.
* Business rules and functionality (include code snippets from original code to make it clearer)
* Detailed Test cases
* State any assumptions

Refer back to the original code to get a better understanding. User example_user_journey.md as an example file, follow the format and structure of that file.

## Step 4:
As a senior business analyst, craft out an introduction to a functional specification document, covering the following 3 areas. 

Purpose of the Document: Explains why this functional specification is needed.
Goals and Objectives: The high-level goals the system aims to achieve.
Scope: Defines what is included and excluded from the project.

Use the following files to guide you:

* customized_report_money_note_detailed_journeys.md
* customized_report_money_note_data_layer.md

and all user journey files in this folder.

Save the file to the following absolute path {file_name} file

## Step 5: Consolidation

gen_fs.py

