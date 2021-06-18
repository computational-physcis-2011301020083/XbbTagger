import glob,math,os,h5py

import argparse,math,os
parser = argparse.ArgumentParser(description="%prog [options]", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--path", dest='path',  default="", help="path")
parser.add_argument("--outname", dest='outname',  default="", help="outname")
args = parser.parse_args()
path1=args.path

f=h5py.File(path1)
data=f.get("std")
#data=f.get('mean')

print(data.shape)
print(data[:,:])

