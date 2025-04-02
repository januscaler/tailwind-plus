import os
import github
from github import Github

# Initialize GitHub API with the token
g = Github(os.environ['GIT_TOKEN'])
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
    return readme_content

# Main execution
if __name__ == "__main__":
    markdown_files = get_markdown_files()
    print(markdown_files)
    new_content = update_readme(markdown_files)
    
    # Check if README.md exists
    try:
        readme = repo.get_contents("README.md")
        # If README.md exists, update it
        repo.update_file(
            "README.md",
            "Automatically update index in README.md",
            new_content,
            readme.sha,
            branch="main"
        )
    except github.GithubException as e:
        # If README.md does not exist, create it
        if e.status == 404:
            repo.create_file(
                "README.md",
                "Automatically update index in README.md",
                new_content,
                branch="main"
            )
        else:
            raise e
