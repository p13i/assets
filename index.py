import os
import html

def build_directory_structure(path):
    """
    Recursively builds a dictionary representing the directory structure,
    ignoring directories that start with a dot, and uses relative paths to the current directory.
    Additionally, creates an index.html file for each subdirectory.
    """
    structure = {}
    cwd = os.getcwd()  # Get the current working directory
    
    # Create an index.html for the current directory
    generate_index_html(path)

    with os.scandir(path) as it:
        for entry in it:
            if entry.name.startswith('.'):
                continue  # Ignore hidden directories
            rel_path = os.path.relpath(entry.path, cwd)  # Get the relative path to CWD
            if entry.is_dir(follow_symlinks=False):
                structure[entry.name] = {
                    "type": "directory",
                    "url": entry.name,  # Use relative path from current directory
                    "contents": build_directory_structure(entry.path)
                }
            else:
                structure[entry.name] = {
                    "type": "file",
                    "url": entry.name  # Use relative path from current directory
                }
    return structure

def generate_index_html(path):
    """
    Generates an index.html file for the given directory.
    It lists all files and subdirectories in that directory with links to them.
    The <h1> tags for files and directories are wrapped with <code> tags for display.
    Links are relative to the current directory.
    """
    cwd = os.getcwd()  # Get the current working directory
    rel_path = os.path.relpath(path, cwd)  # Get the relative path to CWD

    # Only generate an index.html if it's a directory
    if os.path.isdir(path):
        index_html_path = os.path.join(path, "index.html")
        with open(index_html_path, "w") as f:
            f.write("<!DOCTYPE html>\n<html lang='en'>\n<head>\n")
            f.write("<meta charset='UTF-8'>\n<title>Index of {}</title>\n".format(html.escape(rel_path)))
            f.write("</head>\n<body>\n")
            f.write("<h1>Index of <code>{}</code></h1>\n".format(html.escape(rel_path)))
            f.write("<ul>\n")
            
            # List the contents of the current directory
            with os.scandir(path) as it:
                for entry in it:
                    if entry.name.startswith('.'):
                        continue  # Ignore hidden files and directories
                    
                    entry_rel_path = entry.name  # Path relative to the current directory
                    
                    if entry.is_dir(follow_symlinks=False):
                        # Recursively call the function to handle subdirectories
                        f.write(f'<li><a href="{entry_rel_path}/index.html"><code>{html.escape(entry.name)}/</code></a>\n')
                        # Recursively list files in the subdirectory
                        f.write("<ul>\n")
                        list_subdirectory_files(entry.path, f)
                        f.write("</ul>\n")
                        f.write("</li>\n")
                    else:
                        f.write(f'<li><a href="{entry_rel_path}"><code>{html.escape(entry.name)}</code></a></li>\n')
            
            f.write("</ul>\n")
            f.write("</body>\n</html>\n")

    print(f"Generated index.html for {rel_path}")

def list_subdirectory_files(path, file_handle):
    """
    Recursively lists all files in a subdirectory and writes them into the index.html.
    It creates a nested <ul> list for each subdirectory.
    """
    with os.scandir(path) as it:
        for entry in it:
            if entry.name.startswith('.'):
                continue  # Ignore hidden files and directories
            
            entry_rel_path = os.path.relpath(entry.path, os.getcwd())  # Relative path to the current directory

            if entry.is_dir(follow_symlinks=False):
                file_handle.write(f'<li><a href="{entry_rel_path}/index.html"><code>{html.escape(entry.name)}/</code></a>\n')
                file_handle.write("<ul>\n")
                # Recursively list files in the subdirectory
                list_subdirectory_files(entry.path, file_handle)
                file_handle.write("</ul>\n")
                file_handle.write("</li>\n")
            else:
                file_handle.write(f'<li><a href="{entry_rel_path}"><code>{html.escape(entry.name)}</code></a></li>\n')

# Change the path below to the directory you want to start from
if __name__ == "__main__":
    # Start from the current working directory or specify a different path
    start_path = os.getcwd()  # Or replace with a specific directory path
    build_directory_structure(start_path)
