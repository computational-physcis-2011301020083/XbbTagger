import pandas as pd
import glob
import argparse,math,os
parser = argparse.ArgumentParser(description="%prog [options]", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--path", dest='path',  default="", help="path")
args = parser.parse_args()

tCountKey = "GhostTQuarksFinalCount"
hCountKey = "GhostHBosonsCount"
bCountKey = "GhostBHadronsFinalCount"
def label_row(row, isTopSample):
    if isTopSample:
      if  row[tCountKey] >= 1 and  row[hCountKey]<=0:
        return "top"
      else:
        return "ignore"
    else :
      if  row[tCountKey] >= 1 and  row[hCountKey]<=0:
        return "ignore"
      else :
        return "qcd"

filePaths = glob.glob(args.path+"/TopDatasets/*.h5")
#Jet substructure and mass pt
list1=['Split12', 'Split23', 'Qw', 'PlanarFlow', 'Angularity', 'Aplanarity', 'ZCut12', 'KtDR', 'XbbScoreQCD', 'XbbScoreTop', 'XbbScoreHiggs', 'pt', 'eta', 'GhostHBosonsCount', 'GhostTQuarksFinalCount', 'GhostBHadronsFinalCount',  'mcEventWeight',  'mass', 'C2', 'D2', 'e3', 'Tau21_wta', 'Tau32_wta', 'FoxWolfram20']
#Flavor tagging variables
list2=['MV2c10_discriminant', 'IP2D_pb', 'IP2D_pc', 'IP2D_pu', 'IP3D_pb', 'IP3D_pc', 'IP3D_pu', 'JetFitter_N2Tpair', 'JetFitter_dRFlightDir', 'JetFitter_deltaeta', 'JetFitter_deltaphi', 'JetFitter_energyFraction', 'JetFitter_mass', 'JetFitter_massUncorr', 'JetFitter_nSingleTracks', 'JetFitter_nTracksAtVtx', 'JetFitter_nVTX', 'JetFitter_significance3d', 'SV1_L3d', 'SV1_Lxy', 'SV1_N2Tpair', 'SV1_NGTinSvx', 'SV1_deltaR', 'SV1_dstToMatLay', 'SV1_efracsvx', 'SV1_masssvx', 'SV1_pb', 'SV1_pc', 'SV1_pu', 'SV1_significance3d', 'deta', 'dphi', 'dr', 'eta', 'pt', 'rnnip_pb', 'rnnip_pc', 'rnnip_ptau', 'rnnip_pu']
#DL1r variables
#list2=['DL1r_pu','DL1r_pc','DL1r_pb']

list3={}
list4={}
list5={}
for i in list2:
  list3[i]=i+"_1"
  list4[i]=i+"_2"
  list5[i]=i+"_3"

count=0
for filePath in filePaths:
  count=count+1
  sourceDataset=filePath.split("/")[-1]
  print "Processing count: ",count
  isTopSample = True
  h1=pd.read_hdf(filePath, "subjet_VRGhostTag_1")[list2]
  h1.rename(columns=list3,inplace=True)
  h2=pd.read_hdf(filePath, "subjet_VRGhostTag_2")[list2]
  h2.rename(columns=list4,inplace=True)
  h3=pd.read_hdf(filePath, "subjet_VRGhostTag_3")[list2]
  h3.rename(columns=list5,inplace=True)
  newDf =  pd.concat([pd.read_hdf(filePath, "fat_jet")[list1], h1,h2,h3], axis=1)
  newDf["label"] = newDf.apply(lambda row: label_row(row, isTopSample), axis=1)
  newDf["pt"] = (newDf["pt"]/1000.0).astype("float64")
  newDf["mass"] = (newDf["mass"]/1000.0).astype("float64")
  newDf["weight"]=newDf["mcEventWeight"]
  newDf=newDf[newDf["label"]!="ignore"]
  newDf["signal"]=0
  newDf["dsid"]=sourceDataset.split("_")[2]

  newDfFilePath = "../DataVRGhost/ReducedTop/" + sourceDataset
  newDf.to_hdf(newDfFilePath, "dataset", format="table", data_columns=True)
  print "Done "







