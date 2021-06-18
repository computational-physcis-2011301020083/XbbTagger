import argparse
import os,glob,h5py,ROOT,shutil
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

print "************ PHASE LOAD FILE *****************"
weight_file=h5py.File("weight.h5","r")
train_Dijets=weight_file.get("trainDijets")
train_Hbb=weight_file.get("trainHbb")
train_Top=weight_file.get("trainTop")
valid_Dijets=weight_file.get("validDijets")
valid_Hbb=weight_file.get("validHbb")
valid_Top=weight_file.get("validTop")

train_file=h5py.File("../DataVRGhost/PrepareData/trainstd1.h5","r")
train=train_file.get("train")
valid=train_file.get("valid")
train_data=train[:,9:83]
train_y=train[:,0:3]
train_w=np.hstack((train_Dijets,train_Hbb,train_Top)) #Flat pt
#train_w=np.full((8000000, ), 1) #Equal weight
#train_w=train[:,3] #Nominal weight
valid_data=valid[:,9:83]
valid_y=valid[:,0:3]
valid_w=np.hstack((valid_Dijets,valid_Hbb,valid_Top)) #Flat pt
#valid_w=np.full((2000000, ), 1) #Equal weight
#valid_w=valid[:,3] #Nominal weight


def define_model(params):
    inputs=Input(shape=(74, ), name='WeiAdm3bStd1_Flatpt')
    concatenated_inputs =inputs
    for i in range(params['num_layers']):
        if i==0:
            x = Dense(params['num_units'], kernel_initializer='orthogonal')(concatenated_inputs)
            if params['batch_norm']:
               x = BatchNormalization()(x)
            x = Activation(params['activation_type'])(x)
            if params['dropout_strength'] > 0:
               x = Dropout(params['dropout_strength'])(x)
        else:
            x = Dense(params['num_units'], kernel_initializer='orthogonal')(x)
            if params['batch_norm']:
               x = BatchNormalization()(x)
            x = Activation(params['activation_type'])(x)
            if params['dropout_strength'] > 0:
               x = Dropout(params['dropout_strength'])(x)

    predictions = Dense(params['output_size'], activation='softmax', kernel_initializer='orthogonal')(x)
    model = Model(inputs=inputs, outputs=predictions)
    adm = Adam(lr=params['learning_rate'], decay=params['lr_decay'])
    #sgd = SGD(lr=params['learning_rate'], decay=params['lr_decay'], momentum=params['momentum'], nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=adm)
    return model

print "************ PHASE TRAINING *****************"
params = {'num_layers': 6,'num_units': 250,'activation_type': 'relu','dropout_strength': 0.2,'learning_rate': 0.01,'lr_decay': 0.00001,'epochs': 400,'batch_norm': True,'output_size': 3,}   

model = define_model(params)
model_name ="WeiAdm3bStd1_Flatpt"
save_path = "./"
batchsize=10000
save_best = keras.callbacks.ModelCheckpoint(filepath=save_path + model_name + "_best.h5", monitor='val_loss', verbose=0, save_best_only=True)
early_stopping = keras.callbacks.EarlyStopping(monitor='val_loss', min_delta=0, patience=20)
csv_logger = keras.callbacks.CSVLogger(save_path + model_name + '.log')
reduce_lr_on_plateau = keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=10, verbose=0, mode='auto', epsilon=0.0001, cooldown=0, min_lr=0)
callbacks = [save_best, early_stopping, csv_logger, reduce_lr_on_plateau]
history = model.fit(x=train_data,y=train_y,sample_weight=train_w,validation_data=(valid_data,valid_y,valid_w),batch_size=batchsize,callbacks=callbacks,epochs = params['epochs'])







