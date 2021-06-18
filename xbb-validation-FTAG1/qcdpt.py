import ROOT,os,glob,math
from array import array

path="../Reduced/Merge/qcd.root"
f=ROOT.TFile(path,"r")
t=f.Get("t")
t.Show(1)
N=t.GetEntries()
h=ROOT.TH1F( 'h', 'qcd pt', 200, 0, 4000 )
for i in range(N):
    t.GetEntry(i)
    h.Fill(t.pt,t.Weight)
c1=ROOT.TCanvas("c1","c1",100,0,900,700)
c1.SetLogy()
#ROOT.gStyle.SetOptStat(0)
c1.cd()
h.Draw()
c1.Draw()
c1.SaveAs("figures/qcdpt.pdf")



