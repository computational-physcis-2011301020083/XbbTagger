import numpy as np
import pandas as pd
import glob,h5py
import argparse,math,os
parser = argparse.ArgumentParser(description="%prog [options]", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--path", dest='path',  default="", help="path")
args = parser.parse_args()

load_f = h5py.File(args.path, 'r')
outname=args.path.split("/")[-1]
save_f = h5py.File("../DataVRGhost/SplitData/"+outname, 'w')

Data=load_f.get("data")
N=Data.shape[0]
train_index=np.random.choice(N,4000000,replace=False) #Dijets
#train_index=np.random.choice(N,2000000,replace=False) #Hbb and Top
remain_index=np.setdiff1d(np.arange(0,N),train_index) 
valid_index=np.random.choice(remain_index,1000000,replace=False) #Dijets
#valid_index=np.random.choice(remain_index,500000,replace=False) #Hbb and Top
test_index=np.setdiff1d(remain_index,valid_index) 

case=["train","test","valid"]
index={"train":train_index,"test":test_index,"valid":valid_index}
for i in case:
	save_f.create_dataset(i,data=np.take(Data,index[i],axis=0))







