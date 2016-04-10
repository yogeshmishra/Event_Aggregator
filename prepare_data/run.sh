#!/bin/bash
rm -rf input/*
python get_section_data.py 500 $1 $2 $3 $4
python createBroadCategory.py
python update_es_section.py
python prepare_data.py 500 $1 $2 $3 $4
cd ner &&  python pipeline/sentence_pipe.py  --conf pipeline/settings.py -f ../input/corpus.txt -l INFO && cd -



## COPY generated files to data folder 
mkdir -p ../data
cp input/corpus.txt ../data/
cp input/enriched_keys.txt ../data/
cp input/ids.txt ../data/
cp input/locations.txt ../data/
cp input/non_ners.txt ../data/
cp input/persons.txt ../data/
