from string import Template

## API Definition
"""
Args:
    application_directory: The relative directory of the source code of the existing application
    absolute_file_path: The absolute file path for api definition file
"""

api_specification_prompt_string = f"""
Look through @docs/** folder, these files describe an application in the $application_directory.

Document All the API calls:

For each API call include the following information:
* All Request Parameter in the path paremeter, query string parameter or body parameter
* All Response parameters in the body
* Any headers that should be set in the request
* Any headers that should be expected in the response

For each parameter in the request and response document in a table format:
* Name: The Name of the parameter
* Description: A description of the parameter from a business context
* Type: In the path, url or body
* Data type: The datatype of the parameter
* Type: One of Path, QueryString, Body
* Optionality: If the parameter is optional or mandatory

Document the output in markdown format. Save the file to the following absolute path $absolute_file_path.

Please generate the complete and final response without stopping or asking for confirmation to continue.
"""

## API Dependencies
"""
Args:
    application_directory: The relative directory of the source code of the existing application
    absolute_file_path: The absolute file path of the api dependency file
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
    absolute_file_path: The absolute file path of the api plan file
    api_definition_absolute_path : The absolute path of the API definition file
    api_dependencies_absolute_path : The absolute path of the api dependency file
"""

api_plan_prompt_string = f"""
The api definition file $api_definition_absolute_path defines a list of API endpoints

The api dependency file $api_dependencies_absolute_path defines the dependencies between the endpoints.

Using these two input file create a plan to build the backend API endpoints, listing out each API that has to be built in order.
To ensure that an API endpoint is only built AFTER it's dependencies are built.

The plan should be staggered into phases, with each phase consisting of no more than 5 new endpoints, that can be built and tested.

A phase can consist of just a single API endpoint, but not more than 5.

Create the plan in markdown format, and output to $absolute_file_path

Please generate the complete and final response without stopping or asking for confirmation to continue.
"""

## API Design Document
"""
Args:
    absolute_file_path: The absolute file path for saving the introduction for the api design doc
    api_definition_absolute_path : The absolute path of the API definition file
    api_dependencies_absolute_path : The absolute path of the api dependency file
    api_plan_absolute_path : The absolute path of the api design document
"""

api_design_prompt_string = f"""
The api definition file $api_definition_absolute_path defines a list of API endpoints

The api dependency file $api_dependencies_absolute_path defines the dependencies between the endpoints.

The api plan file $api_plan_absolute_path defines the plan for building the api

The architecture principles document $architecture_principles_absolute_path is are the architecture principles for designing a new API

Using these 3 input files create a design document that outlines the design of a new backend API that follows the architecture principles provided.

The detailed design document should provide:
* The overall architecture of the API
* The design considerations
* The overall structure of files to create for the API

Create the plan in markdown format, and output to $absolute_file_path

Please generate the complete and final response without stopping or asking for confirmation to continue.
"""


## Templates
api_specification_prompt_template = Template(api_specification_prompt_string)
api_dependency_prompt_template = Template(api_dependency_prompt_string)
api_plan_prompt_template = Template(api_plan_prompt_string)
api_design_prompt_template = Template(api_design_prompt_string)


