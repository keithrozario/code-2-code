from mrkdwn_analysis import MarkdownAnalyzer

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