import ROOT,h5py
import numpy as np
import argparse,math,os
parser = argparse.ArgumentParser(description="%prog [options]", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--path", dest='path',  default="", help="path")
args = parser.parse_args()

path=args.path
f=ROOT.TFile(path,"r")
t=f.Get("t")
a,b=t.AsMatrix(return_labels=True)
print a.shape,b
predict=a
predict=predict[(predict[:,3]<2500.) & (predict[:,3]>250.)]
predict=predict[(predict[:,4]<2.) & (predict[:,4]>-2.)]
print predict.shape

#DL1rBaseline pb/[(1-f)*pu+f*pc]
f=0.018
DL1r_baseline=np.stack([predict[:,12:13]/((1-f)*predict[:,11:12]+f*predict[:,13:14]), predict[:,15:16]/((1-f)*predict[:,14:15]+f*predict[:,16:17])], axis=1).min(axis=1)
invalid = np.isnan(DL1r_baseline) | np.isinf(DL1r_baseline)
DL1r_baseline[invalid] = 1e-15
DL1rBaseline=np.log(np.clip(DL1r_baseline, 1e-30, 1e30))
#print DL1rBaseline.shape,DL1rBaseline[100:140,:]
data=np.hstack((predict[:,0:11],DL1rBaseline))
print data.shape

new_file_name=path.split("/")[-1]
new_hdf5 = h5py.File("../Reduced/Convert/"+new_file_name, 'w')
new_hdf5.create_dataset("data",data=data)



