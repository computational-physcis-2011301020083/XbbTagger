import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, roc_auc_score
import math,os,glob,h5py
import argparse
parser = argparse.ArgumentParser(description="%prog [options]", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--bins", dest='bins',  default="", help="bins")
parser.add_argument("--neights", dest='neights',  default="", help="neights")
args = parser.parse_args()

#Load samples
filepath="../DataVRGhost/PrepareData/trainstd1.h5"
f=h5py.File(filepath,'r')
data=f.get("train")
#data=f.get("valid")
data=np.reshape(data,(data.shape[0],data.shape[1]))
#data=data[data[:,0]==1] #Dijets
#data=data[data[:,1]==1] #Hbb
data=data[data[:,2]==1] #Top
pt=data[:,8]
weight=data[:,3]

#Reweight to flat pt
from hep_ml.reweight import BinsReweighter
original = pt
xmin, xmax = original.min(), original.max()
target = np.random.rand(original.size) * (xmax - xmin) + xmin
bins=500
neights=1
reweighter = BinsReweighter(n_bins=bins, n_neighs=neights)
reweighter.fit(original, target=target)
weight1 = reweighter.predict_weights(original)

#Weight for training samples
weight1=weight1*4000000/np.sum(weight1)
#weight1=weight1*2000000/np.sum(weight1)

#Weight for validation samples
#weight1=weight1*1000000/np.sum(weight1)
#weight1=weight1*500000/np.sum(weight1)

new_hdf5 = h5py.File("weight.h5", 'a')
new_hdf5.create_dataset("trainDijets",data=weight1)
#new_hdf5.create_dataset("trainHbb",data=weight1)
#new_hdf5.create_dataset("trainTop",data=weight1)

#new_hdf5.create_dataset("validDijets",data=weight1)
#new_hdf5.create_dataset("validHbb",data=weight1)
#new_hdf5.create_dataset("validTop",data=weight1)

#Check pt distribution
weight2=np.full((data.shape[0], ), 1)
Bins = np.linspace(0, 7000, 200)
plt.figure(1)
plt.hist(pt,weights=weight1,bins=Bins,label=" ",histtype="step")
plt.yscale("log", nonposy="clip")
plt.xlabel('pt [GeV]')
plt.ylabel('Events')
#plt.savefig("DijetsPtCheck.pdf")
plt.show()


