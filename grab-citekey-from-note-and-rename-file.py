import os
import re
import subprocess
import pathlib
from pathlib import Path
import time

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
list_files = os.listdir(abs_path_to_files)

# list the the files that have >= 255 characters in their name
files_with_long_names = list(filter(lambda v: len(v) >= 150, list_files))

# truncate the file names to 150 characters
new_file_name: list = []

commands_list: list = []

# remove the prefix from the file name which consists of
# the date and the time the file was created
# using a regular expression
def remove_prefix(file_name: str) -> str:
    return re.sub(pattern=r"^\d{4}-\d{2}-\d{2}\s\d{2}\.\d{2}\.\d{2}\s", repl="", string=file_name)

# remove the prefix from the file name
file_names_without_prefix = [remove_prefix(file) for file in list_files]


def trim_filename(file_name: str, max_length: int) -> str:
    file_path = Path(file_name)
    base_name = file_path.stem
    ext = file_path.suffix

    if len(base_name) > max_length:
        base_name = base_name[:max_length]

    new_file_name = base_name + ext
    return new_file_name

new_file_names = [trim_filename(file, 150) for file in list_files]

for file in files_with_long_names:
    new_file_name = file[:150]
    src = pathlib.PureWindowsPath(os.path.join(abs_path_to_files, file))
    src = src.as_posix()
    src = re.sub(pattern='`', repl='\\\\`', string=src)
    print(f"Original File Name: {src}")
    dst = pathlib.PureWindowsPath(os.path.join(abs_path_to_files, new_file_name))
    dst = dst.as_posix()
    print(F"New File Name:{dst}")
    time.sleep(3)
    commands_list.append(subprocess.list2cmdline(["git", "mv", src, dst]))

# write the commands to a shell script
with open("git-rename-commands.sh", "w") as f:
    for command in commands_list:
        f.write(command + "\n")

# add bin bash to the top of the file
with open("git-rename-commands.sh", "r+") as f:
    content = f.read()
    f.seek(0, 0)
    f.write("#!/bin/bash\n" + content)

# run shell script to rename files
# subprocess.run(["git-rename-commands.sh"], shell=True, cwd=cwd)
