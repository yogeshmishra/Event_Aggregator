#!/bin/bash
if [ $# -ne 4 ]
  then
    echo "USAGE: \n ./run.sh <YEAR> <MONTH [01-12]> <DAY[01-31]> <SECTION [refer section file]>"
fi
rm -rf input/*
python get_section_data.py 500 $1 $2 $3 
python createBroadCategory.py
python update_es_section.py
python prepare_data.py 500 $1 $2 $3 $4
cd ner &&  python pipeline/sentence_pipe.py  --conf pipeline/settings.py -f ../input/corpus.txt -l INFO && cd -



## COPY generated files to data folder 
mkdir -p ../data
cp input/*.txt ../data/

