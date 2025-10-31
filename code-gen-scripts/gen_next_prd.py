import os

import config

import prompts.prd_generation
from helper_funcs import (
    expand_all_task_master_tasks,
    gen_task_from_prd,
    generate_doc_file,
    get_next_phase,
    set_task_status_from_taskmaster,
)

## PRD
# phase = get_next_phase(config.PRDS_DIRECTORY)
phase = 1
prd_file_path = os.path.join(config.PRDS_DIRECTORY, f"prd_phase_{phase}.md")

# generate_doc_file(
#     file_path=prd_file_path,
#     prompt_template=prompts.prd_generation.prd_prompt_template,
#     step_description=f"\nGenerating {prd_file_path}",
#     substitutions={
#         "absolute_file_path": prd_file_path,
#         "phase_number": phase,
#         "example_prd_file_path": config.EXAMPLE_PRD_PATH,
#         "new_app_directory": config.NEW_APP_DIRECTORY,
#     },
# )

# Generate Task from PRD

## TO DO -- refactor stuff under here.
# set_task_status_from_taskmaster()
# try:
#     with open(config.TASKMASTER_STATUS_FILE, "r") as status:
#         status_as_md = status.read()
# except FileNotFoundError:
#     status_as_md = ""
# # Get detail_design
# with open(config.API_DETAIL_DESIGN_PATH, "r") as api_detail_design:
#     api_detail_design_as_md = api_detail_design.read()
# # Update the PRD
# with open(prd_file_path, "a") as prd_file:
#     prd_file.write(status_as_md)
#     prd_file.write(api_detail_design_as_md)
# gen_task_from_prd(prd_file_path)
expand_all_task_master_tasks()

