#!/usr/bin/env bash

rm results.txt

makeElseClearDir () {
    if [ ! -d $1$2 ]
    then
        mkdir $1$2
    else
        rm -rf $1$2
        mkdir $1$2
    fi
}

TESTDIR="testdir/*"

for methodDir in $TESTDIR
do
    echo $methodDir >> results.txt
    for pairDir in "$methodDir/*"
    do
        for ((i=0; i<10; i++))
        do  
            dirList=($pairDir)
            echo ho ${dirList}
            echo he ${dirList[$i]}
            echo hi "${dirList[$i]}/1.png" hi
            filenames="${dirList[$i]}/1.png ${dirList[$i]}/2.png"
            echo ${dirList[$i]} >> results.txt
            
            makeElseClearDir ${dirList[$i]} "/METHOD1"
            makeElseClearDir ${dirList[$i]} "/METHOD2"
            makeElseClearDir ${dirList[$i]} "/METHOD3"
            makeElseClearDir ${dirList[$i]} "/METHOD4"

            echo FILENAMES $filenames
            echo PAIRDIR ${dirList[$i]}

            SAVEFLAG=0
            if [[ $1 -eq "-s" ]]
            then
                SAVEFLAG=1
            fi

            echo $methodDir ${dirList[$i]} "METHOD1" >> results.txt
            { time python method1.py $filenames ${dirList[$i]} $SAVEFLAG ; } 2>> results.txt

            echo $methodDir ${dirList[$i]} "METHOD2" >> results.txt
            { time python method2.py $filenames ${dirList[$i]} $SAVEFLAG ; } 2>> results.txt

            echo $methodDir ${dirList[$i]} "METHOD3" >> results.txt
            { time python method3.py $filenames ${dirList[$i]} $SAVEFLAG ; } 2>> results.txt

            echo $methodDir ${dirList[$i]} "METHOD4" >> results.txt
            { time python method4.py $filenames ${dirList[$i]} $SAVEFLAG ; } 2>> results.txt

            #/usr/bin/time -o results.txt python photoDiffFinder.py $filenames $subdir
        done
    done
done