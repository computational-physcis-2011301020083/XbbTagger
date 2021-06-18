import matplotlib
matplotlib.use('agg')
import numpy as np
import glob
import matplotlib.pyplot as plt


logpath=sorted(glob.glob("../model_opt_PCJKDL1rOR/*PC_JKDL1r_Valloss.log"))
logpath.append("../model_multiInput/WeiAdmStd_PC_JKDL1r.log")
print logpath

lossfile=open(logpath[0],"r")
print logpath[0]
epoch=[]
train_loss=[]
valid_loss=[]
j=0
for line in lossfile:
  j=j+1
  if j>=2:
    Str=line.split(",")
    epoch.append(int(Str[0]))
    train_loss.append(float(Str[1]))
    valid_loss.append(float(Str[2]))
train0=np.asarray(train_loss)
valid0=np.asarray(valid_loss)
epochs0=np.asarray(epoch)

lossfile=open(logpath[1],"r")
print logpath[1]
epoch=[]
train_loss=[]
valid_loss=[]
j=0
for line in lossfile:
  j=j+1
  if j>=2:
    Str=line.split(",")
    epoch.append(int(Str[0]))
    train_loss.append(float(Str[1]))
    valid_loss.append(float(Str[2]))
train1=np.asarray(train_loss)
valid1=np.asarray(valid_loss)
epochs1=np.asarray(epoch)




plt.figure(1)

plt.plot(epochs0,train0,label="PC_JKDL1r(OPT)_Training")
plt.plot(epochs0,valid0,label="PC_JKDL1r(OPT)_Validation")
plt.plot(epochs1,train1,label="PC_JKDL1r(Nominal)_Training")
plt.plot(epochs1,valid1,label="PC_JKDL1r(Nominal)_Validation")


plt.xlabel('Epoch')
plt.ylabel('Loss')
#plt.yscale("log", nonposy="clip")
#plt.xlim(right=280)
plt.ylim(top=0.65)
plt.legend(loc='upper right', fontsize="medium")
plt.text(50,0.64*1.002,r'$\sqrt{s}$=13TeV')
plt.text(50,0.64,r'Xbb tagging')
name="figures/LossPC.pdf"
plt.savefig(name)
name1=name.replace("pdf","png")
name2=name.replace("pdf","eps")
plt.savefig(name1)
plt.savefig(name2)
plt.show()
