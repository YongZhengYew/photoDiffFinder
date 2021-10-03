#!/usr/bin/env bash

rm results.txt

makeElseClearDir () {
    if [ ! -d $1$2 ]
    then
        mkdir $1$2
    else
        rm $1$2/*
    fi
}

TESTDIR="testdir/*"

for methodDir in $TESTDIR
do
    echo $methodDir >> results.txt
    for pairDir in "$methodDir/*"
    do
        filenames="$pairDir/1.png $pairDir/2.png"
        echo $pairDir >> results.txt
        
        makeElseClearDir $pairDir "/METHOD1"
        makeElseClearDir $pairDir "/METHOD2"
        makeElseClearDir $pairDir "/METHOD3"

        echo $methodDir $pairDir "METHOD1" >> results.txt
        { time python ORIG_photoDiffFinder.py $filenames $pairDir ; } 2>> results.txt

        echo $methodDir $pairDir "METHOD2" >> results.txt
        { time python manySmallBoxes_photoDiffFinder.py $filenames $pairDir ; } 2>> results.txt

        echo $methodDir $pairDir "METHOD3" >> results.txt
        { time python photoDiffFinder.py $filenames $pairDir ; } 2>> results.txt
        #/usr/bin/time -o results.txt python photoDiffFinder.py $filenames $subdir
    done
done