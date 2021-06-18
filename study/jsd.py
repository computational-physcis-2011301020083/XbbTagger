import root_numpy
import math,os,glob,h5py
import numpy as np
from scipy.stats import entropy
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import roc_curve, roc_auc_score
import ROOT
import rootplotting as rp
import argparse
parser = argparse.ArgumentParser(description="%prog [options]", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--path", dest='path',  default="", help="path")
parser.add_argument("--thresh", dest='thresh',  default="", help="thresh")
args = parser.parse_args()

cut=float(args.thresh)
filepath=args.path
load_file=h5py.File(filepath,'r')
predict=load_file.get("predict")
predict=np.reshape(predict,(predict.shape[0],predict.shape[1]))
predict=predict[predict[:,0]==1] #JSD study for Dijets
#predict=predict[predict[:,2]==1] #JSD study for Top
info=np.column_stack((predict[:,10],predict[:,6],predict[:,4])) #mass,weight,New_Score 
#info=np.column_stack((predict[:,10],predict[:,6],predict[:,8])) #mass,weight,XbbScore 
info1=info[info[:,2]>=cut]
info2=info[info[:,2]<cut]

bins = np.linspace(50, 300, 100)
c = rp.canvas()
h_pass = c.hist(info1[:,0], bins=bins, weights=info1[:,1], normalise=True)
h_fail = c.hist(info2[:,0], bins=bins, weights=info2[:,1], normalise=True)
P = root_numpy.hist2array(h_pass)
Q = root_numpy.hist2array(h_fail)
p = P / np.sum(P)
q = Q / np.sum(Q)
m = 0.5 * (p + q)
jsd=0.5 * (entropy(p, m, base=2) + entropy(q, m, base=2))
print jsd



