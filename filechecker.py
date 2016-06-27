import os
import sys
import codecs
import pickle
import argparse

def partition(iterable, pred):
    trues = []
    falses = []
    for item in iterable:
        if pred(item):
            trues.append(item)
        else:
            falses.append(item)
    return trues, falses

def canopen(path):
    try:
        open(path, "rb")
        return True
    except:
        return False

def isfile(path):
    return os.path.isfile(path)

def shouldignore(path):
    name = os.path.basename(path)
    return name.startswith('.') or name == "desktop.ini" or name == "Thumbs.db"

class CheckedFolder:
    def __init__(self, path):
        print("Checking {}".format(path))

        self.path = path
        self.names = [os.path.join(path, name) for name in os.listdir(path)]
        files, dirs = partition(self.names, isfile)
        self.goodfiles, self.badfiles = partition(files, canopen)

        self.folders = []
        for d in dirs:
            self.folders.append(CheckedFolder(d))

    def cleanfiles(self):
        self.goodfiles = [f for f in self.goodfiles if not shouldignore(f)]
        self.badfiles  = [f for f in self.badfiles  if not shouldignore(f)]

    def allgoodfiles(self):
        return not self.badfiles

    def allbadfiles(self):
        return not self.goodfiles

    def nofiles(self):
        g = not self.goodfiles
        b = not self.badfiles
        return g and b

    def allgood(self):
        return self.allgoodfiles() and all(f.allgood() for f in self.folders) # all folders good

    def allbad(self):
        return self.allbadfiles() and all(f.allbad() for f in self.folders) # all folders bad

    def empty(self):
        return self.nofiles() and not self.folders

    def prettyprint(self, depth = 0):
        indent =  "   " * depth
        indentx = "   " * (depth+1)
        name = os.path.basename(self.path)
        if self.empty():
            print("{}[ ]: {} -> This is an empty folder.".format(indent, name))
        elif self.allgood():
            print("{}+++: {} -> All files and folders are good.".format(indent, name))
        elif self.allbad():
            print("{}---: {} -> All files and folders are bad.".format(indent, name))
        else:
            print("{}???: {}".format(indent, name))
            if self.nofiles():
                print("{}f[]: No files in this folder".format(indentx))
            elif self.allgoodfiles():
                print("{}f++: All files good".format(indentx))
            elif self.allbadfiles():
                print("{}f--: All files bad".format(indentx))
            else:
                for good in self.goodfiles:
                    name = os.path.basename(good)
                    print("{}f++: {}".format(indentx, name))
                for bad in self.badfiles:
                    name = os.path.basename(bad)
                    print("{}f--: {}".format(indentx, name))
            for child in self.folders:
                child.prettyprint(depth+1)

# Main
# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('path', help="Either a folder to be checked, or a file with previously saved information.")
parser.add_argument("-s", "--save", default="save.checked", help="Where the information about the folder should be saved. Only done when checking a folder.")
args = parser.parse_args()

if os.path.isdir(args.path):
    info = CheckedFolder(args.path)
    if args.save is not None:
        print("Saved to {}".format(args.save))
        pickle.dump(info, open(args.save, "wb"))
elif os.path.isfile(args.path):
    info = pickle.load(open(args.path, "rb"))
else:
    parser.print_help()
    print("Either a file or folder is required, given path leads to nothing useable.")
    exit(2)

# Might cause problems with unicode chars in windows cmd, run "chcp 65001" to fix
info.prettyprint()
