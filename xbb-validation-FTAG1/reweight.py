import math,os,glob,h5py
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

filepathDijets="/global/project/projectdirs/atlas/massDecorrelatedXbb/DAOD0401/Reduced/Convert/qcd.root"
filepathHiggs="/global/project/projectdirs/atlas/massDecorrelatedXbb/DAOD0401/Reduced/Convert/higgs.root"
filepathTop="/global/project/projectdirs/atlas/massDecorrelatedXbb/DAOD0401/Reduced/Convert/top.root"
loadDijets=h5py.File(filepathDijets,'r')
loadHiggs=h5py.File(filepathHiggs,'r')
loadTop=h5py.File(filepathTop,'r')

dijets=loadDijets.get("data")
hbb=loadHiggs.get("data")
top=loadTop.get("data")
dijets=np.reshape(dijets,(dijets.shape[0],dijets.shape[1]))
hbb=np.reshape(hbb,(hbb.shape[0],hbb.shape[1]))
top=np.reshape(top,(top.shape[0],top.shape[1]))

dijetspt=dijets[:,3:4]
dijetsweight=dijets[:,1:2]
hbbpt=hbb[:,3:4]
#hbbweight=hbb[:,0:1]
toppt=top[:,3:4]
#topweight=top[:,0:1]
hbbweight=np.full((hbbpt.shape[0], 1), 1)
topweight=np.full((toppt.shape[0], 1), 1)

bins=np.linspace(0, 4000, 201)
indices=np.digitize(hbbpt,bins)-1
indices1=np.digitize(toppt,bins)-1
#print indices[0:50]-1
dijetshist=np.histogram(dijetspt, bins, weights=dijetsweight)[0]
hbbhist=np.histogram(hbbpt, bins, weights=hbbweight)[0]
tophist=np.histogram(toppt, bins, weights=topweight)[0]
#print dijetshist,hbbhist
ratio=np.zeros_like(dijetshist)
ratio1=np.zeros_like(dijetshist)
valid = np.asarray(hbbhist) > 0.0
valid1=np.asarray(tophist) > 0.0
#print ratio,valid
ratio[valid] = dijetshist[valid] / hbbhist[valid]
ratio1[valid1] = dijetshist[valid1] / tophist[valid1]
#print ratio
reweight=ratio[indices]
hbbhist_reweighted= np.histogram(hbbpt, bins, weights=reweight)[0]
reweight1=ratio1[indices1]
tophist_reweighted= np.histogram(toppt, bins, weights=reweight1)[0]

finalhbb=np.hstack((reweight,hbb))
print finalhbb.shape
savehbb = h5py.File("/global/project/projectdirs/atlas/massDecorrelatedXbb/DAOD0401/Reduced/Reweight/higgs.h5", 'w')
savehbb.create_dataset("data",data=finalhbb)
savehbb.close()
finaltop=np.hstack((reweight1,top))
print finaltop.shape
savetop = h5py.File("/global/project/projectdirs/atlas/massDecorrelatedXbb/DAOD0401/Reduced/Reweight/top.h5", 'w')
savetop.create_dataset("data",data=finaltop)
savetop.close()
finaldijets=np.hstack((dijetsweight,dijets))
print finaldijets.shape
savedijets=h5py.File("/global/project/projectdirs/atlas/massDecorrelatedXbb/DAOD0401/Reduced/Reweight/qcd.h5", 'w')
savedijets.create_dataset("data",data=finaldijets)
savedijets.close()

plt.figure(1)
plt.hist(dijetspt,weights=dijetsweight,bins=bins,label="dijets_pt",histtype="step")
plt.hist(hbbpt,weights=reweight,bins=bins,label="hbb_pt",histtype="step")
plt.hist(toppt,weights=reweight1,bins=bins,label="top_pt",histtype="step")
plt.xlabel('pt')
plt.ylabel('events')
plt.yscale("log", nonposy="clip")
#plt.xlim(left=0.2)
#plt.ylim(top=0.2e6)
plt.legend(loc='best')
ROC_file="figures/"+"reweightPt.pdf"
plt.savefig(ROC_file)
plt.show()

































