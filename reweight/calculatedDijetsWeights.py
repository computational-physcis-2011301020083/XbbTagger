import pandas as pd
import glob
import numpy as np
import h5py
import argparse,math,os
parser = argparse.ArgumentParser(description="%prog [options]", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--path", dest='path',  default="", help="path")
args = parser.parse_args()

filterEff = np.array([0.9755, 0.00067152, 0.00033434, 0.00032012, 0.00053137, 0.00092395, 0.0009427, 0.0003928, 0.010176, 0.012077, 0.0059083, 0.0026761, 0.00042592])
xsec = np.array([78420000.0, 78420000.0, 2433200.0, 26454.0, 254.63, 4.5535, 0.25753, 0.016215, 0.00062503, 1.9639e-05, 1.1962e-06, 4.2259e-08, 1.0367e-09])
dsid=np.array(["361020","361021","361022","361023","361024","361025","361026","361027","361028","361029","361030","361031","361032"])
filterEffTimesXsec = filterEff*xsec
#eventsPYAMI=[153.0, 173.0, 665.0, 9072446.0, 15546372.0, 15993248.0, 17834000.0, 15983000.0, 15999000.0, 13995500.0, 13985000.0, 15948000.0, 15995600.0]
events=[]

for i in range(0,len(dsid)):
  events.append(0)
for i in range(0,len(dsid)):
  paths= glob.glob(args.path+"/*"+dsid[i]+"*.h5")
  for f in paths:
    hf= h5py.File(f, "r")
    #print i,f,events[i],hf["metadata"]["nEventsProcessed"].shape,np.sum(hf["metadata"]["nEventsProcessed"]),hf["metadata"]["nEventsProcessed"]
    events[i]=events[i]+np.sum(hf["metadata"]["nEventsProcessed"])
  print dsid[i],events[i]
print events

list1={}
for i in range(0,len(dsid)):
  list1[int(dsid[i])]=filterEffTimesXsec[i]/float(events[i])
print list1



