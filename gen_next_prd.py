import os
import prompts.prd_generation
import config
from helper_funcs import generate_doc_file, get_next_phase

## PRD
phase = get_next_phase(config.PRDS_DIRECTORY)
prd_file_path = os.path.join(config.PRDS_DIRECTORY, f"prd_phase_{phase}.md")

generate_doc_file(
    file_path=prd_file_path,
    prompt_template=prompts.prd_generation.prd_prompt_template,
    step_description=f"\nGenerating {prd_file_path}",
    substitutions={
        "absolute_file_path": prd_file_path,
        "phase_number": phase,
        "example_prd_file_path": config.EXAMPLE_PRD_PATH,
        "new_app_directory": config.NEW_APP_DIRECTORY,
    },
)