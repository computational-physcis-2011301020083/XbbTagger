import pandas as pd
import glob,h5py
import numpy as np
import argparse,math,os
parser = argparse.ArgumentParser(description="%prog [options]", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--path", dest='path',  default="", help="path")
args = parser.parse_args()

features_group1=['weight','relativeDeltaRToVRJet_1','relativeDeltaRToVRJet_2','relativeDeltaRToVRJet_3','eventNumber','dsid','mass','pt','eta'] #0-9
features_group2=['DL1rT_pu_1', 'DL1rT_pc_1', 'DL1rT_pb_1','DL1rT_pu_2', 'DL1rT_pc_2', 'DL1rT_pb_2','DL1rT_pu_3', 'DL1rT_pc_3', 'DL1rT_pb_3']
features_group3=['DL1r_pu_1', 'DL1r_pc_1', 'DL1r_pb_1','DL1r_pu_2', 'DL1r_pc_2', 'DL1r_pb_2','DL1r_pu_3', 'DL1r_pc_3', 'DL1r_pb_3'] #9-27
features_group4=['Split12', 'Split23', 'Qw', 'PlanarFlow', 'Angularity', 'Aplanarity', 'ZCut12', 'KtDR', 'C2', 'D2', 'e3', 'Tau21_wta', 'Tau32_wta', 'FoxWolfram20'] #27-41
features_group5=['JetFitter_N2Tpair_1', 'JetFitter_dRFlightDir_1', 'JetFitter_deltaeta_1', 'JetFitter_deltaphi_1', 'JetFitter_energyFraction_1', 'JetFitter_mass_1', 'JetFitter_massUncorr_1', 'JetFitter_nSingleTracks_1', 'JetFitter_nTracksAtVtx_1', 'JetFitter_nVTX_1', 'JetFitter_significance3d_1','SV1_L3d_1', 'SV1_Lxy_1', 'SV1_N2Tpair_1', 'SV1_NGTinSvx_1', 'SV1_deltaR_1', 'SV1_dstToMatLay_1', 'SV1_efracsvx_1', 'SV1_masssvx_1', 'SV1_significance3d_1', 'rnnip_pu_1', 'rnnip_pc_1', 'rnnip_pb_1', 'rnnip_ptau_1', 'JetFitter_N2Tpair_2', 'JetFitter_dRFlightDir_2', 'JetFitter_deltaeta_2', 'JetFitter_deltaphi_2', 'JetFitter_energyFraction_2', 'JetFitter_mass_2', 'JetFitter_massUncorr_2', 'JetFitter_nSingleTracks_2', 'JetFitter_nTracksAtVtx_2', 'JetFitter_nVTX_2', 'JetFitter_significance3d_2', 'SV1_L3d_2', 'SV1_Lxy_2', 'SV1_N2Tpair_2', 'SV1_NGTinSvx_2', 'SV1_deltaR_2', 'SV1_dstToMatLay_2', 'SV1_efracsvx_2', 'SV1_masssvx_2', 'SV1_significance3d_2',  'rnnip_pu_2', 'rnnip_pc_2', 'rnnip_pb_2', 'rnnip_ptau_2', 'JetFitter_N2Tpair_3', 'JetFitter_dRFlightDir_3', 'JetFitter_deltaeta_3', 'JetFitter_deltaphi_3', 'JetFitter_energyFraction_3', 'JetFitter_mass_3', 'JetFitter_massUncorr_3', 'JetFitter_nSingleTracks_3', 'JetFitter_nTracksAtVtx_3', 'JetFitter_nVTX_3', 'JetFitter_significance3d_3', 'SV1_L3d_3', 'SV1_Lxy_3', 'SV1_N2Tpair_3', 'SV1_NGTinSvx_3', 'SV1_deltaR_3', 'SV1_dstToMatLay_3', 'SV1_efracsvx_3', 'SV1_masssvx_3', 'SV1_significance3d_3', 'rnnip_pu_3', 'rnnip_pc_3', 'rnnip_pb_3', 'rnnip_ptau_3'] #41-113

new_file_name=args.path.split("/")[-1]
new_hdf5 = h5py.File("/global/project/projectdirs/atlas/massDecorrelatedXbb/Xbb0106/DataVRGhost/FlattenData/MergedDijets/"+new_file_name, 'w')
df = pd.read_hdf(args.path)[features_group1+features_group2] #+features_group3+features_group4]
#df['dsid']=pd.to_numeric(df['dsid'])

Data=df.values
print Data.shape
Data=Data[Data[:,7]<3000.]
print Data.shape
#Data0=Data[(Data[:,1]<1.) | (Data[:,2]<1.) | (Data[:,3]<1.)]
#print Data0.shape
Data=Data[(Data[:,1]>1.) | (Data[:,2]>1.) | (Data[:,3]>1.)]
print Data.shape
for i in range(Data.shape[0]):
    if Data[i,1]<1.:
        Data[i,9:12]=np.nan
    if Data[i,2]<1.:
        Data[i,12:15]=np.nan
    if Data[i,3]<1.:
        Data[i,15:18]=np.nan

'''
#Check
Data1=Data[Data[:,1]<1.]
print Data1.shape
Data2=Data[Data[:,2]<1.]
print Data2.shape  
Data3=Data[Data[:,3]<1.]
print Data3.shape,Data[100:200,:] 
'''
#DL1rBaseline
f=0.018
DL1r_baseline=np.stack([Data[:,11:12]/((1-f)*Data[:,9:10]+f*Data[:,10:11]), Data[:,14:15]/((1-f)*Data[:,12:13]+f*Data[:,13:14])], axis=1).min(axis=1)
invalid = np.isnan(DL1r_baseline) | np.isinf(DL1r_baseline)
DL1r_baseline[invalid] = 1e-15
DL1rBaseline=np.log(np.clip(DL1r_baseline, 1e-30, 1e30))
print DL1rBaseline.shape,DL1rBaseline[100:140,:]

#binned_dl1r
DL1rDisc1=Data[:,11:12]/((1-f)*Data[:,9:10]+f*Data[:,10:11])
DL1rDisc2=Data[:,14:15]/((1-f)*Data[:,12:13]+f*Data[:,13:14])
DL1rDisc3=Data[:,17:18]/((1-f)*Data[:,15:16]+f*Data[:,16:17]) 
DL1rDisc=np.hstack((DL1rDisc1,DL1rDisc2,DL1rDisc3))
print DL1rDisc.shape,DL1rDisc[100:140,:]
DL1rDisc[np.isnan(DL1rDisc) | np.isinf(DL1rDisc)]=np.nan
print DL1rDisc.shape,DL1rDisc[100:140,:]
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
print DL1rDisc.shape,DL1rDisc[100:140,:]

final=np.hstack((Data,DL1rDisc,DL1rBaseline))
print final.shape
'''
DL1rDisc=np.where(DL1rDisc>4.805,5,DL1rDisc)
print DL1rDisc.shape,DL1rDisc[100:140,:]
'''
new_hdf5.create_dataset("data",data=final)




