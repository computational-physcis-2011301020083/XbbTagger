import matplotlib
matplotlib.use('pdf')
import math,os,glob,h5py
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score
#import pandas as pd

path="./Reduced/tot.h5"
load_file=h5py.File(path,'r')
predict=load_file.get("data")
print predict.shape
predict=np.reshape(predict,(predict.shape[0],predict.shape[1]))
predict=predict[predict[:,11]==0]

y=predict[:,10]
w=predict[:,0]

JKDL1rScoreHiggs=predict[:,7]
JKDL1rScoreTop=predict[:,8]
JKDL1rScoreQCD=predict[:,6]
JKDL1r=np.true_divide(JKDL1rScoreHiggs,JKDL1rScoreQCD)
#JKDL1r=np.true_divide(JKDL1rScoreHiggs,(JKDL1rScoreQCD+JKDL1rScoreTop))
JKDL1r=np.nan_to_num(JKDL1r)
JKDL1r_bkg,JKDL1r_signal,JKDL1r_thres=roc_curve(y,JKDL1r,sample_weight=w)
AUC_JKDL1r=roc_auc_score(y, JKDL1r,sample_weight=w)




plt.plot(JKDL1r_signal,np.power(JKDL1r_bkg,-1.0),label="JKDL1r_Higgs/JKDL1r_QCD "+"AUC: "+str(AUC_JKDL1r)[0:6])
#plt.plot(Xbb_signal,np.power(Xbb_bkg,-1.0),label="Xbb_Higgs/Xbb_QCD "+"AUC: "+str(AUC_Xbb)[0:6])

plt.xlabel('Signal Efficiency')
plt.ylabel('Background Rejection')
plt.yscale("log", nonposy="clip")
plt.xlim(left=0.2)
plt.ylim(top=1e3*2)
#plt.ylim(bottom=0)
plt.legend(loc='best')
plt.text(0.3,1.5e1*0.4,r'$\sqrt{s}$=13TeV')
plt.text(0.3,1.5e1*0.2,r'Hbb vs. Dijets')
#plt.text(0.3,1.5e1*0.2,r'Hbb vs. Top')
ROC_file="figures/"+"Roc_CalibrationSample_QCD.pdf"
ROC_file1=ROC_file.replace("pdf","jpg")
#plt.savefig(ROC_file1)
plt.savefig(ROC_file)
plt.show()


