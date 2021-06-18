import h5py
import talos as ta
from keras import *
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam,Adagrad,Adamax,SGD,Nadam
from keras.losses import categorical_crossentropy, logcosh
from keras.activations import relu, elu, softmax
from talos.model.normalizers import lr_normalizer
from talos.model.layers import hidden_layers


print "************ PHASE LOAD FILE *****************"
train_file=h5py.File("../Xbb0106A/trainstd.h5","r")
train=train_file.get("train")
valid=train_file.get("valid")

train_data1=train[:,14:16]
train_data2=train[:,16:25]
train_data=np.hstack((train_data1,train_data2))
train_y=train[:,0:3]
#train_w=train[:,3]
train_w=np.full((6000000, ), 1) #Equal weight

valid_data1=valid[:,14:16]
valid_data2=valid[:,16:25]
valid_data=np.hstack((valid_data1,valid_data2))
valid_y=valid[:,0:3]
#valid_w=valid[:,3]
valid_w=np.full((600000, ), 1) #Equal weight


print train_data.shape,train_y.shape


haper={'first_neuron':[50,120,250,500],'lr':[0.1,0.01,0.001],'hidden_layers':[4,6,8],'batch_size':[10000],'epochs':[200],'dropout':[0],'optimizer':[Adam],'losses':['categorical_crossentropy'],'activation':['relu'],'last_activation':['softmax'],'batchnorm':[True],'shuffle':[True],'decay':[0.001,0.0001,0.00001],'shapes':['brick']}


def hbb_model(train_data,train_y,valid_data,valid_y,param):
    model=Sequential()
    model.add(Dense(param['first_neuron'],input_dim=train_data.shape[1],activation=param['activation'],kernel_initializer='normal'))
    model.add(Dropout(param['dropout']))
    hidden_layers(model,param,1)
    model.add(Dense(train_y.shape[1],activation=param['last_activation'],kernel_initializer='normal'))
    model.compile(optimizer=param['optimizer'](lr=lr_normalizer(param['lr'],param['optimizer'])),loss=param['losses'],metrics=['acc'])

    out=model.fit(train_data,train_y,batch_size=param['batch_size'],epochs=param['epochs'],verbose=0,validation_data=[valid_data,valid_y])
    return out,model


h=ta.Scan(x=train_data,y=train_y,x_val=valid_data,y_val=valid_y,params=haper,dataset_name='Opt_JKDL1r',experiment_no='0',model=hbb_model,grid_downsample=1)











