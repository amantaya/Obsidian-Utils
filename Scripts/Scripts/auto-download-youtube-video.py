import os
import re
from os import path
from pathlib import Path
from time import sleep
import frontmatter
import glob
import yaml

# set the working to directory to the project root
os.chdir("../")

project_directory: str = os.getcwd()

notes_directory: str = os.path.join(project_directory, "Inbox")

markdown_files = []

# list all Markdown files in the "Inbox" folder
for file in os.listdir(notes_directory):
    if file.endswith('.md'):
        markdown_files.append(file)

# detect any files with invalid YAML frontmatter
for file in markdown_files:
    with open(f"Inbox/{file}", "r", encoding='utf8') as file:
        yaml.safe_load_all(file)

# TODO check for files that are missing the YAML frontmatter keys specified in the template

# TODO this fails of the file is missing the YAML frontmatter key "URL"
# initialize an empty list to store the markdown files that have a value that is not None in the key "URL"
markdown_files_with_valid_url_key_value = []

for file in markdown_files:
    with open(f"Inbox/{file}", "r", encoding='utf8') as f:
        post = frontmatter.load(f)
        if post["URL"] is not None:
            markdown_files_with_valid_url_key_value.append(file)

# initialize an empty list to store the markdown files that have a value of "youtube.com" in the key "URL"
markdown_files_with_youtube_key_value = []

# TODO find URLs that have "youtube.com" in the body of the markdown file
# TODO find URLs that have "youtu.be" in the body of the markdown file

# remove files that don't have a YouTube link in the "URL" of the YAML frontmatter
for file in markdown_files_with_valid_url_key_value:
    with open(f"Inbox/{file}", "r", encoding='utf8') as f:
            post = frontmatter.load(f)
            if "youtube.com" in post["URL"]:
                markdown_files_with_youtube_key_value.append(file)

for file in markdown_files_with_youtube_key_value:
    # read in the YAML frontmatter from the first file in "Inbox" folder
    with open(f"Inbox/{file}", "r", encoding='utf8') as file:
        post = frontmatter.load(file)

    # get the URL from the YAML frontmatter
    url = post["URL"]

    # construct the command to download the video
    # TODO what current directory is the command being executed in?
    command = f"youtube-dl.exe -f best -o %(title)s.%(ext)s {url}"

    # execute the command
    os.system(command)

    # grab the original filename of the video
    original_video_filename = []

    # TODO change to glob.glob to search for a file with a specific extension
    # this inadventaently overwrites the {file} variable from the for loop
    for files in os.listdir(project_directory):
        if files.endswith('.mp4'):
            original_video_filename.append(files)

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
    # new_video_filename = [x.replace(' ', '-') for x in new_video_filename]

    # remove the file extension from the filename
    new_video_filename = [os.path.splitext(x)[0] for x in new_video_filename]

    # TODO check if the file already exists before renaming
    # check if the file already exists before renaming
    if not os.path.exists(f"Attachments/{new_video_filename[0]}.mp4"):
        os.rename(original_video_filename[0], f"Attachments/{new_video_filename[0]}.mp4")

    # grab the original H1 title
    original_h1 = post.content.splitlines()[0]

    # write the video filename to the H1 in the Markdown file
    post.content = post.content.replace(post.content.splitlines()[0], f"{original_h1} YouTube Video - {new_h1[0]}")

    # write YouTube video to YAML frontmatter
    post['item type'] = 'YouTube video'

    # break the string into a list of lines
    post_content_list = post.content.splitlines(True)

    # insert the list item right after the H1
    post_content_list.insert(1, f"\n![](Attachments/{new_video_filename[0]}.mp4)\n")

    # join the list back into a string
    post.content = "".join(post_content_list)

    # write the YAML frontmatter back to the Markdown file
    print(frontmatter.dumps(post))

    frontmatter.dump(post, markdown_files_with_youtube_key_value[0])

    # TODO write a git commit message that includes the original filename and the new filename

    # move the Markdown file to the "Resources" folder
    # os.rename("Inbox/2023-09-25-20-04-26.md", "Resources/2023-09-25-20-04-26.md")
