# this is a program for generating a folder structure ready for copying
# photos etc. from a camera to a computer
# it will create the folder for the year wherever this module is run from
# generate folders for all months and days in the current year
# the user should later remove folders that are not used

import datetime
import os
# flag to change whether to generate the subfolders for processed images
createProc = True

now = datetime.date.today()
thisyear =  now.year

# the month names in Cornish
monthnames = ["Genver",
              "Hwevrer",
              "Meurth",
              "Ebrel",
              "Me",
              "Metheven",
              "Gortheren",
              "Est",
              "Gwynngala",
              "Hedra",
              "Du",
              "Kevardhu"]

monthnames = ["mis-"+m for m in monthnames]

# prefix the numerical index of the month, with a leading zero where needed
monthnames = ["{n:02d}_{m}".format(n=x[0]+1,m=x[1]) for x in enumerate(monthnames)]

if os.path.exists(str(thisyear)):
    print("year folder for {y} already exists. ending program".format(y=thisyear))
else:
    # create and enter the year folder
    os.mkdir(str(thisyear))
    os.chdir(str(thisyear))
    # loop through the months
    for i,m in enumerate(monthnames):
        # set the date to the first of the month
        currdate = datetime.date(thisyear,i+1,1)
        # create and enter the month folder
        print("creating folder: {m}".format(m=m))
        os.mkdir(m)
        os.chdir(m)
        while currdate.month == i+1:
            # create the day folder, as long as we're still in the same month
            print("creating folder: {d:02d}".format(d=currdate.day))
            os.mkdir("{d:02d}".format(d=currdate.day))
            # if the flag is True, enter the day folder
            # and generate the subfolders for processed images
            if createProc:
                os.chdir("{d:02d}".format(d=currdate.day))
                print("generating subfolders for processed images")
                os.mkdir("argerdhys")
                os.chdir("argerdhys")
                os.mkdir("1440px")
                # go back up to month folder
                os.chdir("../..")
            currdate = currdate + datetime.timedelta(days=1)
        # go back up to year folder
        os.chdir("..")
            
            
            


