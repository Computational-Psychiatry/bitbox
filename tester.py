
import inspect
import re

def parse_source_file(file_path):
    classes = []
    functions = []

    with open(file_path, 'r') as file:
        source_code = file.read()

    class_pattern = re.compile(r'class\s+(\w+)\s*:')
    function_pattern = re.compile(r'def\s+(\w+)\s*\(.*?\):')

    # Find class definitions
    for match in class_pattern.finditer(source_code):
        class_name = match.group(1)
        classes.append(class_name)

    # Find function definitions
    for match in function_pattern.finditer(source_code):
        function_name = match.group(1)
        functions.append(function_name)

    return classes, functions

def generate_markdown(classes, functions):
    markdown = "# API Reference\n\n"

    markdown += "## Classes\n\n"
    for class_name in classes:
        markdown += f"### {class_name}\n\n"
        # Add class docstring if available

    markdown += "## Functions\n\n"
    for function_name in functions:
        markdown += f"### {function_name}\n\n"
        # Add function signature and docstring

    return markdown

def write_to_file(markdown, output_file):
    with open(output_file, 'w') as file:
        file.write(markdown)

# Example usage
source_file = 'src/bitbox/face_backend/backend3DI.py'
output_file = 'api_reference.md'

classes, functions = parse_source_file(source_file)
markdown = generate_markdown(classes, functions)
write_to_file(markdown, output_file)
