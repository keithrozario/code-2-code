import os
from typing import List

from helper_funcs import get_md_analyzer_and_content, run_till_file_exists
from prompts import user_journey_prompt_template, functional_specification_intro_prompt_template, database_specification_prompt_template


codmod_report = "./docs/codmod_reports/customized_report_money_note_detailed_journeys.md"
codmod_data_report = "./docs/codmod_reports/customized_report_money_note_data_layer.md"
user_journey_relative_directory = "docs/user_journeys"
functional_spec_intro_relative_directory = "docs"

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

for user_journey_name in user_journey_header_texts:
    absolute_file_path = f"{os.getcwd()}/{user_journey_relative_directory}/{user_journey_name.replace(' ','_')}.md"
    prompt = user_journey_prompt_template.substitute(
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

absolute_file_path = f"{os.getcwd()}/docs/functional_specs_introduction.md"
prompt = functional_specification_intro_prompt_template.substitute(
    absolute_file_path = absolute_file_path
)
run_till_file_exists (
    prompt=prompt,
    absolute_file_path=absolute_file_path,
    step_description=f"\nGenerating functional_specs_introduction.md"
)


# Database Design
absolute_file_path = f"{os.getcwd()}/docs/database_design/database_definition.md"
prompt = database_specification_prompt_template.substitute(
    application_directory="moneynote-api/",
    absolute_file_path=absolute_file_path
)
run_till_file_exists (
    prompt=prompt,
    absolute_file_path=absolute_file_path,
    step_description=f"\nGenerating database_definition.md"
)
