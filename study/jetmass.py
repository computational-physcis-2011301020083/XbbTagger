import math,os,glob,h5py
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import roc_curve, roc_auc_score
import argparse
parser = argparse.ArgumentParser(description="%prog [options]", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--path", dest='path',  default="", help="path")
parser.add_argument("--eff", dest='eff',  default="", help="eff")
parser.add_argument("--thresh", dest='thresh',  default="", help="thresh")
args = parser.parse_args()

filepath=args.path
load_file=h5py.File(filepath,'r')
predict=load_file.get("predict")
predict=np.reshape(predict,(predict.shape[0],predict.shape[1]))

predict=predict[predict[:,0]==1] #Dijets
#predict=predict[predict[:,2]==1] #Top
predict=predict[(predict[:,10]<=300.) & (predict[:,10]>=50.)]

thresh=float(args.thresh)
#New_Score
predict1=predict[predict[:,4]>=thresh]
predict2=predict[predict[:,4]<=thresh]
#XbbScore
#predict1=predict[predict[:,8]>=thresh]
#predict2=predict[predict[:,8]<=thresh]

bins = np.linspace(50, 300, 100)
plt.figure(1)
str1="Signal eff: "+args.eff
plt.hist(predict1[:,10],weights=predict1[:,6]/np.sum(predict1[:,6]),bins=bins,label="New_ScoreHiggs Pass, "+str1,histtype="step")
plt.hist(predict2[:,10],weights=predict2[:,6]/np.sum(predict2[:,6]),bins=bins,label="New_ScoreHiggs Fail",histtype="step")
plt.legend(loc='upper right', fontsize="x-small")
plt.yscale("log", nonposy="clip")
plt.xlabel("mass [GeV]")
plt.ylabel("Events fraction")
plt.ylim(top=0.1)
Jetmass_file="figures/"+"Jetmass_Opt1_DijetsEff0p2.pdf"
plt.savefig(Jetmass_file)
plt.show()




