import os
from os import path
from pathlib import Path

# set the working to directory to the project root
os.chdir("../")

# for loop to iterate through all the files in the "Inbox" folder
for file in os.listdir("Inbox"):
    read_file = open("Inbox/" + file, "r")
    

path_to_url:  =