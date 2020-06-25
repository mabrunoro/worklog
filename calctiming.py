#!/usr/bin/env python3
import sys
import os
import datetime
import json
import argparse
import pygments
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import Terminal256Formatter


def sstrip(s):
    return s.rstrip().lstrip()


def tempo(t):
    te = t.split(' ')[-1]
    return datetime.datetime.strptime(te, '%H:%M')


def main(filename, last=True, description=True):
    day = None
    with open(filename) as f:
        lines = f.readlines()
        last_issue = []
        ret = {}
        start = 0
        for i in lines:
            line = sstrip(i)
            if(len(line) > 0):
                if(line[0] == '#'):  # new day
                    day = sstrip(line[1:])
                    ret[day] = {}
                    start = 0
                else:   # worklog
                    a = [sstrip(j) for j in line.split('--')]   # parse task line
                    if(len(a) > 1):
                        if((a[-1] not in ret[day]) and (a[-1] != '')):  # include new task in dict
                            ret[day][a[-1]] = {'time-spent':'0:00'}
                            if(description and (len(a) == 3)):  # if the array has length 3, then a description was provided
                                ret[day][a[-1]]['description'] = []
                        if(start > 0):  # if the file reading has not just started
                            ret[day][last_issue[-1]]['time-spent'] = (tempo(ret[day][last_issue[-1]]['time-spent']) + (tempo(a[0]) - tempo(last_issue[0]))).strftime('%H:%M')
                            if(description and (len(last_issue) == 3)):  # include description if it's enabled and avoid duplicates
                                if('description' not in ret[day][last_issue[-1]]):
                                    ret[day][last_issue[-1]]['description'] = []
                                if(last_issue[1] not in ret[day][last_issue[-1]]['description']):
                                    ret[day][last_issue[-1]]['description'].append(last_issue[1])
                        last_issue = a
                        start = + 1
    return {day:ret[day]} if last else ret

FILEHELPER = """Input file. A valid file will be something like:
# 18-06-20
07:52 -- DESCRIPTION 0 -- TASK 0
08:53 -- TASK 1
09:23 -- TASK 0
11:15 -- DESCRIPTION 1 -- TASK 2
12:01 -- lunch
14:29 -- DESCRIPTION 2 -- TASK 1
15:13 -- DESCRIPTION 3 -- TASK 0
15:28 -- DESCRIPTION 4 -- TASK 3
16:10 -- TASK 0
16:23 -- snack
17:15 -- TASK 3
18:59 -- DESCRIPTION 5 -- TASK 4
19:59 --

Markdown listing is also allowed:
# 19-06-20
- 08:55 -- DESCRIPTION 0 -- TASK 0
- 11:10 -- TASK 1
- 13:08 -- lunch
- 14:22 -- DESCRIPTION 2 -- TASK 0
- 16:39 -- TASK 3
- 16:54 -- DESCRIPTION 4 -- TASK 1
- 18:35 --"""

if(__name__ == "__main__"):
    parser = argparse.ArgumentParser(description='Daily worklog computing.', usage='use "%(prog)s --help" for more information', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-s','--summarized',help='No descriptions, short version.', action='store_true')
    parser.add_argument('-k','--sortkeys',help='Sort tasks on Output.', action='store_true')
    parser.add_argument('-f','--file',help=FILEHELPER)
    parser.add_argument('-n','--nocolor',help='No colored output.', action='store_true')
    parser.add_argument('-l','--lastday',help='Print only last day worklog.', action='store_true')
    
    args = parser.parse_args()
    print(args)
    filename = args.file if args.file is not None else f'{os.path.dirname(__file__)}/TIMING.md'
    description = not args.summarized
    sort_keys = args.sort
    nocolored = args.nocolor
    lastday = args.lastday
    m = main(filename=filename, last=lastday, description=description)
    json_str = json.dumps(m, indent=4, sort_keys=sort_keys)

    if(nocolored):
        print(json_str)
    else:
        print(highlight(json_str, JsonLexer(), Terminal256Formatter(style='monokai')))

# STYLES = [
#     'default',
#     'emacs'   ,
#     'friendly',
#     'colorful',
#     'autumn'  ,
#     'murphy'  ,
#     'manni'   ,
#     'monokai' ,
#     'perldoc' ,
#     'pastie'  ,
#     'borland' ,
#     'trac'    ,
#     'native'  ,
#     'fruity'  ,
#     'bw'      ,
#     'vim'     ,
#     'vs'      ,
#     'tango'   ,
#     'rrt'     ,
#     'xcode'   ,
#     'igor'    ,
#     'paraiso-light',
#     'paraiso-dark',
#     'lovelace',
#     'algol'   ,
#     'algol_nu',
#     'arduino' ,
#     'rainbow_dash',
#     'abap'    ,
#     'solarized-dark',
#     'solarized-light',
#     'sas'        ,
#     'stata'      ,
#     'stata-light',
#     'stata-dark'
# ]
