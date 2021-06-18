import os


listfile="list.txt"
f=open(listfile,"r")
items=f.readlines()
#print(items)
for i in items:
  i=i.rstrip('\n')  
  command="rucio download "+i
  print(command)
  os.system(command)


