import os
import prompts.prd_generation
import config
from helper_funcs import generate_doc_file


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