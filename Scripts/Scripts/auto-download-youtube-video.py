import os
from os import path
from pathlib import Path
from time import sleep
import frontmatter
import glob

# set the working to directory to the project root
os.chdir("../")

# read in the YAML frontmatter from the first file in "Inbox" folder
with open("Inbox/2023-09-25-20-04-26.md", "r", encoding='utf8') as file:
    post = frontmatter.load(file)
    lines = file.readlines()


# get the URL from the YAML frontmatter
url = post["URL"]

# detect if the URL is a YouTube video
if "youtube.com" in url:

    # construct the command to download the video
    # TODO what current directory is the command being executed in?
    command = f"youtube-dl.exe -f best -o '%(title)s.%(ext)s' {url}"

    # execute the command
    os.system(command)

    # wait for the video to download
    sleep(5)

    dir_path: str = os.getcwd()

    for file in os.listdir(dir_path):
        print(file)

    video_filename = []

    for file in os.listdir(dir_path):
        if file.endswith(".mp4"):
            video_filename.append(file)
    print(video_filename)

    # search_path: str = path.join(os.getcwd(), "*.mp4")

    # get the filename of the downloaded video
    # video_filename = glob.glob(search_path)

    # remove any special characters from the filename


    # write the video filename to the H1 in the Markdown file
    for line in lines:
        if line.startswith('# '):
            line = line + video_filename
            print(line)


# TODO Option 2 - write the video title to H1 in the Markdown file

