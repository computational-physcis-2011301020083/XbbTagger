#path="../Data/Hbb/"
path="../Data/Top/"
for i in $(ls $path)
do
python predict2.py --path $path$i
done



