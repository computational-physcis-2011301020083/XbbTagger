import math,os,glob,h5py
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import roc_curve, roc_auc_score
import argparse
parser = argparse.ArgumentParser(description="%prog [options]", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--path", dest='path',  default="", help="path")
args = parser.parse_args()

#Load prediction file
filepath=args.path
load_file=h5py.File(filepath,'r')
predict=load_file.get("predict")
predict=np.reshape(predict,(predict.shape[0],predict.shape[1]))

#predict=predict[predict[:,2]==0] #Hbb vs. Dijets
predict=predict[predict[:,0]==0] #Hbb vs. Top

#Extract info like true value XbbScore and New_Score from model
y=predict[:,1]
scoreHiggs=predict[:,4]
#scoreQCD=predict[:,3]
scoreTop=predict[:,5]
#score=np.true_divide(scoreHiggs,scoreQCD)
score=np.true_divide(scoreHiggs,scoreTop)
score=np.nan_to_num(score)
XbbHiggs=predict[:,8]
#XbbQCD=predict[:,7]
XbbTop=predict[:,9]
#Xbb=np.true_divide(XbbHiggs,XbbQCD)
Xbb=np.true_divide(XbbHiggs,XbbTop)
Xbb=np.nan_to_num(Xbb)
w=predict[:,6]

#Plot ROC 
eff_bkg,eff_signal,thres=roc_curve(y,score,sample_weight=w)
eff_bkg1,eff_signal1,thres1=roc_curve(y,Xbb,sample_weight=w)
AUCNew=roc_auc_score(y, score)
AUCXbb=roc_auc_score(y, Xbb)
plt.figure(1)
#plt.plot(eff_signal,np.power(eff_bkg,-1.0),label="New_HiggsScore/New_QCDScore "+"AUC: "+str(AUCNew)[0:6])
#plt.plot(eff_signal1,np.power(eff_bkg1,-1.0),label="XbbScoreHiggs/XbbScoreQCD "+"AUC: "+str(AUCXbb)[0:6])
plt.plot(eff_signal,np.power(eff_bkg,-1.0),label="New_HiggsScore/New_TopScore "+"AUC: "+str(AUCNew)[0:6])
plt.plot(eff_signal1,np.power(eff_bkg1,-1.0),label="XbbScoreHiggs/XbbScoreTop "+"AUC: "+str(AUCXbb)[0:6])
plt.xlabel('Signal Efficiency')
plt.ylabel('Background Rejection')
plt.yscale("log", nonposy="clip")
plt.xlim(left=0.2)
plt.ylim(top=1e5)
plt.legend(loc='best')
plt.text(0.7,1e4*0.4,r'$\sqrt{s}$=13TeV')
#plt.text(0.7,1e4*0.2,r'Hbb vs. Dijets')
plt.text(0.7,1e4*0.2,r'Hbb vs. Top')
#plt.text(0.7,1e4*0.1,r'pt:[250,1000]GeV')
#plt.text(0.7,1e4*0.1,r'pt:[1000,~]GeV')
#plt.text(0.7,1e4*0.1,r'Loose mass selection')
#plt.text(0.7,1e3*0.5,r'Loose mass selection')
plt.text(0.7,1e4*0.1,r'No mass selection')
#plt.text(0.7,1e3*0.5,r'No mass selection')
ROC_file="figures/"+"RocRatio_Opt1_TopMassPt.pdf"
#ROC_file="figures/"+"RocRatio_Opt1_DijetsMass1Pt1.pdf"
plt.savefig(ROC_file)




