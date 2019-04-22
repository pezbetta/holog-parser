# hosts-parser

Example of usage:
```
python hosts_parser/parser.py -i input-file-10000.txt --host Merideth --init-time 1565647388784 --end-time 1565711716008
> 1565649429591: Merideth -> Arian
> 1565687001744: Merideth -> Jaelianna
> 1565692833479: Merideth -> Monik
> 1565709819417: Merideth -> Shatarra
```

usage: parser.py [-h] -i PATH [--init-time TIME] [--end-time TIME]
                 [--host HOST] [-f] [--period SEG]

Parser a hosts log file

optional arguments:

  -h, --help            show help message and exit

  -i PATH, --input-file PATH  path to the file to parse

  --init-time TIME      time from which to look up lines in the file

  --end-time TIME       time until which to look up lines in the file

  --host HOST           host to look up for in the file

  -f, --follow          show as the file increase after each period

  --period SEG          seconds between checking the file. only works with follow
