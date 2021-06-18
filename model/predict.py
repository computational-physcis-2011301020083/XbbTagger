import argparse
import os,glob,h5py,ROOT,shutil
parser = argparse.ArgumentParser(description="%prog [options]", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--path", dest='path',  default="", help="path")
parser.add_argument("--model", dest='model',  default="", help="model")
args = parser.parse_args()
import tensorflow as tf
from keras import backend as K
import keras
from keras.models import Model, Sequential
from keras.layers import Dense, Input, Dropout, Activation
from keras.layers.normalization import BatchNormalization
from keras.optimizers import SGD,Adam
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score

#Features
features1=['mcEventWeight','eventNumber','mass','pt','eta'] #0-9
features2=['DL1rT_pu', 'DL1rT_pc', 'DL1rT_pb', 'relativeDeltaRToVRJet']
list3={}
list4={}
list5={}
for i in features2:
      list3[i]=i+"_1"
      list4[i]=i+"_2"
      list5[i]=i+"_3"

#Flatten
paths=args.path
h0=pd.read_hdf(paths,"fat_jet")[features1]
h1=pd.read_hdf(paths,"subjet_VRGhostTag_1")[features2]
h1.rename(columns=list3,inplace=True)
h2=pd.read_hdf(paths,"subjet_VRGhostTag_2")[features2]
h2.rename(columns=list4,inplace=True)
h3=pd.read_hdf(paths,"subjet_VRGhostTag_3")[features2]
h3.rename(columns=list5,inplace=True)
h=pd.concat([h0,h1,h2,h3], axis=1)
h["dsid"]=int(paths.split(".")[2])
h["pt"] = (h["pt"]/1000.0).astype("float64")
h["mass"] = (h["mass"]/1000.0).astype("float64")
Data=h[['mcEventWeight','relativeDeltaRToVRJet_1','relativeDeltaRToVRJet_2','relativeDeltaRToVRJet_3','eventNumber','dsid','mass','pt','eta','DL1rT_pu_1', 'DL1rT_pc_1', 'DL1rT_pb_1','DL1rT_pu_2', 'DL1rT_pc_2', 'DL1rT_pb_2','DL1rT_pu_3', 'DL1rT_pc_3', 'DL1rT_pb_3']]
Data=Data.values

#Processing
#Pt cut
Data=Data[Data[:,7]<3000.]
#Overlapping removal
Data=Data[(Data[:,1]>1.) | (Data[:,2]>1.) | (Data[:,3]>1.)]
for i in range(Data.shape[0]):
    if Data[i,1]<1.:                                                                                                            Data[i,9:12]=np.nan
    if Data[i,2]<1.:                                                                                                            Data[i,12:15]=np.nan
    if Data[i,3]<1.:                                                                                                            Data[i,15:18]=np.nan
#DL1rBaseline
f=0.018
DL1r_baseline=np.stack([Data[:,11:12]/((1-f)*Data[:,9:10]+f*Data[:,10:11]), Data[:,14:15]/((1-f)*Data[:,12:13]+f*Data[:,13:14])], axis=1).min(axis=1)
invalid = np.isnan(DL1r_baseline) | np.isinf(DL1r_baseline)
DL1r_baseline[invalid] = 1e-15
DL1rBaseline=np.log(np.clip(DL1r_baseline, 1e-30, 1e30))
#print DL1rBaseline.shape,DL1rBaseline[100:140,:]

#binned_dl1r
DL1rDisc1=Data[:,11:12]/((1-f)*Data[:,9:10]+f*Data[:,10:11])
DL1rDisc2=Data[:,14:15]/((1-f)*Data[:,12:13]+f*Data[:,13:14])
DL1rDisc3=Data[:,17:18]/((1-f)*Data[:,15:16]+f*Data[:,16:17])
DL1rDisc=np.hstack((DL1rDisc1,DL1rDisc2,DL1rDisc3))
#print DL1rDisc.shape,DL1rDisc[100:140,:]
DL1rDisc[np.isnan(DL1rDisc) | np.isinf(DL1rDisc)]=np.nan
#print DL1rDisc.shape,DL1rDisc[100:140,:]
for i in range(DL1rDisc.shape[0]):
    for j in range(DL1rDisc.shape[1]):
        if DL1rDisc[i,j]>4.805:
            DL1rDisc[i,j]=5
        elif DL1rDisc[i,j]>3.515:
            DL1rDisc[i,j]=4
        elif DL1rDisc[i,j]>2.585:
            DL1rDisc[i,j]=3
        elif DL1rDisc[i,j]>1.085:
            DL1rDisc[i,j]=2
        elif DL1rDisc[i,j]<=1.085:
            DL1rDisc[i,j]=1
#print DL1rDisc.shape,DL1rDisc[100:140,:]

#Scaling
info=np.hstack((Data[:,0:9],DL1rBaseline))
train=np.hstack((Data[:,7:18],DL1rDisc))
meanFile=h5py.File("meanstd.h5","r")
mean_vector=meanFile.get("mean")
std_vector=meanFile.get("std")
train=(train-mean_vector)/std_vector
train=np.nan_to_num(train)

#Predict
JKDL1r="WeiAdmStd_JKDL1r.h5"
PC_JKDL1r="WeiAdmStd_PC_JKDL1r.h5"
JKDL1r_pre = keras.models.load_model(JKDL1r)
PC_JKDL1r_pre = keras.models.load_model(PC_JKDL1r)

JK_data=train[:,0:2]
DL1r_data=train[:,2:11]
PCDL1r_data=train[:,11:14]

fatjet=JK_data # 'pt','eta'
subjet0_JK=DL1r_data[:,0:3] # 'DL1rT_pu_1', 'DL1rT_pc_1', 'DL1rT_pb_1'
subjet1_JK=DL1r_data[:,3:6] # 'DL1rT_pu_2', 'DL1rT_pc_2', 'DL1rT_pb_2'
subjet2_JK=DL1r_data[:,6:9] # 'DL1rT_pu_3', 'DL1rT_pc_3', 'DL1rT_pb_3'
subjet0_PC=PCDL1r_data[:,0:1] # 'binned_dl1rT_1'
subjet1_PC=PCDL1r_data[:,1:2] # 'binned_dl1rT_2'
subjet2_PC=PCDL1r_data[:,2:3] # 'binned_dl1rT_3'

JKDL1r_data=[fatjet,subjet0_JK,subjet1_JK,subjet2_JK]
PC_JKDL1r_data=[fatjet,subjet0_PC,subjet1_PC,subjet2_PC]

predictions_PC_JKDL1r=PC_JKDL1r_pre.predict(PC_JKDL1r_data)
predictions_JKDL1r=JKDL1r_pre.predict(JKDL1r_data)
#print predictions_PC_JKDL1r[110:130,:]
#print predictions_JKDL1r[110:130,:]


prediction_file="files/Prediction_"+args.path.split("/")[-1]
save_f = h5py.File(prediction_file, 'w')
predict=np.hstack((info,predictions_JKDL1r,predictions_PC_JKDL1r)) 
save_f.create_dataset("predict",data=predict)
print "Done"
print "Prediction files for study using testing samples, they are in order:"
print " ['mcEventWeight','relativeDeltaRToVRJet_1','relativeDeltaRToVRJet_2','relativeDeltaRToVRJet_3','eventNumber','dsid','mass','pt','eta', 'DL1rBaseline', 'JKDL1r_QCD','JKDL1r_Higgs','JKDL1r_Top','PC_JKDL1r_QCD','PC_JKDL1r_Higgs','PC_JKDL1r_Top' "







