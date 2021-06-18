import math,os,glob,h5py
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score


#Hbb VS QCD
filepath="../Reduced/tot.h5"
print filepath
load_file=h5py.File(filepath,'r')

predict=load_file.get("data")
print predict.shape
predict=np.reshape(predict,(predict.shape[0],predict.shape[1]))
#predict=predict[predict[:,11]==1]
predict=predict[predict[:,9]==1]
eff=[]
mass=[]
cut=[4.03,3.63,3.05,2.34]
Eff=[0.5,0.6,0.7,0.8]
print len(cut)
for j in cut:
  for i in range(25):
    a=i*10+50
    b=i*10+60
    predictI=predict[(predict[:,3]<=b) & (predict[:,3]>=a)] 
    #print a,b,predictI.shape
    #w=predictI[:,0]
    w=np.full((predictI.shape[0], ), 1)
    y=predictI[:,2]
    JKDL1rScoreHiggs=predictI[:,7]
    JKDL1rScoreQCD=predictI[:,6]
    JKDL1rScoreTop=predictI[:,8]
    #Get loge
    JKDL1r=np.true_divide(JKDL1rScoreHiggs,JKDL1rScoreQCD)#+JKDL1rScoreTop)
    JKDL1r=np.log(np.nan_to_num(JKDL1r))
    #print predictI[:,3].shape,JKDL1r.shape
    info=np.column_stack((w,JKDL1r))
    c=j
    d=np.sum(info[info[:,1]>c][:,0])/np.sum(info[:,0])
    #print d
    eff.append(d)
    mass.append(a+5)
print len(eff),len(mass)
plt.figure(1)
plt.plot(mass[0:25],eff[0:25],label="Signal Efficiency 50%: ln(pH/pQCD)>4.03")
plt.plot(mass[25:50],eff[25:50],label="Signal Efficiency 60%: ln(pH/pQCD)>3.63")
plt.plot(mass[50:75],eff[50:75],label="Signal Efficiency 70%: ln(pH/pQCD)>3.05")
plt.plot(mass[75:100],eff[75:100],label="Signal Efficiency 80%: ln(pH/pQCD)>2.34")
#plt.plot(mass[100:125],eff[100:125],label="0.8")
plt.xlabel('Large-R jet mass [GeV]')
plt.ylabel('Background efficiency')
#plt.yscale("log", nonposy="clip")
#plt.xlim(left=0.3)
plt.ylim(top=0.2)
plt.ylim(bottom=0)
#plt.legend(loc='best')
plt.legend(loc='upper right')
plt.text(200,0.10,r'$\sqrt{s}$=13TeV')
plt.text(200,0.085,r'Hbb vs. QCD')
#plt.text(200,0.14,r'Hbb vs. Top')
ROC_file="figures/"+"EffVSQCD_JKDL1r(OR).pdf"
ROC_file1=ROC_file.replace("pdf","jpg")
plt.savefig(ROC_file1)
plt.savefig(ROC_file)
plt.show()   



#Hbb VS Top
filepath="../Reduced/tot.h5"
print filepath
load_file=h5py.File(filepath,'r')

predict=load_file.get("data")
print predict.shape
predict=np.reshape(predict,(predict.shape[0],predict.shape[1]))
predict=predict[predict[:,11]==1]
#predict=predict[predict[:,9]==1]
eff=[]
mass=[]
cut=[2.25,1.61,0.98,0.32]
Eff=[0.5,0.6,0.7,0.8]
print len(cut)
for j in cut:
  for i in range(25):
    a=i*10+50
    b=i*10+60
    predictI=predict[(predict[:,3]<=b) & (predict[:,3]>=a)] 
    #print a,b,predictI.shape
    #w=predictI[:,0]
    w=np.full((predictI.shape[0], ), 1)
    y=predictI[:,1]
    JKDL1rScoreHiggs=predictI[:,7]
    JKDL1rScoreQCD=predictI[:,6]
    JKDL1rScoreTop=predictI[:,8]
    JKDL1r=np.true_divide(JKDL1rScoreHiggs,JKDL1rScoreTop)#+JKDL1rScoreTop)
    JKDL1r=np.log(np.nan_to_num(JKDL1r))
    #print predictI[:,3].shape,JKDL1r.shape
    info=np.column_stack((w,JKDL1r))
    c=j
    d=np.sum(info[info[:,1]>=c][:,0])/np.sum(info[:,0])
    #print d
    eff.append(d)
    mass.append(a+5)
print len(eff),len(mass)
plt.figure(1)
plt.plot(mass[0:25],eff[0:25],label="Signal Efficiency 50%: ln(pH/pTop)>2.25")
plt.plot(mass[25:50],eff[25:50],label="Signal Efficiency 60%: ln(pH/pTop)>1.61")
plt.plot(mass[50:75],eff[50:75],label="Signal Efficiency 70%: ln(pH/pTop)>0.98")
plt.plot(mass[75:100],eff[75:100],label="Signal Efficiency 80%: ln(pH/pTop)>0.32")
plt.xlabel('Large-R jet mass [GeV]')
plt.ylabel('Background efficiency')
#plt.yscale("log", nonposy="clip")
#plt.xlim(left=0.3)
plt.ylim(top=0.4)
plt.ylim(bottom=0)
#plt.legend(loc='best')
plt.legend(loc='upper right')
plt.text(200,0.22,r'$\sqrt{s}$=13TeV')
#plt.text(200,0.14,r'Hbb vs. Dijets')
plt.text(200,0.18,r'Hbb vs. Top')
ROC_file="figures/"+"EffVSTOP_JKDL1r(OR).pdf"
ROC_file1=ROC_file.replace("pdf","jpg")
plt.savefig(ROC_file1)
plt.savefig(ROC_file)
plt.show()   
