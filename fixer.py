# tools to do chores with hugo page (irony - doing it in python)

import glob
import os.path

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