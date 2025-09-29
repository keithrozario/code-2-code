import os
from typing import List

from helper_funcs import get_md_analyzer_and_content, run_gemini_prompt
from prompts import user_journey_prompt_template, functional_specification_intro_prompt_template


codmod_report = "./docs/codmod_reports/customized_report_money_note_detailed_journeys.md"
codmod_data_report = "./docs/codmod_reports/customized_report_money_note_data_layer.md"

def get_user_journey_header_texts (codmod_report: str) -> List[str]:
    """
    Parses the markdown file and returns the list of user_journeys 
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


user_journey_header_texts = get_user_journey_header_texts(codmod_report=codmod_report)

print("Identified the following user_journeys")
for user_journey_name in user_journey_header_texts:
    print(user_journey_name) 

for user_journey_name in user_journey_header_texts:
    file_name = f"{os.getcwd()}/user_journeys/{user_journey_name.replace(' ','_')}.md"
    prompt = user_journey_prompt_template.substitute(
        codmod_detailed_relative_file_path = codmod_report,
        codmod_data_relative_file_path = codmod_data_report,
        user_journey_name = user_journey_name,
        absolute_file_path = file_name
    )

    # Sometimes the file doesn't generate again ...
    for i in range(1,4):
        print(f"\nNow creating for {user_journey_name}")
        run_gemini_prompt(prompt=prompt)
        if os.path.exists(f"{file_name}"):
            print(f"Yay! File created: {file_name}")
            break

    

# # Run prompt for functional specificaiton introduction
# file_name = f"{os.getcwd()}/functional_specs_introduction.md"
# prompt = functional_specification_intro_prompt_template.substitute(
#     absolute_file_path = file_name
# )

# while not os.path.exists(file_name):
#     run_gemini_prompt(prompt=prompt)
# print(f"Yay! File created: {file_name}")
