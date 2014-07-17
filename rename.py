#!/usr/bin/env  python3

# Someday I'll get this shit done!

import os


for dir in os.listdir():
    if os.path.isdir(dir):
        print(dir)
        nome = input("Nome:")
        if nome == "skip" :
            continue
        name = input("Name:")
        if name == "" :
            name = nome
        year = input("Ano:")
        newdir = name + " [" + year + "]"
        for file in os.listdir(dir):
            oldfile = dir + os.sep + file
            newfile = dir + os.sep + nome
            ext = file.rpartition('.')[2]
            if "[Eng].srt" in file or "[Eng][Subs]" in file:
                newfile += " [Eng]" + os.extsep + ext
            else:
                newfile += os.extsep + ext
            print(oldfile + "-->" + newfile)
            os.rename(oldfile,newfile)
        print(dir + "-->" + newdir)
        os.rename(dir,newdir)
print("All done for now!")
