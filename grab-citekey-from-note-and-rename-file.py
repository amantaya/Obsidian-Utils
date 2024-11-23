import os
import re
import subprocess
import pathlib
from pathlib import Path
import time

cwd = os.getcwd()

# location of the Obsidian vault
abs_path_to_vault = Path("C:/Users/andre/personal-knowledge")

# change cwd to the vault directory so that the script can find the files
os.chdir(abs_path_to_vault)

# create a path to the files that need to be renamed
# by appending a sub-directory to the file path
abs_path_to_files = abs_path_to_vault / "Resources"

# change cwd to where the files are located
# because open.file will fail if files are not in cwd
# (or you supply a full path, which will complicate the renaming process)
os.chdir(abs_path_to_files)

# list all the files in the subdirectory
# some of these files we want to rename, but not all of them
note_files = os.listdir(abs_path_to_files)

# remove the prefix from the file name which consists of
# the date and the time the file was created
# using a regular expression
# YYYY-MM-DD-HH-MM-SS
def remove_date_prefix(file_name: str) -> str:
    return re.sub(pattern=r"^\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}\s", repl="", string=file_name)

# remove the prefix from the file name
file_names_without_prefix = [remove_date_prefix(file) for file in note_files]

def trim_filename(file_name: str, max_length: int) -> str:
    file_path = Path(file_name)
    base_name = file_path.stem
    ext = file_path.suffix

    if len(base_name) > max_length:
        base_name = base_name[:max_length]

    new_file_name = base_name + ext
    return new_file_name

new_file_names = [trim_filename(file, 150) for file in file_names_without_prefix]

commands_list = []

for file in note_files:
    src = pathlib.PureWindowsPath(os.path.join(abs_path_to_files, file))
    src = src.as_posix()
    src = re.sub(pattern='`', repl='\\\\`', string=src) # escape backticks which are special characters in shell
    new_file_name = remove_date_prefix(file)
    new_file_name = trim_filename(new_file_name, 150)
    dst = pathlib.PureWindowsPath(os.path.join(abs_path_to_files, new_file_name))
    dst = dst.as_posix()
    commands_list.append(subprocess.list2cmdline(["git", "mv", src, dst]))

os.chdir(cwd)

# write the commands to a shell script
with open("git-rename-commands.sh", "w", encoding="utf-8") as f:
    for command in commands_list:
        f.write(command + "\n")

# add bin bash to the top of the file
with open("git-rename-commands.sh", "r+", encoding="utf-8") as f:
    content = f.read()
    f.seek(0, 0)
    f.write("#!/bin/bash\n" + content)

# run shell script to rename files
# subprocess.run(["git-rename-commands.sh"], shell=True, cwd=cwd)
