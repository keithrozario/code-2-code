import os
from typing import List

import prompts
from helper_funcs import get_md_analyzer_and_content, run_till_file_exists



codmod_report = "./docs/codmod_reports/customized_report_money_note_detailed_journeys.md"
codmod_data_report = "./docs/codmod_reports/customized_report_money_note_data_layer.md"
user_journey_relative_directory = "user_journeys"
absolute_path_docs_directory = f"{os.getcwd()}/docs"

def get_user_journey_header_texts (codmod_report: str) -> List[str]:
    """
    Parses the markdown file and returns the list of headers from the user_journey sections e.g. "Journey 1: Monitoring Financial Situation"
    """
    analyzer, content = get_md_analyzer_and_content(codmod_report)
    headers =  analyzer.identify_headers()['Header']

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
                break # we're done, avoid duplicate User Journey Sessions by breaking here.
        
    return user_journey_header_texts


## User Journeys

user_journey_header_texts = get_user_journey_header_texts(codmod_report=codmod_report)
print("Identified the following user_journeys")
for user_journey_name in user_journey_header_texts:
    print(user_journey_name) 

user_journey_directory = f"{absolute_path_docs_directory}/{user_journey_relative_directory}"
for user_journey_name in user_journey_header_texts:
    absolute_file_path = f"{user_journey_directory}/{user_journey_name.replace(' ','_')}.md"
    prompt = prompts.user_journey_prompt_template.substitute(
        codmod_detailed_relative_file_path = codmod_report,
        codmod_data_relative_file_path = codmod_data_report,
        user_journey_name = user_journey_name,
        absolute_file_path = absolute_file_path
    )
    run_till_file_exists (
        prompt=prompt,
        absolute_file_path=absolute_file_path,
        step_description=f"\nGenerating {user_journey_name} documentation in {absolute_file_path}"
    )

# Functional Specification Intro   

func_specs_file_path = f"{absolute_path_docs_directory}/functional_specs_introduction.md"
prompt = prompts.functional_specification_intro_prompt_template.substitute(
    absolute_file_path = func_specs_file_path
)
run_till_file_exists (
    prompt=prompt,
    absolute_file_path=func_specs_file_path,
    step_description=f"\nGenerating functional_specs_introduction.md"
)


# Database Design
database_definition_file_path = f"{absolute_path_docs_directory}/database_design/database_definition.md"
prompt = prompts.database_specification_prompt_template.substitute(
    application_directory="moneynote-api/",
    absolute_file_path=database_definition_file_path
)
run_till_file_exists (
    prompt=prompt,
    absolute_file_path=database_definition_file_path,
    step_description=f"\nGenerating database_definition.md"
)

# Api Definitition

## Api Specification
api_definition_file_path = f"{absolute_path_docs_directory}/api_design/api_definition.md"
prompt = prompts.api_specification_prompt_template.substitute(
    application_directory="moneynote-api/",
    absolute_file_path=api_definition_file_path
)
run_till_file_exists (
    prompt=prompt,
    absolute_file_path=api_definition_file_path,
    step_description=f"\nGenerating api_definition.md"
)

## Api dependencies
api_dependencies_file_path = f"{absolute_path_docs_directory}/api_design/api_dependencies.md"
prompt = prompts.api_dependency_prompt_template.substitute(
    application_directory="moneynote-api/",
    api_definition_absolute_path=api_definition_file_path,
    absolute_file_path=api_dependencies_file_path
)
run_till_file_exists (
    prompt=prompt,
    absolute_file_path=api_dependencies_file_path,
    step_description=f"\nGenerating api_dependencies.md"
)

## Api plan
api_plan_file_path = f"{absolute_path_docs_directory}/api_design/api_plan.md"
prompt = prompts.api_dependency_prompt_template.substitute(
    api_definition_absolute_path=api_definition_file_path,
    api_dependencies_file_path=api_dependencies_file_path,
    absolute_file_path=api_plan_file_path
)
run_till_file_exists (
    prompt=prompt,
    absolute_file_path=api_plan_file_path,
    step_description=f"\nGenerating api_plan.md"
)