#!/bin/bash

python prepare_data.py 500 $1 $2 $3
cd ner_module &&  python pipeline/sentence_pipe.py  --conf pipeline/settings.py -f ../input/corpus.txt -l INFO && cd -
