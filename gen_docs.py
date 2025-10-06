import os

import prompts.user_journey
import prompts.database_design
import prompts.api_design
import prompts.prd_generation
from helper_funcs import run_till_file_exists, get_user_journey_header_texts

user_journey_relative_directory = "user_journeys"
absolute_path_docs_directory = f"{os.getcwd()}/docs"
codmod_report = f"{absolute_path_docs_directory}/codmod_reports/customized_report_money_note_detailed_journeys.md"
codmod_data_report = f"{absolute_path_docs_directory}/codmod_reports/customized_report_money_note_data_layer.md"
user_journey_directory = (
    f"{absolute_path_docs_directory}/{user_journey_relative_directory}"
)
architecture_principles_absolute_path = (
    f"{absolute_path_docs_directory}/context_docs/architecture_principles.md"
)

## User Journeys

user_journey_header_texts = get_user_journey_header_texts(codmod_report=codmod_report)
print("Identified the following user_journeys")
for user_journey_name in user_journey_header_texts:
    print(user_journey_name)

user_journey_file_paths = []

for user_journey_name in user_journey_header_texts:
    absolute_file_path = (
        f"{user_journey_directory}/{user_journey_name.replace(' ', '_')}.md"
    )
    user_journey_file_paths.append(absolute_file_path)
    prompt = prompts.user_journey.user_journey_prompt_template.substitute(
        codmod_detailed_relative_file_path=codmod_report,
        codmod_data_relative_file_path=codmod_data_report,
        user_journey_name=user_journey_name,
        absolute_file_path=absolute_file_path,
    )
    run_till_file_exists(
        prompt=prompt,
        absolute_file_path=absolute_file_path,
        step_description=f"\nGenerating {user_journey_name} documentation in {absolute_file_path}",
    )

## BRD
for user_journey_file in user_journey_file_paths:
    brd_file_name = user_journey_file.split("/")[-1]
    brd_file_path = f"{absolute_path_docs_directory}/brds/{brd_file_name}"
    prompt = prompts.user_journey.brd_prompt_template.substitute(
        absolute_file_path=brd_file_path,
        user_journey_absolute_path=user_journey_file,
        application_directory="moneynote-api/",
    )
    run_till_file_exists(
        prompt=prompt,
        absolute_file_path=brd_file_path,
        step_description=f"\nGenerating BRD for {brd_file_name}",
    )


# Functional Specification Intro
func_specs_file_path = (
    f"{absolute_path_docs_directory}/functional_specs_introduction.md"
)
prompt = prompts.user_journey.functional_specification_intro_prompt_template.substitute(
    absolute_file_path=func_specs_file_path
)
run_till_file_exists(
    prompt=prompt,
    absolute_file_path=func_specs_file_path,
    step_description="\nGenerating functional_specs_introduction.md",
)


# Database

## Database Design
database_definition_file_path = (
    f"{absolute_path_docs_directory}/database_design/database_definition.md"
)
prompt = prompts.database_design.database_specification_prompt_template.substitute(
    application_directory="moneynote-api/",
    absolute_file_path=database_definition_file_path,
)
run_till_file_exists(
    prompt=prompt,
    absolute_file_path=database_definition_file_path,
    step_description="\nGenerating database_definition.md",
)

## Database ERD
database_erd_file_path = (
    f"{absolute_path_docs_directory}/database_design/database_erd.md"
)
prompt = prompts.database_design.database_erd_prompt_template.substitute(
    application_directory="moneynote-api/",
    absolute_file_path=database_erd_file_path,
    database_design_absolute_file_path=database_erd_file_path,
)
run_till_file_exists(
    prompt=prompt,
    absolute_file_path=database_erd_file_path,
    step_description="\nGenerating database_erd.md",
)


# Api Definitition
## Api Specification
api_definition_file_path = (
    f"{absolute_path_docs_directory}/api_design/api_definition.md"
)
prompt = prompts.api_design.api_specification_prompt_template.substitute(
    application_directory="moneynote-api/", absolute_file_path=api_definition_file_path
)
run_till_file_exists(
    prompt=prompt,
    absolute_file_path=api_definition_file_path,
    step_description="\nGenerating api_definition.md",
)

## Api dependencies
api_dependencies_file_path = (
    f"{absolute_path_docs_directory}/api_design/api_dependencies.md"
)
prompt = prompts.api_design.api_dependency_prompt_template.substitute(
    application_directory="moneynote-api/",
    api_definition_absolute_path=api_definition_file_path,
    absolute_file_path=api_dependencies_file_path,
)
run_till_file_exists(
    prompt=prompt,
    absolute_file_path=api_dependencies_file_path,
    step_description="\nGenerating api_dependencies.md",
)

## Api plan
api_plan_file_path = f"{absolute_path_docs_directory}/api_design/api_plan.md"
prompt = prompts.api_design.api_plan_prompt_template.substitute(
    api_definition_absolute_path=api_definition_file_path,
    api_dependencies_absolute_path=api_dependencies_file_path,
    absolute_file_path=api_plan_file_path,
)
run_till_file_exists(
    prompt=prompt,
    absolute_file_path=api_plan_file_path,
    step_description="\nGenerating api_plan.md",
)

# Api Design Document
api_detail_design_file_path = (
    f"{absolute_path_docs_directory}/api_design/api_detail_design.md"
)
prompt = prompts.api_design.api_design_prompt_template.substitute(
    api_definition_absolute_path=api_definition_file_path,
    api_dependencies_absolute_path=api_dependencies_file_path,
    api_plan_absolute_path=api_plan_file_path,
    architecture_principles_absolute_path=architecture_principles_absolute_path,
    absolute_file_path=api_detail_design_file_path,
)
run_till_file_exists(
    prompt=prompt,
    absolute_file_path=api_detail_design_file_path,
    step_description="\nGenerating api_detail_design.md",
)

# PRD
for phase in range(1, 2):
    prd_file_path = f"{absolute_path_docs_directory}/prds/prd_phase_{phase}.md"
    prompt = prompts.prd_generation.prd_prompt_template.substitute(
        absolute_file_path=prd_file_path,
        phase_number=phase,
        example_prd_file_path=f"{absolute_path_docs_directory}/prds/example.md",
        new_app_directory=f"{os.getcwd()}/new_app",
    )
    run_till_file_exists(
        prompt=prompt,
        absolute_file_path=prd_file_path,
        step_description=f"\nGenerating {prd_file_path}",
    )
