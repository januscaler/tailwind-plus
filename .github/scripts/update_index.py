import os
import github
from github import Github

# Initialize GitHub API with the token
g = Github(os.environ['GITHUB_TOKEN'])
repo = g.get_repo(os.environ['GITHUB_REPOSITORY'])

# Function to get all markdown files in the repository
def get_markdown_files():
    markdown_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.md') and file != 'README.md':
                markdown_files.append(os.path.relpath(os.path.join(root, file), '.'))
    return markdown_files

# Function to update README.md
def update_readme(markdown_files):
    readme_content = "# Index of Documentation\n\n"
    for file in sorted(markdown_files):
        # Convert path to link
        link = file.replace('.md', '').replace(' ', '-').lower()
        readme_content += f"- [{file}](/{(file)}) \n"
    
    with open('README.md', 'w') as readme:
        readme.write(readme_content)

# Main execution
if __name__ == "__main__":
    markdown_files = get_markdown_files()
    update_readme(markdown_files)
    
    # Commit and push changes
    commit_message = "Automatically update index in README.md"
    repo.create_file(
        "README.md",
        commit_message,
        open("README.md", "r").read(),
        branch="main"
    )
