# Contributing to the CADD Vault

We are excited that you are interested in contributing to the CADD Vault! This document provides guidelines for contributions to help ensure that our collaboration is as smooth and efficient as possible.

## How to Contribute

There are many ways you can contribute to the vault, including but not limited to:

- Adding new resources, such as tutorials, articles, or tools related to computer-aided drug design.
- Improving existing content for clarity, accuracy, or completeness.
- Reporting issues or suggesting enhancements.
- Helping to maintain and update the repository's structure for better navigation and usability.

## Pull Request Process

1. Fork the repository and create your branch from main.
2. Make your changes: Ensure any new content or changes are placed in the appropriate subdirectory within the docs directory for MkDocs.
3. Describe your changes: When you submit your pull request, please provide a clear and detailed description of your changes or additions.
4. Submit a pull request: Open a pull request with a clear title and description. Link any relevant issues.

## Updating and Deploying Changes

To update and deploy the documentation, follow these steps:

- Ensure MkDocs is Installed: If you haven't installed MkDocs, you can do so by running `pip install mkdocs` in your terminal.
- Make Your Documentation Changes: Update or add new Markdown files within the docs directory. Make sure to preview your changes locally by running `mkdocs serve` from your project directory.
- Deploy Your Changes: After making your updates, deploy the documentation to GitHub Pages by running `mkdocs gh-deploy`. This command will build your site and push the generated site files to the gh-pages branch of the repository.
- Commit Your Source Changes: Don’t forget to commit the changes made to your source documentation files and the mkdocs.yml configuration file to your branch. Push these commits to your forked repository before or after deploying with `mkdocs gh-deploy`.

```bash
git add .
git commit -m "Describe your documentation updates"
git push origin <your-branch>
