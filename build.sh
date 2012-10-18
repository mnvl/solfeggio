#! /bin/sh

set -e
set -x

rm -f *.mid *.wav *.mp3
python solfeggio.py

for i in `ls *.mid`;
do
    w=`echo $i | sed 's/.mid/.wav/i'`
    /cygdrive/c/timidity/timidity.exe --volume=400 -OwM1 -c c:/timidity/freepats/timidity.cfg $i -o $w

    m=`echo $i | sed 's/.mid/.mp3/i'`
    lame --preset standard $w $m

    rm $w
done
