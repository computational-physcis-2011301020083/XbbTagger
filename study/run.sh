#Prepare sample for study using testing sample from a model
python predict.py --path $pathToModel

#ROC study
python rocRatio.py --path $pathToPredictionfile

#Calculate the threshold corresponding to a certain signal efficiency
python calculateThresh.py --path $pathToPredictionfile 

#JSD study
python jsd.py --path $pathToPredictionfile --thresh $threshold

#Jet mass distribution
python jetmass.py --path $pathToPredictionfile --thresh $threshold --eff $SignalEff

