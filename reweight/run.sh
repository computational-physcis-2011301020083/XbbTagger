#Calculate weights for dijets samples
path="path to dijets samples"
python calculatedDijetsWeights.py --path $path

#Get VR Ghost jets 
python labelDijetsDatasets.py --path $pathToDijets
python labelHbbDatasets.py --path $pathToHbb
python labelTopDatasets.py --path $pathToTop

#Merge Hbb and Top samples
path="../DataVRGhost/ReducedHbb"
name="MergedHbb.h5"
python MergeDatasets.py --path $path --outname $path
path="../DataVRGhost/ReducedTop"
name="MergedTop.h5"
python MergeDatasets.py --path $path --outname $path



