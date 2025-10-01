from string import Template

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

# Data ERD

"""
Args:
    application_directory: The relative directory of the source code of the existing application
    database_design_absolute_file_path: absolute path of the database design document
    absolute_file_path: The absolute file path for saving the introduction for the functional specifications
"""

database_erd_prompt_string = f"""

You are an expert database architect. Your task is to create an Entity-Relationship Diagram (ERD) based on the provided documentation and source code.

## Context & Sources

Primary Source for Entities: $database_design_absolute_file_path

Use this directory to identify all tables (entities), their columns (attributes), primary keys, and foreign keys.

Source for Business Logic: @docs/user_journeys

Use these user flows to understand how entities relate to each other in practice and to infer relationships that might not be explicit in the schema.

Definitive Reference (if needed): $application_directory

If the documentation is ambiguous or conflicting, refer to the application's source code as the ultimate source of truth for database interactions.

## Task & Instructions

Identify Entities & Attributes: Systematically go through the files in @docs/database_design to list all database tables and their columns.

Determine Relationships & Cardinality: For each entity, identify its relationship to other entities.

Use foreign key constraints defined in the schema as the primary evidence.

Verify these relationships against the logic described in @docs/user_journeys.

The relationship must be one of the following: one-to-one (1--1), one-to-many (|o--||), or many-to-many.

Generate ERD Code: Create the ERD using Mermaid JS syntax. This is a text-based format that can be rendered into a visual diagram.

Clearly label Primary Keys (PK) and Foreign Keys (FK) for each attribute.

Use Crow's Foot notation for relationships.

Add a descriptive label to each relationship line (e.g., places, contains, manages).

## Example

If the documentation described users and orders tables, the Mermaid JS output should look like this:

Code snippet

erDiagram
    users {{
        int id PK "User ID"
        string name
        string email
    }}
    orders {{
        int id PK "Order ID"
        int user_id FK "User reference"
        datetime created_at
        decimal amount
    }}

    users ||--|o orders : "places"
## Output

Generate a single code block containing the complete ERD in Mermaid JS syntax. Ensure all tables from the database design are included. Save the generated Mermaid JS code to the following absolute path: $absolute_file_path.

"""


database_specification_prompt_template = Template(database_specification_prompt_string)
database_erd_prompt_template = Template(database_erd_prompt_string)