#!/usr/bin/env python3

# This series shat gonna haunt me forever X___________X
# Getting better, looks really good now!! ^^

import os, sys

def parsecli(argv):
    opts = {"sub":False, "pth":"", "ssn":"", "ep":"", "conf":True}

    for arg in argv:
        if '--path=' in arg:
            opts["pth"] = os.path.expanduser(arg.partition('=')[2])
        elif '--season=' in arg:
            opts["ssn"] = int(arg.partition('=')[2])
        elif '--eps=' in arg:
            opts["ep"] = os.path.expanduser(arg.partition('=')[2])
        elif arg == '--noconfirm':
            opts["conf"] = False
        elif ('-h' or '--help') in arg:
            print(argv[0]+" [--path=<>] [--season=<>] [--eps=<>] [--noconfirm]")
            exit(0)
    return opts

def interact(opts):
    a = {"pth":"Path", "ssn":"Season", "ep":"Ep file"}

    for k, v in opts.items():
        if v == "":
            tmp = input("{}: ".format(a[k]))
            if tmp.isdecimal():
                tmp = int(tmp)
            else:
                tmp = os.path.expanduser(tmp)
            opts[k] = tmp
    return opts

def listdir(path):
    tmp = os.listdir(path)
    tmp.sort()
    return tmp

def formato(ssn, ep, name, ext):
    return "{0}x{1} - {2}{3}{4}".format(ssn, ep, name, os.extsep, ext)

def reformat(old, new, season, length):
    nu_list = []
    num = ""

    for i in range(1, length):
        if "-" in num:
            num = ""
            continue
        extn = old[i-1].rpartition(os.extsep)[2]
        num = "%02i"%i+"-"+"%02i"%(i+1) if new[i] == '#' else "%02i"%i
        tmp_n = formato("%02i"%season, num, new[i-1], extn)
        nu_list.append((old[i-1],tmp_n))
    return nu_list

def print_changes(pair):
    for o, n in pair:
        print("<<< {0}\n>>> {1}".format(o, n))

def doit(path, pair):
    for orig, dest in pair:
        os.rename(os.sep.join((path,orig)),os.sep.join((path,dest)))

def parsedir(dir_content):
    sub = []
    old = []

    if ".srt" in " ".join(dir_content):
        for i in range(1, len(dir_content)+1, 2):
            old.append(dir_content[i-1])
            sub.append(dir_content[i])
    else:
        old = dir_content
    return sub, old

opts = interact(parsecli(sys.argv))
sub, old = parsedir(listdir(opts["pth"]))
with open(opts["ep"],'r') as arq:
    names = arq.read()
new = names.split("\n")
if len(sub) != 0:
    opts["sub"] = True
    subs = reformat(sub, new, opts["ssn"], len(new))
eps = reformat(old, new, opts["ssn"], len(new))

if opts["conf"]:
    print_changes(eps)
    ans = input("Are you ready? [Y/n]: ")
    if ans in ["N","n"]:
        print("Whenever you fell safe, brother!")
        exit(1)
doit(opts["pth"], eps)
if opts["sub"]:
    doit(opts["pth"], subs)
print("Done!")
exit(0)
