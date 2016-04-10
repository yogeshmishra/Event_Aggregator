#!/bin/bash

python prepare_data.py 500 $1 $2 $3
python createBroadCategory.py
python update_es_section.py
cd ner &&  python pipeline/sentence_pipe.py  --conf pipeline/settings.py -f ../input/corpus.txt -l INFO && cd -
