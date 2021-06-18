import ROOT,os,glob,math
from array import array
import argparse
parser = argparse.ArgumentParser(description="%prog [options]", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--path", dest='path',  default="", help="path")
parser.add_argument("--outname", dest='outname',  default="", help="outname")
args = parser.parse_args()
#path1=args.path
filepath="../Original/Merge/*"
paths=sorted(glob.glob(filepath+"*qcd*"))
print paths
path=paths[int(args.path)]
f=ROOT.TFile(path,"r")
t=f.Get("FlavourTagging_Nominal")
#hist="MetaData_EventCount"
#metadata=f.Get(hist)
fname=path.split("/")[-1]
newf=ROOT.TFile("../Reduced/"+fname,"recreate")
newt=ROOT.TTree("t","test tree")
#SumOfWeights=metadata.GetBinContent(4)
N=t.GetEntries()
mcEventWeight=array("f",[0.])
Weight=array("f",[0.])
m=array("f",[0.])
pt=array("f",[0.])
eta=array("f",[0.])
QCD=array("f",[0.])
Higgs=array("f",[0.])
Top=array("f",[0.])
isQCD=array("f",[0.])
isHiggs=array("f",[0.])
isTop=array("f",[0.])
DL1r_pu_1=array("f",[0.])
DL1r_pb_1=array("f",[0.])
DL1r_pc_1=array("f",[0.])
DL1r_pu_2=array("f",[0.])
DL1r_pb_2=array("f",[0.])
DL1r_pc_2=array("f",[0.])
newt.Branch("mcEventWeight",mcEventWeight,"mcEventWeight/F")
newt.Branch("Weight",Weight,"Weight/F")
newt.Branch("m",m,"m/F")
newt.Branch("pt",pt,"pt/F")
newt.Branch("eta",eta,"eta/F")
newt.Branch("QCD",QCD,"QCD/F")
newt.Branch("Higgs",Higgs,"Higgs/F")
newt.Branch("Top",Top,"Top/F")
newt.Branch("isQCD",isQCD,"isQCD/F")
newt.Branch("isHiggs",isHiggs,"isHiggs/F")
newt.Branch("isTop",isTop,"isTop/F")
newt.Branch("DL1r_pu_1",DL1r_pu_1,"DL1r_pu_1/F")
newt.Branch("DL1r_pb_1",DL1r_pb_1,"DL1r_pb_1/F")
newt.Branch("DL1r_pc_1",DL1r_pc_1,"DL1r_pc_1/F")
newt.Branch("DL1r_pu_2",DL1r_pu_2,"DL1r_pu_2/F")
newt.Branch("DL1r_pb_2",DL1r_pb_2,"DL1r_pb_2/F")
newt.Branch("DL1r_pc_2",DL1r_pc_2,"DL1r_pc_2/F")
Dsid=int(fname.split(".")[1])
dsid=array("i",[0])
newt.Branch("dsid",dsid,"dsid/I")
#h=ROOT.TH1F( 'h', 'higgs score', 50, 0, 10 )
reweight=[2.12081115, 0.76465958 ,0.3977954  ,0.08777136 ,0.04706718]
for i in range(N):
  t.GetEntry(i)
  #print t.fat_pt.size()
  if t.fat_pt.size()>=1 and t.fat_assocTrkjet_ind[0].size()>=2:
   if t.fat_assocTrkjet_ind[0][1]<=t.trkjet_DL1r_pb.size()-1 and t.fat_assocTrkjet_ind[0][1]<=t.trkjet_DL1r_pu.size()-1 and t.fat_assocTrkjet_ind[0][1]<=t.trkjet_DL1r_pc.size()-1:
    mcEventWeight[0]=t.eve_mc_w
    Weight[0]=mcEventWeight[0]*reweight[int(args.path)]
    #EventNumber[0]=t.eve_num
    pt[0]=t.fat_pt[0]/1000.0
    eta[0]=t.fat_eta[0]
    V=ROOT.TLorentzVector()
    V.SetPtEtaPhiE(t.fat_pt[0],t.fat_eta[0],t.fat_phi[0],t.fat_E[0])
    m[0]=V.M()/1000.0
    QCD[0]=t.fat_SubjetBScore_QCD[0]
    Top[0]=t.fat_SubjetBScore_Top[0]
    Higgs[0]=t.fat_SubjetBScore_Higgs[0]
    #Bhad=t.fat_BHad_n
    #Bhad1=t.fat_BHad_n_GA
    #n1=t.fat_assocTrkjet_ind
    #isGbb=t.fat_isGbbJet
    #Higgs=t.fat_XbbScoreHiggs #[0]
    #Higgs=t.fat_HbbScore[0]
    isQCD[0]=1
    isTop[0]=0
    isHiggs[0]=0
    dsid[0]=Dsid
    DL1r_pu_1[0]=t.trkjet_DL1r_pu[t.fat_assocTrkjet_ind[0][0]]
    DL1r_pu_2[0]=t.trkjet_DL1r_pu[t.fat_assocTrkjet_ind[0][1]]
    DL1r_pb_1[0]=t.trkjet_DL1r_pb[t.fat_assocTrkjet_ind[0][0]]
    DL1r_pb_2[0]=t.trkjet_DL1r_pb[t.fat_assocTrkjet_ind[0][1]]
    DL1r_pc_1[0]=t.trkjet_DL1r_pc[t.fat_assocTrkjet_ind[0][0]]
    DL1r_pc_2[0]=t.trkjet_DL1r_pc[t.fat_assocTrkjet_ind[0][1]]
    #print Higgs,QCD,
    #print pt,QCD,Top,Higgs,n1,mcEventWeight
    newt.Fill()
newf.Write()
newf.Close()
print "done"
