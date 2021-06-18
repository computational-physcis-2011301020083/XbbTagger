import argparse,math,os,glob,h5py
parser = argparse.ArgumentParser(description="%prog [options]", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--path", dest='path',  default="", help="path")
args = parser.parse_args()
import numpy as np
import keras

def load_Data(data,style):
  load_f=h5py.File(data)
  load_data=load_f.get(style)
  if "Hbb" in data:
    y=np.full((load_data.shape[0],),1,dtype=int)
    load_y=keras.utils.to_categorical(y, num_classes=3)
  if "Top" in data:
    y=np.full((load_data.shape[0],),2,dtype=int)
    load_y=keras.utils.to_categorical(y, num_classes=3)
  if "Dijets" in data:
    y=np.full((load_data.shape[0],),0,dtype=int)
    load_y=keras.utils.to_categorical(y, num_classes=3)
  load_fdata=np.hstack((load_y,load_data))
  load_fdata[:,3]=load_fdata[:,3]*2000000/np.sum(load_fdata[:,3]) #Nominalize sum of weight into total samples, change 2M according to samples
  return load_fdata

outname="train.h5" #Prepare training
#outname="test.h5" #Prepare testing
save_f = h5py.File("../DataVRGhost/PrepareData/"+outname, 'w')
files=sorted(glob.glob(args.path+"/*.h5"))

#Prepare training samples
train_Dijets=load_Data(files[0],"train")
train_Hbb=load_Data(files[1],"train")
train_Top=load_Data(files[2],"train")
train_data=np.vstack((train_Dijets,train_Hbb,train_Top))
save_f.create_dataset("train",data=train_data)

valid_Dijets=load_Data(files[0],"valid")
valid_Hbb=load_Data(files[1],"valid")
valid_Top=load_Data(files[2],"valid")
valid_data=np.vstack((valid_Dijets,valid_Hbb,valid_Top))
save_f.create_dataset("valid",data=valid_data)

#Prepare testing samples
'''
test_Dijets=load_Data(files[0],"test")
print files[0],files[1],files[2]
test_Hbb=load_Data(files[1],"test")
test_Top=load_Data(files[2],"test")
test_data=np.vstack((test_Dijets,test_Hbb,test_Top))
print test_data,test_data.shape
save_f.create_dataset("test",data=test_data)
'''



 












