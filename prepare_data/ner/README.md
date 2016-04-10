#SpeedRead:
####Fast NER pipeline for English.



Citation
-------------------------------------
Please cite the paper when you use this code in your work:

    @InProceedings{alrfou-skiena:2012:PAPERS,
     author    = {Al-Rfou, Rami  and  Skiena, Steven},
     title     = {{S}peed{R}ead: A Fast Named Entity Recognition Pipeline},
     booktitle = {Proceedings of COLING 2012},
    month     = {December},
    year      = {2012},
    address   = {Mumbai, India},
    publisher = {The COLING 2012 Organizing Committee},
    pages     = {51--66},
    url       = {http://www.aclweb.org/anthology/C12-1004}
    }




Example
-------------------------------------


    $ python pipeline/pipe.py --conf pipeline/settings.py -f InputFile -l DEBUG

    2013-03-08 12:00:47 DEBUG pipe.py: 51 Initialization ...
    2013-03-08 12:00:52 DEBUG pipe.py: 36 Initialized the POSTagger in      5.621374 seconds
    2013-03-08 12:00:52 DEBUG util.py: 139 Memory: 675.800781, Resident: 675.941406, Stack: 0.000000
    2013-03-08 12:00:56 DEBUG pipe.py: 45 Initialized the NERTagger in      4.046353 seconds
    2013-03-08 12:00:56 DEBUG util.py: 139 Memory: 364.460938, Resident: 357.824219, Stack: 0.000000
    2013-03-08 12:00:56 DEBUG pipe.py: 54 Initialized the Taggers in        9.669022 seconds
    2013-03-08 12:00:56 DEBUG util.py: 139 Memory: 1040.261719, Resident: 1033.773438, Stack: 0.000000
    2013-03-08 12:00:56 DEBUG pipe.py: 59 Time spent building the document is 0.063158
    2013-03-08 12:00:57 DEBUG command.py: 40 Command: /media/data2/speedread/resources/lexer
    2013-03-08 12:00:57 DEBUG command.py: 41 Command executed in 1.133909 seconds
    2013-03-08 12:00:57 DEBUG tokenizer.py: 32 Converting text to unicode took 0.002948 seconds
    2013-03-08 12:00:58 DEBUG tokenizer.py: 43 Parsed output of the lexer in 0.476163 seconds
    2013-03-08 12:01:05 DEBUG pos.py: 218 POS tags calculated in 6.913627 seconds
    2013-03-08 12:01:14 DEBUG util.py: 139 Memory: 1354.402344, Resident: 1353.453125, Stack: 0.000000
    2013-03-08 12:01:14 DEBUG pipe.py: 63 Time spent processing the file is 17.986612
    2013-03-08 12:01:18 DEBUG document.py: 92 Document string representation is caculated in 3.828846 seconds
    2013-03-08 12:01:18 DEBUG pipe.py: 66 Time spent writing the file is 3.895351
    2013-03-08 12:01:18 DEBUG util.py: 139 Memory: 1395.929688, Resident: 1393.070312, Stack: 0.000000
