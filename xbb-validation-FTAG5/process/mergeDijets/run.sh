#Flatten Dijets samples
j=1
for i in $(ls ../../DataVRGhost/ReducedDijets/*h5)
do
	path=$i
	echo $j,$path
	python flattenDijets.py --path $path
	let j=j+1
done

#Merge Dijets samples by DSID
path="../../DataVRGhost/FlattenData/MergedDijets/"
for i in 361023 361024 361025 361026 361027 361028 361029 361030
do
	python MergeDijetsDSID.py --path $path --dsid $i
done

#Dijets subsample
for i in $(ls ../../DataVRGhost/FlattenData3a/MergedDijetsDSID/)
do
	path="../../DataVRGhost/FlattenData3a/MergedDijetsDSID/"$i
	python subsampleDijets.py --path $path
done

#Merge Dijets samples
path="../../DataVRGhost/FlattenData/ReducedDijetsDSID/"
python MergeDijets.py --path $path


