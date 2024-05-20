import os
import re

def bold_hyperlinks_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Regex to find non-bold hyperlinks
    non_bold_pattern = r'(?<!\*\*)(\[.*?\]\(.*?\))(?!\*\*)'
    bold_content = re.sub(non_bold_pattern, r'**\1**', content)
    
    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(bold_content)

def recursively_bold_hyperlinks(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                bold_hyperlinks_in_file(file_path)
                print(f"Processed {file_path}")

# Specify the directory to search
directory_to_search = '../docs'

# Call the function
recursively_bold_hyperlinks(directory_to_search)
