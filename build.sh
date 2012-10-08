#! /bin/sh

set -e
set -x

rm -f *.mid
python solfeggio.py

for i in `ls *.mid`;
do
    w=`echo $i | sed 's/.mid/.wav/i'`
    rm -f $w
    /cygdrive/c/timidity/timidity.exe -OwM1 -c c:/timidity/freepats/timidity.cfg $i -o $w

    m=`echo $i | sed 's/.mid/.mp3/i'`
    rm -f $m
    lame --preset extreme $w $m

    rm $w
done
