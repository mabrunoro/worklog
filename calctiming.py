#!/usr/bin/env python3
import sys
import os
import datetime
import json
import argparse
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import Terminal256Formatter


def sstrip(s):
    return s.rstrip().lstrip()


def tempo(t):
    te = t.split(' ')[-1]
    return datetime.datetime.strptime(te, '%H:%M')


def main(filename, last=True, description=True):
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
    return ret

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
    parser.add_argument('--summarized','-s',help='No description, short version.')
    parser.add_argument('--sort','-k',help='Sort tasks on Output.')
    parser.add_argument('--file','-f',help=FILEHELPER)
    parser.add_argument('--nocolor','-n',help='No colored output.')
    args = parser.parse_args()
    filename = sys.argv[1] if len(sys.argv) > 1 else f'{os.path.dirname(__file__)}/TIMING.md'
    description = args.summarized is None
    sort_keys = args.sort is not None
    colored = args.nocolor is None
    m = main(filename=filename, description=description)
    json_str = json.dumps(m, indent=4, sort_keys=sort_keys)

    if(colored):
        print(highlight(json_str, JsonLexer(), Terminal256Formatter(style='monokai')))
    else:
        print(json_str)
