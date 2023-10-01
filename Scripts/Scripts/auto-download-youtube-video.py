import os
import re
from os import path
from pathlib import Path
from time import sleep
import frontmatter
import glob

# set the working to directory to the project root
os.chdir("../")

dir_path: str = os.getcwd()

markdown_files = []

# list all Markdown files in the "Inbox" folder
for file in os.listdir(dir_path):
    if file.endswith('.md'):
        markdown_files.append(file)

# remove files that don't have a YouTube link in the "URL" of the YAML frontmatter
for file in markdown_files:
    with open(f"Inbox/{file}", "r", encoding='utf8') as file:
        post = frontmatter.load(file)
        if "https://youtube.com" not in post["URL"]:
            markdown_files.remove(file)

for file in markdown_files:
    # read in the YAML frontmatter from the first file in "Inbox" folder
    with open(f"Inbox/{markdown_files[file]}", "r", encoding='utf8') as file:
        post = frontmatter.load(file)

    # get the URL from the YAML frontmatter
    url = post["URL"]

    # construct the command to download the video
    # TODO what current directory is the command being executed in?
    command = f"youtube-dl.exe -f best -o %(title)s.%(ext)s {url}"

    # execute the command
    os.system(command)

    # grab the orginal filename of the video
    original_video_filename = []

    for file in os.listdir(dir_path):
        if file.endswith('.mp4'):
            original_video_filename.append(file)

    print(original_video_filename)

    # remove any forbidden characters from the filename
    new_video_filename = [re.sub(r'[\\/*?:"<>|]', "", x) for x in original_video_filename]

    # remove any non-ASCII characters from the filename
    new_video_filename = [re.sub(r'[^\x00-\x7F]+', "", x) for x in new_video_filename]

    # remove "!" from the filename
    new_video_filename = [x.replace('!', '') for x in new_video_filename]

    # remove #" from the filename
    new_video_filename = [x.replace('#', '') for x in new_video_filename]

    # create a filename for the markdown h1 header based on the video filename
    new_h1 = [x.replace('.mp4', '') for x in new_video_filename]

    # remove spaces from the filename
    new_video_filename = [x.replace(' ', '-') for x in new_video_filename]

    # remove the file extension from the filename
    video_filename = [os.path.splitext(x)[0] for x in video_filename]

    # write the video filename to the H1 in the Markdown file
    post.content = post.content.replace(post.content.splitlines()[0], f"{original_h1} YouTube Video - {new_h1[0]}")

    # write YouTube video to YAML frontmatter
    post['item type'] = 'YouTube video'

    # write the YAML frontmatter back to the Markdown file
    print(frontmatter.dumps(post))

    frontmatter.dump(post, f"Inbox/{markdown_file}")

# TODO Option 2 - write the video title to H1 in the Markdown file
