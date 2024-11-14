import os
import shutil

def erase_folder():
    folder_path = "images"
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        os.makedirs(folder_path)
        print("Folder deleted and created again.")
    else:
        os.makedirs(folder_path)
        print("Folder created.")

if __name__ == "__main__":
    erase_folder()