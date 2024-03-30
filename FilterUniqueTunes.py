# Filtering to remove duplicate (different versions) of the same tune from the tune from the Tunes folder
# Rhys O'Higgins, 3/24
# Code help from:
# https://www.geeksforgeeks.org/copy-all-files-from-one-directory-to-another-using-python/

from pathlib import Path
import shutil
import os

files = os.listdir("Tunes")

for file in files: # file is a string with the name of the file
    if not "version" in file:
        if not any(vnum in file for vnum in ["v1", "v2", "v3","v4","v5","v6"]):
            shutil.copy2(os.path.join('Tunes',file), 'UniqueTunes')