# File Checker

A very simple python program that checks files in a folder.
It tries to open all files in the folder and subfolders, then reports which can and can't be opened.

I used this when a home server, with a bunch of old files, crashed.
The server still had references to files, without knowing they were lost.
So the files showed up in explorer, but when opened an error was given on some (but not all) files.
This script helped me find out which files were lost and which were still there.
Luckily there weren't any really important files on there, but still nice to know which could be saved.

## Usage

    filechecker.py [-h] [-s SAVE] path

path: Either the folder to be checked, or a file to previously saved information.
-s SAVE, --save SAVE: Where the information should be saved if you want.

### UnicodeEndoceError

If you get a "UnicodeEndoceError" this is because by default the Windows console can't show UTF-8 properly.
To fix this I had to run "chcp 65001" before running the script.
This is only a problem is there are some special characters in your folder names.

## Output

The script will show which folder it is checking now, so you know it's working.
Then it will output the folder structure, indicating which files can and can't be opened.
If all files in a folder (and its subfolders) can be opened, it will collapse that folder, stating that everything is fine in there, to reduce clutter.

* +++ means that all the files in the folder and subfolders can be opened
* --- means that none of the files nor files in subfolders could be opened
* ??? means some can and some can't be opened
* [ ] is an empty folder
* f++ indicates that the file can be opened
* f-- indicates that the file can't be opened

If the folder you are checking is entirely fine, which is should unless you had a similar crash as me, all it will output is:

    +++: FolderName

If nothing can be opened:

    ---: FolderName

Otherwise something like:

    +++: GoodFolder
    ---: BadFolder
    ???: OtherFolder
        f++: Good file
        f--: Missing file
        +++: ANother good folder

    ...and so one...
