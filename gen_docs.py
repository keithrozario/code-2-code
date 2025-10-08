import json
import os
import re

def find_class_file(class_name, root_dir):
    """Finds the Java file defining a class."""
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file == f"{class_name}.java":
                return os.path.join(root, file)
    return None

def analyze_java_class(class_file_path):
    """Analyzes a Java class file to extract its fields."""
    if not class_file_path or not os.path.exists(class_file_path):
        return []

    fields = []
    with open(class_file_path, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            # Simple regex to find field declarations
            match = re.search(r'private\s+([\w.<>]+)\s+(\w+);', line)
            if match:
                data_type = match.group(1)
                name = match.group(2)
                optionality = "Optional"
                # Check for @NotNull annotation for mandatory fields
                if any("@NotNull" in prev_line for prev_line in lines[max(0, i-3):i]):
                    optionality = "Mandatory"
                fields.append({
                    "Name": name,
                    "Data Type": data_type,
                    "Description (Business Context)": "", # Description is hard to get automatically
                    "Optionality": optionality
                })
    return fields

def format_params_to_markdown(title, params):
    """Formats a list of parameters into a Markdown table."""
    if not params:
        return ""
    
    markdown = f"### {title}\n"
    markdown += "| Name | Data Type | Description (Business Context) | Optionality |\n"
    markdown += "|---|---|---|---|
"
    for param in params:
        markdown += f"| {param['Name']} | {param['Data Type']} | {param['Description (Business Context)']} | {param['Optionality']} |\n"
    return markdown + "\n"

def analyze_endpoint(endpoint, root_dir):
    """Analyzes a single endpoint and returns its documentation."""
    source_location = endpoint["sourceLocation"]
    file_path, line_number_str = source_location.split(":")
    line_number = int(line_number_str)
    
    full_path = os.path.join(root_dir, file_path)

    request_params = []
    response_params = []

    if os.path.exists(full_path):
        with open(full_path, 'r') as f:
            lines = f.readlines()
            if line_number -1 < len(lines):
                method_line = lines[line_number-1]
                # Look for next line to get method signature
                if line_number < len(lines):
                    method_signature_line = lines[line_number]
                    
                    # Analyze request parameters
                    request_body_match = re.search(r'@RequestBody\s+([\w]+)', method_signature_line)
                    if request_body_match:
                        request_class_name = request_body_match.group(1)
                        class_file = find_class_file(request_class_name, root_dir)
                        request_params.extend(analyze_java_class(class_file))

                    path_variable_matches = re.findall(r'@PathVariable\("(.*?)"\)\s+(\w+)', method_signature_line)
                    for match in path_variable_matches:
                        request_params.append({
                            "Name": match[0],
                            "Data Type": match[1],
                            "Description (Business Context)": "Path Parameter",
                            "Optionality": "Mandatory"
                        })

                    # Analyze response
                    response_match = re.search(r'new\s+BaseResponse\((.*?)\)', method_line + lines[line_number])
                    if response_match:
                        response_params.append({
                            "Name": "success",
                            "Data Type": "boolean",
                            "Description (Business Context)": "Indicates if the operation was successful.",
                            "Optionality": "Mandatory"
                        })
                    else: # Try to get from return type
                        return_type_match = re.search(r'public\s+([\w.<>]+)', method_signature_line)
                        if return_type_match:
                            return_type = return_type_match.group(1)
                            if return_type != "BaseResponse":
                                class_file = find_class_file(return_type, root_dir)
                                response_params.extend(analyze_java_class(class_file))
                            else:
                                response_params.append({
                                    "Name": "success",
                                    "Data Type": "boolean",
                                    "Description (Business Context)": "Indicates if the operation was successful.",
                                    "Optionality": "Mandatory"
                                })


    # Format output
    markdown = f"## Endpoint: `{endpoint['method']} {endpoint['path']}`\n\n"
    markdown += f"**Description:** {endpoint['description']}\n"
    markdown += f"**Source:** `{endpoint['sourceLocation']}`\n\n"
    markdown += format_params_to_markdown("Request Parameters", request_params)
    markdown += format_params_to_markdown("Response Parameters", response_params)
    
    return markdown

if __name__ == "__main__":
    root_dir = "/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4"
    output_file = "step2_api"
    
    with open("step1_api", "r") as f:
        endpoints = json.load(f)
        
    all_docs = ""
    for endpoint in endpoints:
        # Skipping .py files is implicitly handled as we only process .java files
        all_docs += analyze_endpoint(endpoint, root_dir)
        all_docs += "---\n\n" # Separator
        
    with open(output_file, "w") as f:
        f.write(all_docs)