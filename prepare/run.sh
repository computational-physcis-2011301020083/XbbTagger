#Prepare training and testing samples
path="../DataVRGhost/SplitData"
python prepare.py --path $path

#Calculate mean and std
path="../DataVRGhost/PrepareData/train.h5"
python calculateMean.py --path $path

#Scaling samples
path="../DataVRGhost/PrepareData/train.h5"
python scaling.py --path $path
path="../DataVRGhost/PrepareData/test.h5"
python scaling.py --path $path

