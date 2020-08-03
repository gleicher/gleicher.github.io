# tools to do chores with hugo page (irony - doing it in python)

import glob
import os.path
from collections import defaultdict
import shutil

# find all PDF files so we can deal with them...
# this makes them all external links
def findPDFs(root="content/talks", target="Talks",
             movebase="/p/graphics/public/htdocs/GleicherAssets"):
    flist = glob.glob(root+"/**/*.pdf")
    # switch from Window to Univ slashes
    flist = [i.replace("\\","/") for i in flist]

    # store what we did
    moves = []
    extpdfs = []

    # process each one...
    for path in flist:
        dir,pdf = os.path.split(path)
        ignore, dirname = os.path.split(dir)
        #
        # make a new file name
        year,month,fname = dirname.split("_",2)
        newname = "{}_{}_{}".format(year,month,pdf)
        newpath = movebase + "/" + target + "/" + newname
        moves.append( (path, newpath) )

        # now, transform the hugo file
        hf = dir + "/index.md"
        with open(hf) as fi:
            lines = fi.readlines()
        if lines.count("---\n") !=2:
            raise ValueError("{} doesn't have two header breaks!".format(hf))
        # find the last "---"
        last = max([loc for loc,val in enumerate(lines) if val=="---\n"])
        # check to see if it already has an extpdfs
        for li in lines:
            if li[:6] == "extpdf":
                print("!!!! Warning {} has an extpdfs already!".format(hf))
        # stick in a new extpdfs
        eline = 'extpdfs: ["{}/{}"]\n'.format(target, newname)
        lines.insert(last,eline)
        # write
        with open(hf,"w") as fo:
            fo.writelines(lines)

    with open("moves.sh","w") as fo:
        for m in moves:
            fo.write("mv {} {}\n".format(m[0],m[1]))

def delPDFs(root="content/talks"):
    flist = glob.glob(root+"/**/*.pdf")
    # switch from Window to Univ slashes
    flist = [i.replace("\\","/") for i in flist]

    for file in flist:
        print(file)
        os.remove(file)

def moveMovies(root="content/video",target="Videos"):
    flist = glob.glob(root+"/**/*.mp4") + glob.glob(root+"/**/*.avi")
    flist = [i.replace("\\","/") for i in flist]

    moves = []
    dirs = defaultdict(list)

    # process each one...
    for path in flist:
        dir,movie = os.path.split(path)
        ignore, dirname = os.path.split(dir)
        #
        # make a new file name
        year = dirname[:4]
        mname = movie.replace(" ","_").replace("(","").replace(")","")

        newname = mname if mname[0].isdigit() else "{}_{}".format(year,mname)
        newpath = target + "/" + newname
        moves.append( (path, newpath) )
        dirs[dir].append(newpath)

    for d in dirs:
        print(d,"-->",dirs[d])

        # now, transform the hugo file
        hf = d + "/index.md"
        with open(hf) as fi:
            lines = fi.readlines()
        if lines.count("---\n") !=2:
            raise ValueError("{} doesn't have two header breaks!".format(hf))
        # find the last "---"
        last = max([loc for loc,val in enumerate(lines) if val=="---\n"])
        # check to see if it already has an extpdfs
        for li in lines:
            if li[:6] == "extpdf":
                print("!!!! Warning {} has an extpdfs already!".format(hf))
        # stick in a new extpdfs
        eline = 'extvideos: {}\n'.format(dirs[d])
        eline = eline.replace("'",'"')
        lines.insert(last,eline)
        # print(eline)
        # write
        with open(hf,"w") as fo:
            fo.writelines(lines)

    for m in moves:
        shutil.move(m[0],m[1])

# in videos I screwed up and made it pdfs, not videos
def fixvideos(root="content/video"):
    flist = glob.glob(root+"/**/index.md")

    for f in flist:
        with open(f) as fi:
            lines = fi.readlines()
        print("{} has {} lines".format(f,len(lines)))
        with open(f,"w") as fo:
           for l in lines:
               fo.write(l.replace("extpdfs","extvideos"))
