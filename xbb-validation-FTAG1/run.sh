#:<<!
for i in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 
do
python reduceTop.py --path $i
done

python reduceHiggs.py --path 0
for i in 0 1 2 3 4
do
python reduceQCD.py --path $i
done

#!
:<<!
p="./Reduced/Merge/"
for i in $(ls ./Reduced/Merge/)
do
python convert.py --path $p$i
done
!
