import os
import re
import argparse

EXTENSIONS = ('.txt', '.py', '.html', '.css', '.js', '.toml', '.rst', '.yml', '.yaml', 'Dockerfile', 'dockerfile', '.conf', '.ini')


def rename_files_and_dirs(directory, old_word, new_word):
    for root, dirs, files in os.walk(directory, topdown=False):  # bottom-up to rename files first
        # Rename files
        for file in files:
            if file == 'rename_project.py':
                continue            
            if old_word in file:
                old_path = os.path.join(root, file)
                new_path = os.path.join(root, file.replace(old_word, new_word))
                os.rename(old_path, new_path)
                print(f'Renamed file: {old_path} -> {new_path}')
        # Rename directories
        for dir_name in dirs:
            if old_word in dir_name:
                old_path = os.path.join(root, dir_name)
                new_path = os.path.join(root, dir_name.replace(old_word, new_word))
                os.rename(old_path, new_path)
                print(f'Renamed directory: {old_path} -> {new_path}')
                
                
def search_word_in_files(directory, search_word, extensions=EXTENSIONS):
    search_pattern = re.compile(re.escape(search_word))
    for root, _, files in os.walk(directory):
        for file in files:
            if file == 'rename_project.py':
                continue
            if file.endswith(extensions):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        for line_num, line in enumerate(f, start=1):
                            if search_pattern.search(line):  # Match found
                                print(f'{file_path}:{line_num}: {line.strip()}')  # Show match
                except Exception as e:
                    print(f'Could not read {file_path}: {e}')


def replace_word_in_files(directory, old_word, new_word, extensions=EXTENSIONS):  
    for root, _, files in os.walk(directory):
        for file in files:
            if file == 'rename_project.py':
                continue
            if file.endswith(extensions):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                if old_word in content:
                    new_content = content.replace(old_word, new_word)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f'Replaced in: {file_path}')
                    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('name', help='New name for project')
    parser.add_argument('--files-and-dirs', action='store_true', help='Renames files and directories')
    parser.add_argument('--file-contents', action='store_true', help='Renames file contents')
    args, _ = parser.parse_known_args() # Ignore any Briefcase args 
    if args.files_and_dirs:
        print('Renaming files and directories...')
        rename_files_and_dirs('.', 'mydjangoapp', args.name.lower())
    elif args.file_contents:
        print('Renaming file contents...')
        replace_word_in_files('.', 'mydjangoapp', args.name.lower())
        replace_word_in_files('.', 'MyDjangoApp', args.name)
    else:
        print('Renaming all...')
        rename_files_and_dirs('.', 'mydjangoapp', args.name.lower())
        replace_word_in_files('.', 'mydjangoapp', args.name.lower())
        replace_word_in_files('.', 'MyDjangoApp', args.name)


if __name__ == '__main__':
    main()