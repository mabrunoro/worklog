#!/usr/bin/env python3
import sys
import os
import datetime
import json
import argparse


def sstrip(s):
    return s.rstrip().lstrip()


def tempo(t):
    return datetime.datetime.strptime(t, '%H:%M')


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
                    if((a[-1] not in ret[day]) and (a[-1] != '')):  # include new task in dict
                        ret[day][a[-1]] = {'time-spent':'0:00'}
                        if(description and (len(a) == 3)):  # if the array has length 3, then a description was provided
                            ret[day][a[-1]]['description'] = []
                    if(start > 0):  # if the file reading has not just started
                        ret[day][last_issue[-1]]['time-spent'] = (tempo(ret[day][last_issue[-1]]['time-spent']) + (tempo(a[0]) - tempo(last_issue[0]))).strftime('%H:%M')
                        if(description and (len(last_issue) == 3) and (last_issue[1] not in ret[day][last_issue[-1]]['description'])):  # include description if it's enabled and avoid duplicates
                            ret[day][last_issue[-1]]['description'].append(last_issue[1])
                    last_issue = a
                    start = + 1
    return ret

SUMMARIZEHELPER = 'No description, short version.'

FILEHELPER = """Input file. Format should be something like:
            # 18-06-20
            07:52 -- changing HAPI according to GSheet -- HDM-374
            08:53 -- hotfix for custom-lis in release_31 -- HDM-370
            09:23 -- changing HAPI according to GSheet -- HDM-374
            11:15 -- creating lis-spesialitetsmappe layout -- HDM-372
            12:01 -- lunch
            14:29 -- analyzing issue -- HDM-659
            15:13 -- exporting folder -- HDM-660
            15:28 -- back to logo issue and updating Prod -- HDM-659
            16:10 -- creating lis-spesialitetsmappe layout -- HDM-372
            16:23 -- snack
            17:15 -- creating lis-spesialitetsmappe layout -- HDM-372
            18:59 -- copying partner nodes from master to draft -- NTF-545
            19:59 --
            # 19-06-20
            08:55 -- DESCRIPTION 0 -- TASK 0
            11:10 -- TASK 1
            13:08 -- lunch
            14:22 -- DESCRIPTION 2 -- TASK 0
            16:39 -- TASK 3
            16:54 -- DESCRIPTION 4 -- TASK 1
            18:35 --"""

if(__name__ == "__main__"):
    parser = argparse.ArgumentParser(description='Daily worklog computing.', usage='use "%(prog)s --help" for more information', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--summarized','-s',help=SUMMARIZEHELPER)
    parser.add_argument('--file','-f',help=FILEHELPER)
    args = parser.parse_args()
    filename = sys.argv[1] if len(sys.argv) > 1 else f'{os.path.dirname(__file__)}/TIMING.md'
    description = args.summarized is None
    m = main(filename=filename, description=description)
    print(json.dumps(m, indent=4, sort_keys=True))
