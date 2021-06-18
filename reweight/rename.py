import os,shutil

listfile="list.txt"
f=open(listfile,"r")
items=f.readlines()
#print(items)
#for i in items:
#  i=i.rstrip('\n')  

Top_DSID=['301322', '301323', '301324', '301325', '301326', '301327', '301328', '301329', '301330', '301331', '301332', '301333', '301334', '301335']
Hbb_DSID=['301488', '301489', '301490', '301491', '301492', '301493', '301494', '301495', '301496', '301497', '301498', '301499', '301500', '301501', '301502', '301503', '301504', '301505', '301506', '301507', '305776', '305777', '305778', '305779', '305780', '309450']

count=0
for i in items:
    j=i.rstrip('\n')
    count=count +1
    print count
    if j.split(".")[2] in Top_DSID:
        for k in os.listdir(j):
            name=j+k 
            rename=name.replace("_s3126_r9364_p4258.2020_ftag5dev.v1_output.h5/user.dguest.",".") #.replace(".h5/user.dguest.",".")
            rename="Top/"+rename
            print name,rename
            shutil.copy(name,rename)
    elif j.split(".")[2] in Hbb_DSID:
        for k in os.listdir(j):
            name=j+k
            rename=name.replace("_s3126_r9364_p4258.2020_ftag5dev.v1_output.h5/user.dguest.",".") #.replace(".h5/user.dguest.",".")
            rename="Hbb/"+rename
            print name,rename
            shutil.copy(name,rename)
    else:
        print "error"






