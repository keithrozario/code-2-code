from typing import List
from pathlib import Path
from helper_funcs import get_md_analyzer_and_content

def get_section(header:str, headers: List[dict], content:List[str], new_header_level: int)->str:
    """
    Extracts the content of a specific section from a markdown file based on the header title.

    Args:
        header (str): The title of the section to extract.
        headers List[dict]: List of headers generated from analyzer.identify_headers()
        content List[str]: The content of the markdown file as a list of lines.
        new_header_level (int): The level of header to return for this section.

    Returns:
        str: The content of the section as a single string.
    """
    
    section_start = [h for h in headers if h['text'] == header][0]
    section_end = [h for h in headers if h['level'] == section_start['level'] and h['line'] > section_start['line']][0]
    
    section_content = content[section_start['line']:section_end['line']-2]
    new_header = f"{'#'*new_header_level} {header} \n"
    section_content.insert(0, new_header)
    
    return "".join(section_content)


def get_sections_from_file(file_path: str, extract_sections: List[dict]) -> str:
    """
    Extract sections from the file

    Args:
        file_path: Path to file
        extract_sections: List of dicts with 'header' and 'new_level'
    
    returns
        content: Content as a string, with headers set to the 'new_level' specified.
    """
    analyzer, content = get_md_analyzer_and_content(file_path)
    headers =  analyzer.identify_headers()['Header']
    new_content = []
    for section in extract_sections:
        section_content = get_section(section['header'], headers, content, section['new_level'])
        if section_content[-1] != "\n":
            section_content = section_content + "\n"
        new_content.append(section_content)

    return "".join(new_content)


def append_entire_file(input_file: str, output_file: str):
    """
    Appends the content of the entire input file to the end of the output file
    """

    with open(input_file, 'r') as i:
        with open(output_file, 'a') as o:
            o.write(i.read())

    return None

if __name__ == "__main__":

    final_output_file = "final_functional_specification.md"
    append_entire_file(
        input_file = "functional_specs_introduction.md",
        output_file=final_output_file
    )
    
    
    # file_name = "./customized_report_money_note_data_layer.md" 
    # extract_sections = [
    #     {
    #         "header": "Key Data Entities",
    #         "new_level": 2
    #     },
    #     {
    #         "header": "Data Model",
    #         "new_level": 3
    #     },
    #     {
    #         "header": "Data Flow",
    #         "new_level": 3
    #     }
    # ]
    # new_content = get_sections_from_file(file_name, extract_sections)
    # with open(final_output_file, "a") as output_file:
    #     output_file.write(new_content)
    
    file_names = [
    p.name for p in Path('./user_journeys/').glob('*') 
    if p.is_file()
    ]
    for file_name in sorted(file_names):
        append_entire_file(
            input_file = f"./user_journeys/{file_name}",
            output_file=final_output_file
        )