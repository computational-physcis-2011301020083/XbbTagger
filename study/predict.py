import argparse
import os,glob,h5py,ROOT,shutil
parser = argparse.ArgumentParser(description="%prog [options]", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--path", dest='path',  default="", help="path")
args = parser.parse_args()
import tensorflow as tf
from keras import backend as K
import keras
from keras.models import Model, Sequential
from keras.layers import Dense, Input, Dropout, Activation
from keras.layers.normalization import BatchNormalization
from keras.optimizers import SGD,Adam
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score

model_file=args.path
model_pre = keras.models.load_model(model_file)
load_file=h5py.File("../DataVRGhost/PrepareData/teststd.h5")
test=load_file.get("test")
data=test[:,9:83] 
y=test[:,0:3]
w=test[:,3:9]
predictions = model_pre.predict(data)
prediction_file="prediction_"+model_file.split("/")[-1]
save_f = h5py.File("./"+prediction_file, 'w')
predict=np.hstack((y,predictions,w))
save_f.create_dataset("predict",data=predict)
print "Prediction files for study using testing samples, they are in order:"
print "is_Dijets, is_Hbb, is_Top, Prediction_ScoreQCD, Prediction_ScoreHiggs, Prediction_ScoreTop, weight, XbbScoreQCD, XbbScoreHiggs, XbbScoreTop, mass[GeV], pt[GeV]"



