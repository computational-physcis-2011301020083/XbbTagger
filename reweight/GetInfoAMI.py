import numpy as np

# weight calculation
FilterEff=np.array([1.,2.,3.,4.,5.])
CrossSect=np.array([2.,3.,4.,5.,6.])
TotalEvent=np.array([3.,4.,5.,6.,7.])
weight=FilterEff*CrossSect/TotalEvent
print weight.shape

import os
#Get Info from AMI
events=[]
filtereff=[]
xcross=[]
FileList=["mc16_13TeV.361020.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ0W.deriv.DAOD_FTAG5.e3569_s3126_r9364_p3870","mc16_13TeV.361021.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ1W.deriv.DAOD_FTAG5.e3569_s3126_r9364_p3870","mc16_13TeV.361022.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ2W.deriv.DAOD_FTAG5.e3668_s3126_r9364_p3870","mc16_13TeV.361023.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ3W.deriv.DAOD_FTAG5.e3668_s3126_r9364_p3870","mc16_13TeV.361024.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ4W.deriv.DAOD_FTAG5.e3668_s3126_r9364_p3870","mc16_13TeV.361025.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ5W.deriv.DAOD_FTAG5.e3668_s3126_r9364_p3870","mc16_13TeV.361026.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ6W.deriv.DAOD_FTAG5.e3569_s3126_r9364_p3870","mc16_13TeV.361027.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ7W.deriv.DAOD_FTAG5.e3668_s3126_r9364_p3870","mc16_13TeV.361028.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ8W.deriv.DAOD_FTAG5.e3569_s3126_r9364_p3870","mc16_13TeV.361029.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ9W.deriv.DAOD_FTAG5.e3569_s3126_r9364_p3870","mc16_13TeV.361030.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ10W.deriv.DAOD_FTAG5.e3569_s3126_r9364_p3870","mc16_13TeV.361031.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ11W.deriv.DAOD_FTAG5.e3569_s3126_r9364_p3870","mc16_13TeV.361032.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ12W.deriv.DAOD_FTAG5.e3668_s3126_r9364_p3870"]
for i in FileList:
  output=os.popen("ami show dataset info "+i)
  for line in output.readlines():
    if "totalEvents          :" in line:
      e=float(line.split(":")[1])
      #print e
      events.append(e)
    if "crossSection         :" in line:
      x=float(line.split(":")[1])
      print i,x
      xcross.append(x) 
    if "genFiltEff           :" in line:
      f=float(line.split(":")[1])
      #print f
      filtereff.append(f)
      

print "events",events
print "filtereff: ",filtereff
print "xcross: ",xcross

import numpy as np
events=np.asarray(events)
xcross=np.asarray(xcross)
filtereff=np.asarray(filtereff)
weights=filtereff*xcross/events
print weights

