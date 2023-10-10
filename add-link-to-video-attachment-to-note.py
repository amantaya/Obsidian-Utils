
# grab the original H1 title
# original_h1 = post.content.splitlines()[0]
#
# # write the video filename to the H1 in the Markdown file
# post.content = post.content.replace(post.content.splitlines()[0], f"{original_h1} YouTube Video - {new_h1[0]}")
#
# # write YouTube video to YAML frontmatter
# post['item type'] = 'YouTube video'
#
# # break the string into a list of lines
# post_content_list = post.content.splitlines(True)
#
# # insert the list item right after the H1
# post_content_list.insert(1, f"\n![](Attachments/{new_video_filename[0]}.mp4)\n")
#
# # join the list back into a string
# post.content = "".join(post_content_list)
#
# # write the YAML frontmatter back to the Markdown file
# print(frontmatter.dumps(post))
#
# frontmatter.dump(post, f"Resources {markdown_files_with_youtube_url[0]}")

# TODO write a git commit message that includes the original filename and the new filename

# move the Markdown file to the "Resources" folder
# os.rename("Inbox/2023-09-25-20-04-26.md", "Resources/2023-09-25-20-04-26.md")
