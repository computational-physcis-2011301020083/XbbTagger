import pandas as pd
import glob,math,os,h5py

import argparse,math,os
parser = argparse.ArgumentParser(description="%prog [options]", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--path", dest='path',  default="", help="path")
parser.add_argument("--outname", dest='outname',  default="", help="outname")
args = parser.parse_args()
path1=args.path

#f=h5py.File(path1)
#data=f.get('train')
#data=f.get('predict')
#data=f.get('test')
#data=f.get('data')
#print data.shape

#print f["metadata"]["nEventsProcessed"].shape


#h1=pd.read_hdf(path1)
#h1=pd.read_hdf(path1,"subjet_VRGhostTag_1")
h1=pd.read_hdf(path1,"fat_jet")
#h1=pd.read_hdf(path1,"metadata")
#print list(h1.keys())
print h1.keys
for i in h1.keys():
    print i

