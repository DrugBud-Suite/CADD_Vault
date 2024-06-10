import pandas as pd
import os
import shutil

# Get the absolute path to the directory where the script is running
script_dir = os.path.dirname(os.path.abspath(__file__))

# Set the path to the docs folder, which is at the same level as the scripts folder
docs_dir = os.path.join(script_dir, '../docs')


# Function to clear the docs directory except for specified files
def clear_directory_except(docs_path, keep_files):
    for item in os.listdir(docs_path):
        item_path = os.path.join(docs_path, item)
        if item not in keep_files:
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)


# Load the CSV file
df = pd.read_csv('../processed_cadd_vault_data.csv')


def update_md_file(file_path, content, subcategory, subsubcategory):
    # Function to update markdown file with proper headers and content
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            if pd.notna(subcategory):
                file.write(f"## {subcategory}\n")
            if pd.notna(subsubcategory):
                file.write(f"### {subsubcategory}\n")
            file.write(content)
    else:
        with open(file_path, 'a+', encoding='utf-8') as file:
            file.seek(0)
            existing_content = file.read()
            if pd.notna(subcategory
                        ) and f"## {subcategory}" not in existing_content:
                file.write(f"\n## {subcategory}\n")
            if pd.notna(subsubcategory
                        ) and f"### {subsubcategory}" not in existing_content:
                file.write(f"### {subsubcategory}\n")
            file.write(content)


# First, clean up the docs directory except for the specified files
clear_directory_except(docs_dir,
                       ['CONTRIBUTING.md', 'index.md', 'LogoV1.png', 'images'])

# Create the folders and files based on the specified structure
for index, row in df.iterrows():
    folder_path = os.path.join(docs_dir, row['FOLDER1'])
    file_name = str(row['CATEGORY1']) + '.md'
    file_path = os.path.join(folder_path, file_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    entry_content = f"- **{row['ENTRY NAME']}**: {row['DESCRIPTION'] if pd.notna(row['DESCRIPTION']) else ''}\n"
    if pd.notna(row['CODE']):
        entry_content += f"\t- [Code]({row['CODE']}) : Last updated in {row['LAST_COMMIT']}, {row['LAST_COMMIT_AGO']}\n"
    if pd.notna(row['PUBLICATION']):
        entry_content += f"\t- [Publication]({row['PUBLICATION']}) : Citations: {row['CITATIONS'] if pd.notna(row['CITATIONS']) else 'N/A'}\n"
    if pd.notna(row['WEBSERVER']):
        entry_content += f"\t- [Webserver]({row['WEBSERVER']})\n"
    if pd.notna(row['LINK']):
        entry_content += f"\t- [Link]({row['LINK']})\n"

    update_md_file(file_path, entry_content, row['SUBCATEGORY1'],
                   row['SUBSUBCATEGORY1'])

total_publications = len(df['PUBLICATION'].dropna())
total_code_repos = len(df['CODE'].dropna())
total_webserver_links = len(df['WEBSERVER'].dropna())


def update_index_file(docs_directory, total_publications, total_code_repos,
                      total_webserver_links):
    index_file_path = os.path.join(docs_directory, "index.md")
    if not os.path.exists(index_file_path):
        print(f"{index_file_path} does not exist.")
        return

    with open(index_file_path, "r", encoding='utf-8') as f:
        lines = f.readlines()

    if len(lines) < 5:
        print("The index.md file has less than 5 lines.")
        return

    lines[4] = f"Number of publications: {total_publications}\n"
    lines[5] = f"Number of code repositories: {total_code_repos}\n"
    lines[6] = f"Number of webserver links: {total_webserver_links}\n"

    with open(index_file_path, "w", encoding='utf-8') as f:
        f.writelines(lines)


update_index_file(docs_dir, total_publications, total_code_repos,
                  total_webserver_links)
