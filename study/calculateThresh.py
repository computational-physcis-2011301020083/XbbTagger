#Calculate the threshold corresponding to a certain signal efficiency
#wei.ding@cern.ch

import math,os,glob,h5py
import numpy as np
from scipy.stats import entropy
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score
import argparse
parser = argparse.ArgumentParser(description="%prog [options]", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--path", dest='path',  default="", help="path")
args = parser.parse_args()

filepath=args.path
load_file=h5py.File(filepath,'r')
predict=load_file.get("predict")
predict=np.reshape(predict,(predict.shape[0],predict.shape[1]))
#predict=predict[predict[:,2]==0] #Hbb vs. Dijets
predict=predict[predict[:,0]==0] #Hbb vs. Top

y=predict[:,1]
score=predict[:,4]
Xbb=predict[:,8]
w=predict[:,6]
eff_bkg,eff_signal,thres=roc_curve(y,score,sample_weight=w) #New_score
#eff_bkg,eff_signal,thres=roc_curve(y,Xbb,sample_weight=w) #XbbScore

info=np.column_stack((1.0/eff_bkg,eff_signal,thres))
efflist=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.75,0.8,0.85,0.9,0.95]
count=0
for a in efflist:
    count=count+1
    if count==1:
        info1=info[abs(info[:,1]-a)==abs(info[:,1]-a).min()][0,:]
    if count!=1:
        info1=np.vstack((info1,info[abs(info[:,1]-a)==abs(info[:,1]-a).min()][0,:]))
save_f = h5py.File("effInfo.h5", 'w')
save_f.create_dataset("data",data=info1)

print "They are in order bkg_rejection, signal_efficiency, threshold"
print info1
