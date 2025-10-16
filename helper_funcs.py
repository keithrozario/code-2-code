import json
import os
import subprocess
import time
from string import Template
from typing import List

from mrkdwn_analysis import MarkdownAnalyzer

import config


def get_md_analyzer_and_content(file_path:str):
    """
    Gets the MarkdownAnalyzer instance and content of a markdown file.

    Args:
        file_path (str): The path to the markdown file.

    Returns:
        analyzer (MarkdownAnalyzer): An instance of MarkdownAnalyzer initialized with the markdown file.
        content (List[str]): The content of the markdown file as a list of lines.
    """
    with open(file_path) as input_file:
        content = input_file.readlines()
    analyzer = MarkdownAnalyzer(file_path)

    return analyzer, content


def run_gemini_prompt(prompt: str)->bool:

    prompt = '"'+prompt.replace('"','\\"')+'"'
    try:
        result = subprocess.run([
            'gemini',
            '--approval-mode=yolo',
            '--model=gemini-2.5-pro',
            '-p',
            prompt
        ], text=True, check=True, stderr=subprocess.STDOUT)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Stderr: {e.stderr}")
        return False
    
    return True

def gen_task_from_prd(prd_filepath: str):

    try:
        result = subprocess.run([
            'task-master',
            'parse-prd',
            prd_filepath
        ], text=True, check=True, stderr=subprocess.STDOUT)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing shell command: {e}")
        print(f"Stderr: {e.stderr}")
        return False

    return True


def expand_task_master_task(task_id: int)->bool:
    try:
        result = subprocess.run([
            'task-master',
            'expand',
            f'--id={task_id}'
        ], text=True, check=True, stderr=subprocess.STDOUT)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing shell command: {e}")
        print(f"Stderr: {e.stderr}")
        return False

    return True


def run_till_file_exists(prompt: str, absolute_file_path: str, step_description: str):
    """
    Executes the prompt in gemini-cli until the file in the absolute file path exists
    """

    max_attempts = 5
    delay_in_seconds = 15
    
    for i in range(0,max_attempts):
        # if the file already exists, we proceed to next steps, 
        # this way we can halt execution and resume without regenerating the same file over again
        if os.path.exists(f"{absolute_file_path}"):
            print(f"Yay! File created: {absolute_file_path}")
            break
        time.sleep(delay_in_seconds*i)
        print(step_description)
        run_gemini_prompt(prompt=prompt)
    
    return None

def generate_doc_file(file_path: str, prompt_template: Template, step_description: str, substitutions: dict):
    """
    Generates a documentation file using a prompt template and substitutions.

    Args:
        file_path (str): The absolute path to the file to be generated.
        prompt_template (any): The prompt template to use.
        step_description (str): The description of the step.
        substitutions (dict): A dictionary of substitutions for the prompt template.
    """
    prompt = prompt_template.substitute(substitutions)
    run_till_file_exists(
        prompt=prompt,
        absolute_file_path=file_path,
        step_description=step_description,
    )

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

def create_taskmaster_status_file():
    """
    Creates a taskmaster status if one doesn't exists.
    Populates the intro for the file
    """
    task_status_intro = f"""
## Completed Task so far

The following task have been executed and completed, do not repeat them, assume their output is ready for use for tasks in the future:
"""
    
    if not os.path.exists(config.TASKMASTER_STATUS_FILE):
        with open(config.TASKMASTER_STATUS_FILE, 'w') as status_file:
            status_file.write(task_status_intro)

    return None

def set_task_status_from_taskmaster():
    """
    Sets the latest task from taskmaster, and writes status to taskmaster status file
    Taskmaster status is a custom file we create to store state across invocations of taskmaster.
    Be sure to commit this to version control.
    """
    try:
        with open(config.TASKMASTER_JSON_FILE, "r") as task_file:
            tasks = json.loads(task_file.read())['master']['tasks']
        create_taskmaster_status_file()
    except FileNotFoundError:
        # file not found, do not proceed
        return None

    task_titles = [task['title'] for task in tasks]
    task_titles_status = "\n".join([f"- [✔] {title}" for title in task_titles])

    with open(config.TASKMASTER_STATUS_FILE, 'a') as status_file:
        status_file.write(task_titles_status)

    return None

def expand_all_task_master_tasks():
    """
    Expands all task master tasks to subtask
    """
    with open(config.TASKMASTER_JSON_FILE, "r") as task_file:
        tasks = json.loads(task_file.read())['master']['tasks']
    
    task_ids = [task['id'] for task in tasks]
    for task_id in task_ids:
        expand_task_master_task(task_id)
    
    return None