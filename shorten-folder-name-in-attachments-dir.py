import os
import re
import subprocess
import pathlib
from pathlib import Path

cwd = os.getcwd()

# location of the Obsidian vault
abs_path_to_vault = Path("C:/Users/andre/personal-knowledge")

# change cwd to the vault directory so that the script can find the files
os.chdir(abs_path_to_vault)

# create a path to the files that need to be renamed
# by appending a sub-directory to the file path
abs_path_to_attachments = abs_path_to_vault / "Attachments"

# change cwd to where the files are located
# because open.file will fail if files are not in cwd
# (or you supply a full path, which will complicate the renaming process)
os.chdir(abs_path_to_attachments)

# list all the files in the subdirectory
# some of these files we want to rename, but not all of them
attachment_folders_abs_path = [
    f for f in abs_path_to_attachments.iterdir() if f.is_dir()
]

attachment_folders = [
    f.name for f in attachment_folders_abs_path
    ]


# remove the prefix from the file name which consists of
# the date and the time the file was created
# using a regular expression
# YYYY-MM-DD-HH-MM-SS
def remove_date_prefix(file_name: str) -> str:
    return re.sub(
        pattern=r"^\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}\s",
        repl="",
        string=file_name
    )


# remove the prefix from the file name
folders_without_date_prefix = [
    remove_date_prefix(folders) for folders in attachment_folders
]


# trim the folder name to 150 characters
def trim_foldername(folder_name: str, max_length: int) -> str:
    return folder_name[:max_length]


new_folder_names = [
    trim_foldername(folder, 150) for folder in folders_without_date_prefix
    ]

commands_list = []

git_worktree = "--work-tree=$HOME/personal-knowledge/"

git_dir = "--git-dir=$HOME/personal-knowledge/.git"

# make new directories
for folder in attachment_folders:
    new_folder_name = remove_date_prefix(folder)
    new_folder_name = trim_foldername(new_folder_name, 150)
    new_abs_path = pathlib.PureWindowsPath(
        os.path.join(abs_path_to_attachments, new_folder_name)
    )
    new_abs_path_posix = new_abs_path.as_posix()
    new_abs_path_escaped = re.sub(
        pattern='`', repl='\\\\`', string=new_abs_path_posix
    )
    command = subprocess.list2cmdline(["mkdir", new_abs_path_escaped])
    commands_list.append(command)

os.chdir(cwd)

# write the commands to a shell script
with open("mkdir-commands.sh", "w", encoding="utf-8") as f:
    for command in commands_list:
        f.write(command + "\n")

# add bin bash to the top of the file
with open("mkdir-commands.sh", "r+", encoding="utf-8") as f:
    content = f.read()
    f.seek(0, 0)
    f.write("#!/bin/bash\n" + content)

# run shell script to rename files
# subprocess.run(["mkdir-commands.sh"], shell=True, cwd=cwd)

# now we need to move the files to the new directories
# this is a bit more complicated because we need to
# create a list of commands to move the files
# and write them to a shell script
# and then
# run the shell script

# create a list of commands to move the files
# to the new directories
commands_list = []

for folder in attachment_folders:
    new_folder_name = remove_date_prefix(folder)
    new_folder_name = trim_foldername(new_folder_name, 150)
    new_abs_path = pathlib.PureWindowsPath(
        os.path.join(abs_path_to_attachments, new_folder_name)
    )
    new_abs_path_posix = new_abs_path.as_posix()
    new_abs_path_escaped = re.sub(
        pattern='`', repl='\\\\`', string=new_abs_path_posix
    )
    old_abs_path = pathlib.PureWindowsPath(
        os.path.join(abs_path_to_attachments, folder)
    )
    old_abs_path_posix = old_abs_path.as_posix()
    old_abs_path_escaped = re.sub(
        pattern='`', repl='\\\\`', string=old_abs_path_posix
    )
    src = old_abs_path_escaped
    dst = new_abs_path_escaped
    command = subprocess.list2cmdline(
        ["git", git_dir, git_worktree, "mv", src, dst]
    )
    commands_list.append(command)

# write the commands to a shell script
with open("git-mv-dir-commands.sh", "w", encoding="utf-8") as f:
    for command in commands_list:
        f.write(command + "\n")

# add bin bash to the top of the file
with open("git-mv-dir-commands.sh", "r+", encoding="utf-8") as f:
    content = f.read()
    f.seek(0, 0)
    f.write("#!/bin/bash\n" + content)
