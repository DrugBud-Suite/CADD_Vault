import pandas as pd
import os
import shutil
import requests
import re
import yaml
from multiprocessing import Pool, cpu_count
from functools import partial
import logging

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Get the absolute path to the directory where the script is running
script_dir = os.path.dirname(os.path.abspath(__file__))

# Set the path to the docs folder, which is at the same level as the scripts folder
docs_dir = os.path.join(script_dir, '../docs')
readme = os.path.join(script_dir, '../README.md')


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


def check_url(url):
    try:
        response = requests.get(url, timeout=10)  # Timeout after 10 seconds
        if response.status_code == 200:
            return "online"
        else:
            return "offline"
    except requests.RequestException:
        return "offline"


def update_md_file(file_path, content, subcategory, subsubcategory, page_icon):
    # Initialize headers as not written
    header_written = {
        'icon': False,
        'subcategory': False,
        'subsubcategory': False
    }

    # Check if file exists and set headers as written if it does
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            existing_content = file.read()
            if "---" in existing_content:
                header_written['icon'] = True
            if f"## **{subcategory}**" in existing_content:
                header_written['subcategory'] = True
            if f"### **{subsubcategory}**" in existing_content:
                header_written['subsubcategory'] = True

    # Write to file, appending if exists, otherwise create new
    with open(file_path,
              'a+' if os.path.exists(file_path) else 'w',
              encoding='utf-8') as file:
        if not header_written['icon'] and pd.notna(page_icon):
            file.write(f"---\nicon: {page_icon}\n---\n\n")
        if not header_written['subcategory'] and pd.notna(subcategory):
            file.write(f"\n## **{subcategory}**\n")
        if not header_written['subsubcategory'] and pd.notna(subsubcategory):
            file.write(f"### **{subsubcategory}**\n")
        file.write(content)


def process_folder(folder_group, docs_dir):
    folder, group = folder_group
    folder_path = os.path.join(docs_dir, folder)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for _, row in group.iterrows():
        file_name = str(row['CATEGORY1']) + '.md'
        file_path = os.path.join(folder_path, file_name)

        entry_content = f"- **{row['ENTRY NAME']}**: {row['DESCRIPTION'] if pd.notna(row['DESCRIPTION']) else ''}  \n"

        if pd.notna(row['CODE']):
            if 'github' in row['CODE'] and 'gist' not in row['CODE']:

                def clean_github_url(url):
                    url = url.replace('.git', '')  # Remove '.git' if present
                    match = re.match(r'https://github\.com/([^/]+)/([^/?#]+)',
                                     url)
                    if match:
                        return f"{match.group(1)}/{match.group(2)}"
                    return None

                url = clean_github_url(row['CODE'])
                entry_content += f"\t[![Code](https://img.shields.io/github/stars/{url}?style=for-the-badge&logo=github)]({row['CODE']})  \n"
                entry_content += f"\t[![Last Commit](https://img.shields.io/github/last-commit/{url}?style=for-the-badge&logo=github)]({row['CODE']})  \n"
            else:
                entry_content += f"\t[![Code](https://img.shields.io/badge/Code)]({row['CODE']})\n"

        if pd.notna(row['PUBLICATION']):
            citations = int(row['CITATIONS']) if pd.notna(
                row['CITATIONS']) else 'N/A'
            logo = 'arxiv' if 'rxiv' in row['PUBLICATION'] else 'bookstack'
            entry_content += f"\t[![Publication](https://img.shields.io/badge/Publication-Citations:{citations}-blue?style=for-the-badge&logo={logo})]({row['PUBLICATION']})  \n"

        if pd.notna(row['WEBSERVER']):
            status = check_url(row['WEBSERVER'])
            if status == 'online':
                entry_content += f"\t[![Webserver](https://img.shields.io/badge/Webserver-online-brightgreen?style=for-the-badge&logo=cachet&logoColor=65FF8F)]({row['WEBSERVER']})  \n"
            else:
                entry_content += f"\t[![Webserver](https://img.shields.io/badge/Webserver-offline-red?style=for-the-badge&logo=xamarin&logoColor=red)]({row['WEBSERVER']})  \n"

        if pd.notna(row['LINK']):
            status = check_url(row['LINK'])
            if status == 'online':
                entry_content += f"\t[![Link](https://img.shields.io/badge/Link-online-brightgreen?style=for-the-badge&logo=cachet&logoColor=65FF8F)]({row['LINK']})  \n"
            else:
                entry_content += f"\t[![Link](https://img.shields.io/badge/Link-offline-red?style=for-the-badge&logo=xamarin&logoColor=red)]({row['LINK']})  \n"

        update_md_file(file_path, entry_content, row['SUBCATEGORY1'],
                       row['SUBSUBCATEGORY1'], row['PAGE_ICON'])

    logging.info(f"Processed folder: {folder}")


def update_index_file(docs_directory, readme, total_publications,
                      total_code_repos, total_webserver_links):
    index_file_path = os.path.join(docs_directory, "index.md")
    if not os.path.exists(index_file_path):
        logging.error(f"{index_file_path} does not exist.")
        return

    with open(index_file_path, "r", encoding='utf-8') as f:
        lines = f.readlines()

    if len(lines) < 5:
        logging.error("The index.md file has less than 5 lines.")
        return

    lines[4] = f"Number of publications: {total_publications}  \n"
    lines[5] = f"Number of code repositories: {total_code_repos}  \n"
    lines[6] = f"Number of webserver links: {total_webserver_links}"

    with open(index_file_path, "w", encoding='utf-8') as f:
        f.writelines(lines)

    if not os.path.exists(readme):
        logging.error(f"{readme} does not exist.")
        return

    with open(readme, "r", encoding='utf-8') as f:
        lines = f.readlines()

    if len(lines) < 5:
        logging.error("The README.md file has less than 5 lines.")
        return

    lines[25] = f"Number of publications: {total_publications}  \n"
    lines[26] = f"Number of code repositories: {total_code_repos}  \n"
    lines[27] = f"Number of webserver links: {total_webserver_links}  \n"

    with open(readme, "w", encoding='utf-8') as f:
        f.writelines(lines)


def main():
    # First, clean up the docs directory except for the specified files
    clear_directory_except(
        docs_dir, ['CONTRIBUTING.md', 'index.md', 'LogoV1.png', 'images'])

    # Group the data by FOLDER1
    grouped = df.groupby('FOLDER1')

    # Set up the multiprocessing pool
    num_processes = min(cpu_count(), len(grouped))
    pool = Pool(processes=num_processes)

    # Use partial to pass the docs_dir argument to process_folder
    process_folder_partial = partial(process_folder, docs_dir=docs_dir)

    # Process folders in parallel
    pool.map(process_folder_partial, grouped)

    # Close the pool and wait for all processes to finish
    pool.close()
    pool.join()

    # Calculate totals
    total_publications = len(df['PUBLICATION'].dropna())
    total_code_repos = len(df['CODE'].dropna())
    total_webserver_links = len(df['WEBSERVER'].dropna())

    # Update index file and README
    update_index_file(docs_dir, readme, total_publications, total_code_repos,
                      total_webserver_links)

    logging.info("Documentation generation completed successfully.")


if __name__ == "__main__":
    main()
