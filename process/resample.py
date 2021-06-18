import math,os,glob,h5py
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt


filepathDijets="/global/project/projectdirs/atlas/massDecorrelatedXbb/Xbb0202/DataVRGhost/FlattenReweighted/MergedDijets.h5"
filepathHiggs="/global/project/projectdirs/atlas/massDecorrelatedXbb/Xbb0202/DataVRGhost/FlattenReweighted/MergedHbb.h5"
filepathTop="/global/project/projectdirs/atlas/massDecorrelatedXbb/Xbb0202/DataVRGhost/FlattenReweighted/MergedTop.h5"
loadDijets=h5py.File(filepathDijets,'r')
loadHiggs=h5py.File(filepathHiggs,'r')
loadTop=h5py.File(filepathTop,'r')
dijets=loadDijets.get("data")
hbb=loadHiggs.get("data")
top=loadTop.get("data")
print dijets.shape
print "1"

dijets=np.reshape(dijets,(dijets.shape[0],dijets.shape[1]))
hbb=np.reshape(hbb,(hbb.shape[0],hbb.shape[1]))
top=np.reshape(top,(top.shape[0],top.shape[1]))
print "2"

dijetspt=dijets[:,8:9]
higgspt=hbb[:,8:9]
topt=top[:,8:9]
dijetsweight=np.full((dijetspt.shape[0], 1), 1)
higgsweight=np.full((higgspt.shape[0], 1), 1)
topweight=np.full((topt.shape[0], 1), 1)

bins=np.linspace(0, 4000, 401)
dijetshist,binedge=np.histogram(dijetspt, bins, weights=dijetsweight)#[0]
higgshist=np.histogram(higgspt, bins, weights=higgsweight)[0]
tophist=np.histogram(topt, bins, weights=topweight)[0]
dijetsindice=np.array(list(np.digitize(dijetspt,bins)-1))
higgsindice=np.array(list(np.digitize(higgspt,bins)-1))
topindice=np.array(list(np.digitize(topt,bins)-1))
dijetsindicept=np.column_stack((dijetsindice,dijetspt,dijets))
higgsindicept=np.column_stack((higgsindice,higgspt,hbb))
topindicept=np.column_stack((topindice,topt,top))

jetcounts=np.column_stack((dijetshist,higgshist,tophist))
minjets=np.amin(jetcounts,axis=1)
print "3"

for ibin, njets in enumerate(minjets):
    #print ibin,njets,dijetshist[ibin],higgshist[ibin],tophist[ibin]
    if njets!=0: # and ibin<=30:
        if ibin==25:
            redijets=dijetsindicept[dijetsindicept[:,0]==ibin][0:njets]
            rehiggs=higgsindicept[higgsindicept[:,0]==ibin][0:njets]
            retop=topindicept[topindicept[:,0]==ibin][0:njets]
        else:
            redijets=np.vstack((redijets,dijetsindicept[dijetsindicept[:,0]==ibin][0:njets]))
            rehiggs=np.vstack((rehiggs,higgsindicept[higgsindicept[:,0]==ibin][0:njets]))
            retop=np.vstack((retop,topindicept[topindicept[:,0]==ibin][0:njets]))
print "4"


finaldijets=redijets[:,2:]
print finaldijets.shape
savedijets = h5py.File("/global/project/projectdirs/atlas/massDecorrelatedXbb/Xbb0202/DataVRGhost/FlattenResample/MergedDijets.h5", 'w')
savedijets.create_dataset("data",data=finaldijets)
savedijets.close()

finaltop=retop[:,2:]
print finaltop.shape
savetop = h5py.File("/global/project/projectdirs/atlas/massDecorrelatedXbb/Xbb0202/DataVRGhost/FlattenResample/MergedTop.h5", 'w')
savetop.create_dataset("data",data=finaltop)
savetop.close()

finalhbb=rehiggs[:,2:]
print finalhbb.shape
savehbb = h5py.File("/global/project/projectdirs/atlas/massDecorrelatedXbb/Xbb0202/DataVRGhost/FlattenResample/MergedHbb.h5", 'w')
savehbb.create_dataset("data",data=finalhbb)
savehbb.close()


print "5"

plt.hist(redijets[:,1],weights=np.full((redijets.shape[0], ), 1),bins=bins,label="QCD_pt",histtype="step")
plt.hist(rehiggs[:,1],weights=np.full((rehiggs.shape[0], ), 1),bins=bins,label="Higgs_pt",histtype="step")
plt.hist(retop[:,1],weights=np.full((retop.shape[0], ), 1),bins=bins,label="Top_pt",histtype="step")
plt.plot(np.linspace(0, 4000, 400),minjets,label="minjets")
plt.xlabel('pt')
plt.ylabel('events')
plt.yscale("log", nonposy="clip")
plt.legend(loc='best')
pt_file="figures/"+"resamplePt.pdf"
plt.savefig(pt_file)
#plt.show()

print "6"
