"""
This script is meant to find duplicate files in a directory and subdirectories via md5 checksums
Any collisions found are listed.
Collisions are any two files with the same md5 hash value.
"""

from hashlib import md5
import os

rootDir="/home/user/Music/"
renamedCount = 0
fileDict = {}
collisions=0
targetPercent=10

#returns an md5 hash of a file - found at https://gist.github.com/Jalkhov
def getMD5Hash(fname):
    hashObj = md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hashObj.update(chunk)
    return hashObj.hexdigest()

#returns a string list of file paths for all files in a directory and its subdirectories - refer to os.walk(dir)
def get_filepaths(directory):
    
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, _, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return file_paths

filePaths = get_filepaths(rootDir) #root directory to search

#exit if 1 or 0 files exist in directory
if len(filePaths)>1:
    print("%i files found in %s\nPopulating dictionary. This may take a while."%(len(filePaths),rootDir))
else:
    print("Too few files in directory")
    exit()
#iterate over the string list of file paths and populates a hashtable

for i,filepath in enumerate(filePaths):

    #add some visual feedback
    percent = int(100*float(i)/len(filePaths))
    if percent>=targetPercent:
        targetPercent+=10
        print("%s%% processed"%percent)

    #populate hash table
    key = getMD5Hash(filepath)
    if key in fileDict.keys(): #add to a pre-existing list
        fileDict[key].append(filepath)
        collisions+=1
    else: #create a new list under the key
        fileDict[key]=[filepath]

#list collisions if any (collisions will be any list in our hashtable greater than size 1)
print("%i collisions found:"%collisions)
if collisions>1:
    collisions=0 #recycle this variable
    for fList in fileDict.values():
        if len(fList)>1:
            collisions+=1
            print(collisions)
            for duplicate in fList:
                print("\t"+duplicate)
print("Finished.")