import os
import re

def count_hyperlinks(directory):
    total_links = 0

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding='utf-8') as f:
                    content = f.read()
                    links = re.findall(r"\[.*?\]\((.*?)\)", content)
                    total_links += len(links)

    return total_links

def update_index_file(docs_directory, total_links):
    index_file_path = os.path.join(docs_directory, "index.md")
    if not os.path.exists(index_file_path):
        print(f"{index_file_path} does not exist.")
        return
    
    with open(index_file_path, "r", encoding='utf-8') as f:
        lines = f.readlines()
    
    if len(lines) < 5:
        print("The index.md file has less than 5 lines.")
        return
    
    lines[4] = f"Total number of hyperlinks: {total_links}\n"
    
    with open(index_file_path, "w", encoding='utf-8') as f:
        f.writelines(lines)

docs_directory = "../docs/"
total_hyperlinks = count_hyperlinks(docs_directory)
print(f"Total number of hyperlinks in .md files: {total_hyperlinks}")

update_index_file(docs_directory, total_hyperlinks)
