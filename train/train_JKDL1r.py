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
train_file=h5py.File("../Xbb0106A/trainstd.h5","r")
train=train_file.get("train")
valid=train_file.get("valid")
print train.shape
train_data1=train[:,14:16]
train_data2=train[:,16:25]
train_data=np.hstack((train_data1,train_data2))
fatjet=train_data1
subjet0=train_data2[:,0:3]
subjet1=train_data2[:,3:6]
subjet2=train_data2[:,6:9]
train_y=train[:,0:3]
#train_w=train[:,3]
train_w=np.full((6000000, ), 1) #Equal weight

valid_data1=valid[:,14:16]
valid_data2=valid[:,16:25]
valid_data=np.hstack((valid_data1,valid_data2))
fatjetV=valid_data1
subjet0V=valid_data2[:,0:3]
subjet1V=valid_data2[:,3:6]
subjet2V=valid_data2[:,6:9]
valid_y=valid[:,0:3]
#valid_w=valid[:,3]
valid_w=np.full((600000, ), 1) #Equal weight


def define_model(params):
    kinematic_input = Input(shape=(2, ), name='fatjet')
    subjet_1_input = Input(shape=(3, ), name='subjet0') 
    subjet_2_input = Input(shape=(3, ), name='subjet1') 
    subjet_3_input = Input(shape=(3, ), name='subjet2')        
    inputs = [kinematic_input, subjet_1_input, subjet_2_input, subjet_3_input]
    concatenated_inputs = keras.layers.concatenate(inputs)
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
    model.compile(loss='categorical_crossentropy', optimizer=adm)
    return model

print "************ PHASE TRAINING *****************"
params = {'num_layers': 6,'num_units': 250,'activation_type': 'relu','dropout_strength': 0.,'learning_rate': 0.01,'lr_decay': 0.00001,'epochs': 200,'batch_norm': True,'output_size': 3,}   

model = define_model(params)
model_name ="WeiAdmStd_JKDL1r"
save_path = "./"
batchsize=10000
save_best = keras.callbacks.ModelCheckpoint(filepath=save_path + model_name + "_best.h5", monitor='val_loss', verbose=0, save_best_only=True)
early_stopping = keras.callbacks.EarlyStopping(monitor='val_loss', min_delta=0, patience=20)
csv_logger = keras.callbacks.CSVLogger(save_path + model_name + '.log')
reduce_lr_on_plateau = keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=10, verbose=0, mode='auto', epsilon=0.0001, cooldown=0, min_lr=0)
#callbacks = [save_best, early_stopping, csv_logger, reduce_lr_on_plateau]
callbacks = [save_best, csv_logger, reduce_lr_on_plateau]
history = model.fit(x=[fatjet,subjet0,subjet1,subjet2],y=train_y,sample_weight=train_w,validation_data=([fatjetV,subjet0V,subjet1V,subjet2V],valid_y,valid_w),batch_size=batchsize,callbacks=callbacks,epochs = params['epochs'])

arch = model.to_json()
with open(save_path + model_name + '_architecture.json', 'w') as arch_file:
        arch_file.write(arch)
model.save_weights(save_path + model_name + '_weights.h5')
model.save(save_path + model_name + '.h5')









