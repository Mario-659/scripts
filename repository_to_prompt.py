# turns every file in given repository into promp
# if output is too large you can split it with some tool like https://chatgpt-prompt-splitter.jjdiaz.dev/ https://github.com/jupediaz/chatgpt-prompt-splitter

import os
import sys
import re


def get_repo_content(repo_path, max_chars=10000):
    content = ""

    for root, dirs, files in os.walk(repo_path):
        excluded_dirs = ['.vs', 'img', 'node_modules', '.git', 'build', 'dist', "test", "test_performance", "out", "cmake-build-debug-visual-studio", "venv", "vite", "cmake-build-release-mingw", "cmake-build-release-visual-studio"]
        included_file_extensions = ('.kt', '.js', '.ts', '.html', ".h", ".cpp", ".tex", ".bib", ".set", ".txt")

        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        
        for file in files:
            if file.endswith(included_file_extensions) and not file.endswith('.spec.ts'):
                file_path = os.path.join(root, file)
                print(f"reading: {file_path}")
                # content += os.path.relpath(file_path, repo_path)
                # content += "\n"

                with open(file_path, "r", encoding='utf8') as f:
                    file_content = f.read()

                    # Remove import lines and empty lines
                    file_content = re.sub(r"import.*\n|\n\s*\n", "", file_content)
                    
                    content += "---------------------\n"
                    content += os.path.relpath(file_path, repo_path)
                    content += "\n\n"
                    content += file_content
                    
    return  content


def create_prompt(repo_path, max_chars=10000):
    print(f"Analyzing repository: {repo_path}")
    content = get_repo_content(repo_path, max_chars)
    prompt = f"""
Analyze the following repository content:

{content}

Based on this code and structure, please provide:
1. A brief summary of the project and its main functionalities.
2. An overview of the project's directory structure and organization.
3. Any notable patterns, practices, or architectural decisions you observe.
4. Potential areas for improvement or optimization, if any.
"""
    return prompt


def main():
    # Check if a repo path is provided as a command-line argument
    if len(sys.argv) > 1:
        repo_path = sys.argv[1]
    else:
        # If no argument is provided, try to read from stdin (for piping)
        repo_path = sys.stdin.read().strip()

    # If we still don't have a repo path, print usage and exit
    if not repo_path:
        print("Usage: python script.py <repo_path>")
        print("   or: echo <repo_path> | python script.py")
        sys.exit(1)

    # Ensure the repo path exists
    if not os.path.exists(repo_path):
        print(f"Error: The repository path '{repo_path}' does not exist.")
        sys.exit(1)

    prompt = create_prompt(repo_path)

    with open("generated_prompt.txt", "a", encoding="utf-8") as f:
        f.write(prompt)


if __name__ == "__main__":
    main()
