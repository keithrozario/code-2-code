import prompts.user_journey
import prompts.database_design
import prompts.api_design
import config

from helper_funcs import generate_doc_file, get_user_journey_header_texts

## User Journeys

user_journey_header_texts = get_user_journey_header_texts(
    codmod_report=config.CODMOD_REPORT_PATH
)
print("Identified the following user_journeys")
for user_journey_name in user_journey_header_texts:
    print(user_journey_name)

user_journey_file_paths = []

for user_journey_name in user_journey_header_texts:
    absolute_file_path = (
        f"{config.USER_JOURNEY_DIRECTORY_PATH}/{user_journey_name.replace(' ', '_')}.md"
    )
    user_journey_file_paths.append(absolute_file_path)
    generate_doc_file(
        file_path=absolute_file_path,
        prompt_template=prompts.user_journey.user_journey_prompt_template,
        step_description=f"\nGenerating {user_journey_name} documentation in {absolute_file_path}",
        substitutions={
            "codmod_detailed_relative_file_path": config.CODMOD_REPORT_PATH,
            "codmod_data_relative_file_path": config.CODMOD_DATA_REPORT_PATH,
            "user_journey_name": user_journey_name,
            "absolute_file_path": absolute_file_path,
        },
    )

## BRD
for user_journey_file in user_journey_file_paths:
    brd_file_name = user_journey_file.split("/")[-1]
    brd_file_path = f"{config.BRDS_DIRECTORY_PATH}/{brd_file_name}"
    generate_doc_file(
        file_path=brd_file_path,
        prompt_template=prompts.user_journey.brd_prompt_template,
        step_description=f"\nGenerating BRD for {brd_file_name}",
        substitutions={
            "absolute_file_path": brd_file_path,
            "user_journey_absolute_path": user_journey_file,
            "application_directory": "moneynote-api/",
        },
    )

doc_generation_configs = [
    {
        "file_path": config.FUNCTIONAL_SPECS_PATH,
        "prompt_template": prompts.user_journey.functional_specification_intro_prompt_template,
        "step_description": "\nGenerating functional_specs_introduction.md",
        "substitutions": {"absolute_file_path": config.FUNCTIONAL_SPECS_PATH},
    },
    {
        "file_path": config.DATABASE_DEFINITION_PATH,
        "prompt_template": prompts.database_design.database_specification_prompt_template,
        "step_description": "\nGenerating database_definition.md",
        "substitutions": {
            "application_directory": "moneynote-api/",
            "absolute_file_path": config.DATABASE_DEFINITION_PATH,
        },
    },
    {
        "file_path": config.DATABASE_ERD_PATH,
        "prompt_template": prompts.database_design.database_erd_prompt_template,
        "step_description": "\nGenerating database_erd.md",
        "substitutions": {
            "application_directory": "moneynote-api/",
            "absolute_file_path": config.DATABASE_ERD_PATH,
            "database_design_absolute_file_path": config.DATABASE_ERD_PATH,
        },
    },
    {
        "file_path": config.API_DEFINITION_PATH,
        "prompt_template": prompts.api_design.api_specification_prompt_template,
        "step_description": "\nGenerating api_definition.md",
        "substitutions": {
            "application_directory": "moneynote-api/",
            "absolute_file_path": config.API_DEFINITION_PATH,
        },
    },
    {
        "file_path": config.API_DEPENDENCIES_PATH,
        "prompt_template": prompts.api_design.api_dependency_prompt_template,
        "step_description": "\nGenerating api_dependencies.md",
        "substitutions": {
            "application_directory": "moneynote-api/",
            "api_definition_absolute_path": config.API_DEFINITION_PATH,
            "absolute_file_path": config.API_DEPENDENCIES_PATH,
        },
    },
    {
        "file_path": config.API_PLAN_PATH,
        "prompt_template": prompts.api_design.api_plan_prompt_template,
        "step_description": "\nGenerating api_plan.md",
        "substitutions": {
            "api_definition_absolute_path": config.API_DEFINITION_PATH,
            "api_dependencies_absolute_path": config.API_DEPENDENCIES_PATH,
            "absolute_file_path": config.API_PLAN_PATH,
        },
    },
    {
        "file_path": config.API_DETAIL_DESIGN_PATH,
        "prompt_template": prompts.api_design.api_design_prompt_template,
        "step_description": "\nGenerating api_detail_design.md",
        "substitutions": {
            "api_definition_absolute_path": config.API_DEFINITION_PATH,
            "api_dependencies_absolute_path": config.API_DEPENDENCIES_PATH,
            "api_plan_absolute_path": config.API_PLAN_PATH,
            "architecture_principles_absolute_path": config.ARCHITECTURE_PRINCIPLES_PATH,
            "absolute_file_path": config.API_DETAIL_DESIGN_PATH,
        },
    },
]

for doc_config in doc_generation_configs:
    generate_doc_file(**doc_config)

