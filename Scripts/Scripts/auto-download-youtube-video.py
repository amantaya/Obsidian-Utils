import os
from os import path
from pathlib import Path
import frontmatter

# set the working to directory to the project root
os.chdir("../")

# read in the YAML frontmatter from the first file in "Inbox" folder
with open("Inbox/2020-05-01-what-is-a-frontend-developer.md", "r") as file:
    post = frontmatter.load(file)

# get the URL from the YAML frontmatter
url = post["URL"]

# detect if the URL is a YouTube video
if "youtube.com" in url:
    # extract the video ID from the URL
    video_id = url.split("v=")[1]

    # construct the command to download the video
    command = f"youtube-dl -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' https://www.youtube.com/watch?v={video_id}"

    # execute the command
    os.system(command)
