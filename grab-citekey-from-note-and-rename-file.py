import os
import re
import subprocess
import pathlib
from pathlib import Path

# location of the Obsidian vault
path_to_vault = Path("C:/Users/andre/personal-knowledge")

# change cwd to the vault directory so that the script can find the files
os.chdir(path_to_vault)

vault_dir = os.getcwd()

# create a path to the files that need to be renamed
# by appending a sub-directory to the file path
path_to_files = os.path.join(vault_dir, "Resources")

# change cwd to where the files are located
# because open.file will fail if files are not in cwd
# (or you supply a full path, which will complicate the renaming process)
os.chdir(path_to_files)

# list all the files in the subdirectory
# some of these files we want to rename, but not all of them
list_files = os.listdir(path_to_files)

# check the file names before renaming
# print(list_files)

# create a RegEx that matches a file with a timestamp YYYY-MM-dd-hh-mm
# some files that do have timestamps are missing the seconds field
pattern = re.compile(pattern='([0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}-[0-9]{2})|([0-9]{12})')

# filter out file names that do not match the RegEx
# do not rename files that already have timestamps
files_without_timestamps = list(filter(lambda v: not pattern.match(v), list_files))

# check files that we don't want renamed were filtered out correctly
# print(files_without_timestamps)

commands_list = []

# rename files by the line starting with "Created:" which is inside the file
for file in files_without_timestamps:
    with open(file, 'r', encoding='utf8') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('date created:'):
                # extract just the time from the string
                # TODO better to use a regex here instead of hardcoding the index
                created_date = line[14:]
                created_date_drop_newline = re.sub(pattern='\n', repl='', string=created_date)
                created_date_strip_leading_and_trailing_whitespace = created_date_drop_newline.strip()
                # replace colons and spaces with dashes to be consistent with naming convention
                # YYYY-MM-dd-hh-mm-ss
                created_date_replace = re.sub(pattern='(:)|( )', repl='-', string=created_date_strip_leading_and_trailing_whitespace)
                new_filename_without_backticks = re.sub(pattern='`', repl='\'', string=file)
                new_file_name = created_date_replace + ' ' + new_filename_without_backticks
                # print(file)
                # print(new_file_name)
                src = pathlib.PureWindowsPath(os.path.join(path_to_files, file))
                src = src.as_posix()
                src = re.sub(pattern='`', repl='\\\\`', string=src)
                # print(src)
                dst = pathlib.PureWindowsPath(os.path.join(path_to_files, new_file_name))
                dst = dst.as_posix()
                # print(dst)
                # src = "'%s'" % src
                # dst = "'%s'" % dst
                # command = fr'"%ProgramFiles%\Git\bin\bash.exe" -c "git mv {src} {dst}"'
                # print(command)
                # subprocess.check_output(command, shell=True)
                # subprocess.run(["git", "mv", "-f", file, new_file_name], shell=True)
                commands_list.append(subprocess.list2cmdline(["git", "mv", src, dst]))

os.chdir(cwd)

with open("git-rename-commands.sh", "w") as f:
    for command in commands_list:
        f.write(command + "\n")

# add bin bash to the top of the file
with open("git-rename-commands.sh", "r+") as f:
    content = f.read()
    f.seek(0, 0)
    f.write("#!/bin/bash\n" + content)

# run shell script to rename files
subprocess.run(["git-rename-commands.sh"], shell=True, cwd=cwd)
