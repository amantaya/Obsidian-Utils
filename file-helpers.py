import os
import shutil
import subprocess

cwd = os.getcwd()

print(cwd)

path_to_files = os.path.join(cwd, 'renamed')

# remove the test files if they exist
if os.path.isdir(path_to_files):
    try:
        shutil.rmtree(path_to_files)
    except OSError as e:
        print("Error: %s : %s" % (path_to_files, e.strerror))

# copy the original files to a new directory to test the renaming process
shutil.copytree(src='C:\\Users\\andre\\Dropbox\\dev\\sysadmin\\originals',
                  dst='C:\\Users\\andre\\Dropbox\\dev\\sysadmin\\renamed')

subprocess.run(["git", "add", "-A"], shell=True)  # add all files to git

subprocess.run(["git", "commit", "-m", "add all test files to version control"], shell=True)  # commit changes
