import os
import prompts.prd_generation
from helper_funcs import run_till_file_exists, set_task_status_from_taskmaster, gen_task_from_prd, expand_all_task_master_tasks
from helper_funcs import task_master_status_file

absolute_path_docs_directory = f"{os.getcwd()}/docs"
api_detail_design = f"{absolute_path_docs_directory}/api_design/api_detail_design.md"


def get_next_phase(directory: str) -> int:
    """
    Determines the next PRD phase number to generate.
    It returns the first missing phase in the sequence. If no phases are missing, it returns the next phase after the latest one.

    Args:
        directory: The path to the directory containing the PRD files.

    Returns:
        The integer of the next phase to generate. Returns 1 if no phase files exist yet.
    """
    try:
        files = os.listdir(directory)
    except FileNotFoundError:
        return 1
        
    phase_numbers = []
    for filename in files:
        if filename.startswith("prd_phase_") and filename.endswith(".md"):
            phase_part = filename.removeprefix("prd_phase_").removesuffix(".md")
            try:
                phase_numbers.append(int(phase_part))
            except ValueError:
                continue
    
    if not phase_numbers:
        return 1
        
    # Find the missing phases
    latest_phase = max(phase_numbers)
    expected_phases = set(range(1, latest_phase + 1))
    existing_phases = set(phase_numbers)
    missing_phases = sorted(list(expected_phases - existing_phases))
    
    # Decide what to return
    if missing_phases:
        return missing_phases[0]  # Return the first gap in the sequence
    else:
        return latest_phase + 1   # No gaps, so return the next number

## PRD
phase = get_next_phase(f"{absolute_path_docs_directory}/prds/")
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

# Generate Task from PRD
set_task_status_from_taskmaster()
try:
    with open(task_master_status_file, 'r') as status:
        status_as_md = status.read()
except FileNotFoundError:
    status_as_md = ""
# Get detail_design
with open(api_detail_design, 'r') as api_detail_design:
    api_detail_design_as_md = api_detail_design.read()
# Update the PRD
with open(prd_file_path, 'a') as prd_file:
    prd_file.write(status_as_md)
    prd_file.write(api_detail_design_as_md)
gen_task_from_prd(prd_file_path)
expand_all_task_master_tasks()