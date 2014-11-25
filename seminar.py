#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function
import pandas as pd
from os.path import expanduser, splitext
from easygui import fileopenbox
#from pdb import set_trace

'''Michael Hirsch 2014
analyses Blackboard Grading Center results
'''

def analyzeForms(fn,name,email):
    pd.options.display.max_colwidth=17
    ext = splitext(fn)[1]
    if ext == '.xls' or ext == '.xlsx':
        data = pd.read_excel(expanduser(fn))
    elif ext == '.csv':
        data = pd.read_csv(expanduser(fn))

    semrep(data,name,email)

    return data

def semrep(data,name,email):
    ''' have to find seminar index from Blackboard data file (don't count on position!)'''
    semcol = data.columns.values.tolist().index('Seminar Attendance')
    #numeach = data.ix[:,3:].sum(axis=1,numeric_only=True) #old per seminar spreadsheet
    nosem = data.ix[:,semcol]==0
    onesem = data.ix[:,semcol]==1
    twosem = data.ix[:,semcol]==2

    sep = email+'; '

    if name:
        di = ['﻿"Last Name"','First Name']

        print("NO seminars:",nosem.sum()) #(numeach==0).sum())
        print(data.ix[nosem,di].values,sep=';')

        print('one seminar:',onesem.sum())
        print(data.ix[onesem,di].values,sep=';')

        print('two seminars:',twosem.sum())
        print(data.ix[twosem,di].values,sep=';')
    else: #email
        di = 2
        print("NO seminars:",nosem.sum()) #numeach.isnull().sum() )
        print(*data.ix[nosem,di].tolist(),sep=sep)

        print("one seminar:",onesem.sum())
        print(*data.ix[onesem,di].tolist(),sep=sep)

        print('two seminars:',twosem.sum())
        print(*data.ix[twosem,di].tolist(),sep=sep)



if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='Analyzes Blackboard Learn statistics')
    p.add_argument('infile',help='.xls filename',type=str,nargs='?',default=None)
    p.add_argument('--name',help='print name instead of email',action='store_true')
    p.add_argument('-e','--email',help='text to append to end of username to make complete email address',default='',type=str)
    ar = p.parse_args()

    if ar.infile is None:
        fn = fileopenbox('select seminar file',default='*.csv')
    else:
        fn = ar.infile


    analyzeForms(fn,ar.name,ar.email)
