import math,os,glob,h5py
import numpy as np
import matplotlib.pyplot as plt

print("Loading data")
filepathDijets="../FlattenReweighted/MergedDijets.h5"
filepathHiggs="../FlattenReweighted/MergedHbb.h5"
filepathTop="../FlattenReweighted/MergedTop.h5"
loadDijets=h5py.File(filepathDijets,'r')
loadHiggs=h5py.File(filepathHiggs,'r')
loadTop=h5py.File(filepathTop,'r')
dijets=loadDijets.get("data")
hbb=loadHiggs.get("data")
top=loadTop.get("data")

print("Loading pt and eta")
#dijets=np.reshape(dijets,(dijets.shape[0],dijets.shape[1]))
#hbb=np.reshape(hbb,(hbb.shape[0],hbb.shape[1]))
#top=np.reshape(top,(top.shape[0],top.shape[1]))

#dijetspt=dijets[:,8:9]
#higgspt=hbb[:,8:9]
#topt=top[:,8:9]
#dijetseta=dijets[:,9:10]
#higgseta=hbb[:,9:10]
#topeta=top[:,9:10]

dijetspt=dijets[:,8]
higgspt=hbb[:,8]
topt=top[:,8]
dijetseta=dijets[:,9]
higgseta=hbb[:,9]
topeta=top[:,9]

dijetsweight=np.full((dijetspt.shape[0], 1), 1)
higgsweight=np.full((higgspt.shape[0], 1), 1)
topweight=np.full((topt.shape[0], 1), 1)

ptbins=np.linspace(0, 4000, 401)
etabins=np.linspace(-3.2, 3.2, 401)

print("Processing 1")
dijetshist,_,_= np.histogram2d(dijetseta, dijetspt,[etabins, ptbins])
higgshist,_,_ = np.histogram2d(higgseta,higgspt,[etabins, ptbins])
tophist,_,_ = np.histogram2d(topeta,topt,[etabins, ptbins])

dijets_locations_pt = np.digitize(dijetspt, ptbins) - 1
dijets_locations_eta = np.digitize(dijetseta, etabins) - 1
dijets_locations = zip(dijets_locations_pt, dijets_locations_eta)
dijets_locations = list(dijets_locations)

higgs_locations_pt = np.digitize(higgspt, ptbins) - 1
higgs_locations_eta = np.digitize(higgseta, etabins) - 1
higgs_locations = zip(higgs_locations_pt, higgs_locations_eta)
higgs_locations = list(higgs_locations)

top_locations_pt = np.digitize(topt, ptbins) - 1
top_locations_eta = np.digitize(topeta, etabins) - 1
top_locations = zip(top_locations_pt, top_locations_eta)
top_locations = list(top_locations)

print("Processing 2")
dijets_loc_indices = { (pti, etai) : [] for pti,_ in enumerate(ptbins[::-1]) for etai,_ in enumerate(etabins[::-1])}
higgs_loc_indices = { (pti, etai) : [] for pti,_ in enumerate(ptbins[::-1]) for etai,_ in enumerate(etabins[::-1])}
top_loc_indices = { (pti, etai) : [] for pti,_ in enumerate(ptbins[::-1]) for etai,_ in enumerate(etabins[::-1])}
for i, x in enumerate(dijets_locations):
        dijets_loc_indices[x].append(i)
for i, x in enumerate(higgs_locations):
        higgs_loc_indices[x].append(i)
for i, x in enumerate(top_locations):
        top_loc_indices[x].append(i)
dijets_indices = []
higgs_indices = []
top_indices = []

print("Processing 3")
for pt_bin_i in range(len(ptbins) - 1):
        for eta_bin_i in range(len(etabins) - 1):
            loc = (pt_bin_i, eta_bin_i)
            ndijets = int(dijetshist[eta_bin_i][pt_bin_i])
            nhiggs = int(higgshist[eta_bin_i][pt_bin_i])
            ntop = int(tophist[eta_bin_i][pt_bin_i])
            njets = min([ndijets, nhiggs, ntop])
            dijets_indices_for_bin = dijets_loc_indices[loc][0:njets]
            higgs_indices_for_bin = higgs_loc_indices[loc][0:njets]
            top_indices_for_bin = top_loc_indices[loc][0:njets]
            dijets_indices += dijets_indices_for_bin
            higgs_indices += higgs_indices_for_bin
            top_indices += top_indices_for_bin

dijets_indices.sort()
higgs_indices.sort()
top_indices.sort()
print(np.array(dijets_indices), np.array(higgs_indices), np.array(top_indices))


plt.figure()
Dijets=np.take(dijets, dijets_indices,axis=0)
Higgs=np.take(hbb, higgs_indices,axis=0)
Top=np.take(top, top_indices,axis=0)
print(Dijets.shape)
plt.hist(Dijets[:,9],weights=np.full((Dijets.shape[0], ), 1),bins=etabins,label="QCD_pt",histtype="step")
plt.hist(Higgs[:,9],weights=np.full((Higgs.shape[0], ), 1),bins=etabins,label="Higgs_pt",histtype="step")
plt.hist(Top[:,9],weights=np.full((Top.shape[0], ), 1),bins=etabins,label="Top_pt",histtype="step")
#plt.plot(np.linspace(0, 4000, 400),minjets,label="minjets")
plt.xlabel('eta')
plt.ylabel('events')
plt.yscale("log", nonposy="clip")
plt.legend(loc='best')
plt.show()
name="figures/"+"eta.pdf"
plt.savefig(name)

finaldijets=Dijets
print( finaldijets.shape)
savedijets = h5py.File("../FlattenResample/MergedDijets.h5", 'w')
savedijets.create_dataset("data",data=finaldijets)
savedijets.close()

finaltop=Top
print( finaltop.shape)
savetop = h5py.File("../FlattenResample/MergedTop.h5", 'w')
savetop.create_dataset("data",data=finaltop)
savetop.close()

finalhbb=Higgs
print( finalhbb.shape)
savehbb = h5py.File("../FlattenResample/MergedHbb.h5", 'w')
savehbb.create_dataset("data",data=finalhbb)
savehbb.close()


