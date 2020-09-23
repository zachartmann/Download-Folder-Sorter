import os, time, shutil
from pathlib import Path
from mac_tags import Tags

PATH_TO_WATCH = "WHERE_YOU_ARE_DOWNLOADING_TO" # Directory watching for additions
ADD_ROOT_DIR = "THE_ROOT_DIR_FOR_SORTING" # Top directory to add to (with child directories chosen later)

class FileDetails(object):
    def __init__(self, file_title, file_directory, file_rating):
        self.file_title = file_title
        self.file_directory = file_directory
        self.file_rating = file_rating

def get_file_directory(current_dir):
    for root, dirs, files in os.walk(current_dir):
        if not dirs: # Leaf node:
            return current_dir
        
        # Get a list of directories they can choose
        dir_choice = input("Choose a directory. {0}: ".format(list_dirs(dirs)))
        # Re ask them if it fails
        valid_choice = dir_choice in dirs
        while not valid_choice:
            dir_choice = input("Invalid choice. {0}: ".format(list_dirs(dirs)))
            valid_choice = dir_choice in dirs

        # Get path to choice
        next_dir = os.path.join(root, dir_choice)
        # Recurse
        return get_file_directory(next_dir)

def list_dirs(dirs):
    final_string = ''
    for dir in dirs:
        final_string += "{0}, ".format(dir)
    return final_string[:-2] # Remove final ", "

def get_file_details(title):
    directory = get_file_directory(ADD_ROOT_DIR)
    file_rating = input("Rating (1-7) (0 to skip) = ")
    while file_rating.upper() not in ['1', '2', '3', '4', '5', '6', '7']:
        file_rating = input("Try again. Rating (1-7) = ")
    return FileDetails(title, directory, file_rating)

def tag_document(FILE_PATH, file_rating):
    doc = Tags(FILE_PATH)
    # My personal rating system
    if file_rating == '0':
        return # Skip tagging
    elif file_rating == '1':
        doc.add("Purple")
    elif file_rating == '2':
        doc.add("Blue")
    elif file_rating == '3':
        doc.add("Green")
    elif file_rating == '4':
        doc.add("Yellow")
    elif file_rating == '5':
        doc.add("Orange")
    elif file_rating == '6':
        doc.add("Red")
    elif file_rating == '7':
        doc.add("Red", "Grey")

before = os.listdir(PATH_TO_WATCH)
while True:
    time.sleep(1)
    after = os.listdir(PATH_TO_WATCH)
    added = [x for x in after if not x in before]
    if added:
        for title in added:
            if ".com" in title: # Remove google's temporary download files
                break
            print("File added: {0}".format(title))
            print("================")
            file_details = get_file_details(title)
            # Get the path of the file where it begins
            origin_file = "{0}/{1}".format(PATH_TO_WATCH, file_details.file_title)
            # Move it to the directory chosen
            shutil.move(origin_file, file_details.file_directory)
            # Get the path of the file now that it's been moved
            destination_file = "{0}/{1}".format(file_details.file_directory, file_details.file_title)
            # Set the tag
            tag_document(destination_file, file_details.file_rating)