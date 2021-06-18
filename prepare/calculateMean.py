import numpy as np
import pandas as pd
import glob,h5py
import argparse,math,os
parser = argparse.ArgumentParser(description="%prog [options]", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--path", dest='path',  default="", help="path")
args = parser.parse_args()

filepath=args.path
f=h5py.File(filepath,"r")
train=f.get("train")
Info=train[:,0:9]
training=train[:,8:82]
mean_vector = np.nanmean(training, axis=0)
std_vector = np.nanstd(training, axis=0)
mean_vector=np.reshape(mean_vector,(1,mean_vector.shape[0]))
std_vector=np.reshape(std_vector,(1,std_vector.shape[0]))

save_f = h5py.File("../DataVRGhost/PrepareData/meanstd.h5", 'w')
save_f.create_dataset("mean",data=mean_vector)
save_f.create_dataset("std",data=std_vector)









