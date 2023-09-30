import os
from os import path
from pathlib import Path
from time import sleep

import frontmatter

# set the working to directory to the project root
os.chdir("../")

# read in the YAML frontmatter from the first file in "Inbox" folder
with open("Inbox/2023-09-25-20-04-26,md", "r") as file:
    post = frontmatter.load(file)

# get the URL from the YAML frontmatter
url = post["URL"]

# detect if the URL is a YouTube video
if "youtube.com" in url:
    # extract the video ID from the URL
    video_id = url.split("v=")[1]

    # construct the command to download the video
    # TODO what current directory is the command being executed in?
    command = f"youtube-dl.exe -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' -o 'Inbox/%(title)s.%(ext)s' https://www.youtube.com/watch?v={video_id}"

    # execute the command
    os.system(command)

    # wait for the video to download
    sleep(180)

    # get the filename of the downloaded video
    video_filename = Path("Inbox").glob("*.mp4")[0]

    # set the title of the post to the title of the video
    post["title"] = post["title"] + video_filename

    # write the YAML frontmatter back to the file
    frontmatter.dump(post, file)

# TODO Option 2 - write the video title to H1 in the Markdown file

