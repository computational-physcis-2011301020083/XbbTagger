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

#Read in the dataset
features1=['mcEventWeight','eventNumber','mass','pt','eta','GhostHBosonsCount','GhostTQuarksFinalCount'] #0-9
features2=['DL1r_pu', 'DL1r_pc', 'DL1r_pb', 'relativeDeltaRToVRJet']
Xbbv12=['Xbb202006_QCD','Xbb202006_Higgs','Xbb202006_Top','Xbb2020v2_QCD','Xbb2020v2_Higgs','Xbb2020v2_Top']
list3={}
list4={}
list5={}
for i in features2:
      list3[i]=i+"_1"
      list4[i]=i+"_2"
      list5[i]=i+"_3"
paths=args.path
hXbbv12=pd.read_hdf(paths,"fat_jet")[Xbbv12]
h0=pd.read_hdf(paths,"fat_jet")[features1]
h1=pd.read_hdf(paths,"subjet_VRGhostTag_1")[features2]
h1.rename(columns=list3,inplace=True)
h2=pd.read_hdf(paths,"subjet_VRGhostTag_2")[features2]
h2.rename(columns=list4,inplace=True)
h3=pd.read_hdf(paths,"subjet_VRGhostTag_3")[features2]
h3.rename(columns=list5,inplace=True)
h=pd.concat([hXbbv12,h0,h1,h2,h3], axis=1)
h["dsid"]=int(paths.split(".")[4])
h["pt"] = (h["pt"]/1000.0).astype("float64")
h["mass"] = (h["mass"]/1000.0).astype("float64")
h=h[h["pt"]<3000.]
h=h[h["eta"]<2.]
h=h[h["eta"]>-2.]
h=h[h["GhostHBosonsCount"]>=1.] #Hbb
#h=h[h["GhostTQuarksFinalCount"]>=1.] #Top
Data=h[['mcEventWeight','relativeDeltaRToVRJet_1','relativeDeltaRToVRJet_2','relativeDeltaRToVRJet_3','eventNumber','dsid','mass','pt','eta','DL1r_pu_1', 'DL1r_pc_1', 'DL1r_pb_1','DL1r_pu_2', 'DL1r_pc_2', 'DL1r_pb_2','DL1r_pu_3', 'DL1r_pc_3', 'DL1r_pb_3','Xbb202006_QCD','Xbb202006_Higgs','Xbb202006_Top','Xbb2020v2_QCD','Xbb2020v2_Higgs','Xbb2020v2_Top']]
Data=Data.values
#DataXbb=hXbbv12.values

#Normalize the data
#Data=Data[Data[:,7]<3000.]
#Data=Data[Data[:,8]<2.]
#Data=Data[Data[:,8]>-2.]

train=Data[:,7:18]
meanFile=h5py.File("meanstd.h5","r")
mean_vector=meanFile.get("mean")
std_vector=meanFile.get("std")
#print(mean_vector,std_vector)
train=(train-mean_vector[:,0:11])/std_vector[:,0:11]
train=np.nan_to_num(train)

#Feeds it to Keras to call predict
JKDL1r="WeiAdmStd_JKDL1r.h5"
JKDL1r_pre = keras.models.load_model(JKDL1r)
JKDL1r_data=train
predictions_JKDL1r=JKDL1r_pre.predict(JKDL1r_data)
print(Data[100:120,18:24],predictions_JKDL1r[100:120,:])
#print predictions_JKDL1r[110:130,:]



