# Mass-decorrelated-Xbb-tagger

Tools for training and study of mass de-correlated Xbb tagger using deep neural network
by Wei Ding wei.ding@cern.ch .

This tool is inherited from the [tool](https://gitlab.cern.ch/atlas-boosted-hbb/xbb-tagger-training) by Julian Collado Umana.  
[Here](https://gitlab.cern.ch/atlas-boosted-xbb/xbb-datasets) is the input MC samples. 
And more studies of this tagger are [here](https://indico.cern.ch/event/864911/). 

The instructions for how to run are in the file **run.sh** in each directory:

1. reweight


- Get the h5 [samples](https://gitlab.cern.ch/atlas-boosted-xbb/xbb-datasets) from grid using **download.py** first,
then rename them using **rename.py** and divide them into three categories in three directories: Hbb Dijets Top .

- Get the cross-section and filter-efficiency informations of Dijets samples from grid using **GetInfoAMI.py** and calculate the normalization weights for them using **calculatedDijetsWeights.py**.

- Get the variables for training using **label*Datasets.py**.


- After that, we can merge the Hbb samples and Top samples into one pd file using **MergeDatasets.py**,
the Dijets samples are too large, so next, we need to sub-sample them into suitable size as Top and Hbb samples.

- The **printINFO.py** is used to print out the informations and variables in these h5 files.

2. process

- Sub-sample the Dijets sample in directoy mergeDijets :

  - Flatten these samples using **flattenDijets.py** first.

  - Merge these samples by DSID using **MergeDijetsDSID.py**.

  - Sub-sample then by DSID using **subsampleDijets.py**.

  - Merge them into one file using **MergeDijets.py**.

- Flatten the Hbb and Top samples using **flatten.py**, now we get three flatted samples Hbb Top and Dijets.

- Perform pt-eta 2D resampling using **resample2D.py**.

- Split these three samples into training validation and test using **split.py**.

- Scripts **resample.py** and **reweight.py** are used to perform pt resampling and reweighting. 


3. prepare

- Label and merge the training and validation parts of these three samples using **prepare.py**.

- Label and merge the test part of these three samples using **prepare.py**.

- Calculate the mean and std of training part using **calculateMean.py**, they will be used for scaling.

- Scale the training and validation parts of these samples using **scaling.py**.

- Scale the test part of these samples using **scaling.py**.

4. train

- Perform training using **train_JKDL1r.py**.

5. study

- Make predictions for test samples from trained 2D model using **predict.py**.

- Study the mass correlations of the trained 2D model using **jetmass.py**.

- Study the ROC performances of the trained 2D model using **roc.py**.

- Study the Loss function of the trained 2D model using **loss.py** to make sure that there is no over-fitting.

- Jupyter scripts  **ROC.ipynb** and **ROCRatioPanel.ipynb** are used to study the ROC performances of the trained 2D model.

- Script **calculateThresh.py** is used to calculate the threshold for a fixed working point.

- Script **jsd.py** is used to study the JSD.

- Script **EffVSMass.py** is used to plot the efficiency as a function of mass.


6. model2D

- The trained 2D model, informations for this model is in **info.txt**.

- The **predict.py** is used to make predictions from primal h5 files to validate this model.

- The converted json file of this model for C++ is in **lwnn**.


7. xbb-validation-FTAG*

- Validation scripts for this model.




