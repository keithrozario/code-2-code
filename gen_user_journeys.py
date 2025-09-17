from helper_funcs import get_md_analyzer_and_content
import subprocess

def run_gemini_prompt(prompt: str)->bool:

    try:
        result = subprocess.run([
            'gemini',
            '-y',
            '-p',
            prompt
        ], capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing shell command: {e}")
        print(f"Stderr: {e.stderr}")
        return False
    
    return True

code_mod_report = "customized_report_money_note_detailed_journeys.md"

analyzer, content = get_md_analyzer_and_content(code_mod_report)
headers =  analyzer.identify_headers()['Header']


# The prompt specifies creating a new section called "User Journeys"
journey_header = [header for header in headers if "User Journeys" in header['text']][0]

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
            break # we're done, avoid duplicate User Journey Sessions



for user_journey_name in user_journey_header_texts:
    print(user_journey_name)
    prompt = f"""
    Look at the customized_report_money_note_detailed_journeys.md file, and the customized_report_money_note_data_layer.md file. 
    These files represent a report for code in moneynote-api directory. 
    As a senior business analyst Document {user_journey_name}. Document your results in an .md file with the following content:

    * Detailed user journey and flows. If there are multiple journeys include one section for each journey.
    * Detailed object level data structures. For each data structure, capture the data attributes as present in code or the database.
    * Database tables to be updated
    * API Calls that are made.
    * Business rules and functionality (include code snippets from original code to make it clearer)
    * Detailed Test cases
    * State any assumptions

    Refer back to the original code to get a better understanding. 
    Use the example_user_journey.md as an example file, follow the format and structure of that file. 
    Save the file to the current working directory {user_journey_name}.md file
    """

    run_gemini_prompt(prompt=prompt)

# Run prompt for functional specificaiton introduction
prompt = """
As a senior business analyst, craft out an introduction to a functional specification document, covering the following 3 areas. 

Purpose of the Document: Explains why this functional specification is needed.
Goals and Objectives: The high-level goals the system aims to achieve.
Scope: Defines what is included and excluded from the project.

Use the following files to guide you:

* customized_report_money_note_detailed_journeys.md
* customized_report_money_note_data_layer.md

and all user journey files in this folder.

output the results to the functional_specs_introduction.md file
"""
run_gemini_prompt(prompt=prompt)
