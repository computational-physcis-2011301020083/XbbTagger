import numpy as np
import pandas as pd
import glob,h5py
import argparse,math,os
parser = argparse.ArgumentParser(description="%prog [options]", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--path", dest='path',  default="", help="path")
args = parser.parse_args()

filepath=args.path
f=h5py.File(filepath,"r")
train=f.get("train") #Scaling training samples
#train=f.get("valid") #Scaling validation samples
#train=f.get("test") #Scaling testing samples
Info=train[:,0:9]
training=train[:,8:82]

Mean="../DataVRGhost/PrepareData/meanstd.h5"
meanFile=h5py.File(Mean,"r")
mean_vector=meanFile.get("mean")
std_vector=meanFile.get("std")
training=(training-mean_vector)/std_vector
NewTrain=np.hstack((Info,training))
NewTrain=np.nan_to_num(NewTrain)

save_f = h5py.File("../DataVRGhost/PrepareData/trainstd.h5", 'a')
#save_f = h5py.File("../DataVRGhost/PrepareData/teststd.h5", 'a')
save_f.create_dataset("train",data=NewTrain)
#save_f.create_dataset("valid",data=NewTrain)
#save_f.create_dataset("test",data=NewTrain)


