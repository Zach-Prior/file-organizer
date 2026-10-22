# File Organizer

## Description

- The purpose of this project was to create a simple command line script to organize directories easily. Users can run this script in any directory on their machine and it will sort all files in said directory into subfolders based on file type.

## Features

- The script has support for 5 file Categories
    - PDFs: .pdf files
    - Images: .jpg, .jpeg, .png, .gif, .svg files
    - Documents: .doc, .docx, .txt, .md, .rtf files
    - Spreadsheets: .xls, .xlsx, .csv files
    - Archives: .zip, .rar, .tar, .gz files
    - Other: any files not listed will be put in a fallback directory
- The script also will add numbered suffixes to files that share the same name.
- The --dry-run arguement was also implemented in the program to allow a user to see the changes the program would make without actually changing the target directory. Running the command with this arguement will simply display the moves the program would make to the terminal.
- Some additional features are that the script will preserve existing subdirectories already in your folder, the script also prevents itself from moving itself, and the the script also handles permissions and file operation errors.

## Requirments

- Python 3.14.7 or newer.
- Uses Pythons built in [argparse](https://docs.python.org/3/library/argparse.html), [shutil](https://docs.python.org/3/library/shutil.html), [sys](https://docs.python.org/3/library/sys.html), and [pathlib](https://docs.python.org/3/library/pathlib.html) modules
- This script has no external dependencies.

## Installation

- Simply clone the repository by clicking the code button, copying the https link of the repository, and then pasting the link in your IDE of choice. 
- Alternatively you can simply install the script istself. you can click the file_organizer.py file in the repository's home, and then click the download raw file button to download just the script.
- In order to be ready to use the script, in your terminal you need to navigate to the directory where the script is located. If you cloned the whole repo, then simply navigate to the file-organizer directory in your terminal. If you copied the raw python file, you need to navigate to the directory wherever you downloaded the file.
