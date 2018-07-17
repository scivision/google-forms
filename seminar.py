#!/usr/bin/env python
from pathlib import Path
import pandas as pd

pd.options.display.max_colwidth = 17
'''Michael Hirsch 2014
analyses Blackboard Grading Center results
'''


def analyzeForms(fn: Path, name, email):
    fn = Path(fn).expanduser()

    ext = fn.suffix
    if ext in ('.xls', '.xlsx'):
        data = pd.read_excel(fn)
    elif ext == '.csv':
        data = pd.read_csv(fn)

    semrep(data, name, email)

    return data


def semrep(data, name, email):
    ''' have to find seminar index from Blackboard data file (don't count on position!)'''
    semcol = data.columns.values.tolist().index('Seminar Attendance')
    # numeach = data.ix[:,3:].sum(axis=1,numeric_only=True) #old per seminar spreadsheet
    nosem = data.ix[:, semcol] == 0
    onesem = data.ix[:, semcol] == 1
    twosem = data.ix[:, semcol] == 2

    sep = email+'; '

    if name:
        di = ['﻿"Last Name"', 'First Name']

        print("NO seminars:", nosem.sum())  # (numeach==0).sum())
        print(data.ix[nosem, di].values, sep=';')

        print('one seminar:', onesem.sum())
        print(data.ix[onesem, di].values, sep=';')

        print('two seminars:', twosem.sum())
        print(data.ix[twosem, di].values, sep=';')
    else:  # email
        di = 2
        print("NO seminars:", nosem.sum())  # numeach.isnull().sum() )
        print(*data.ix[nosem, di].tolist(), sep=sep)

        print("one seminar:", onesem.sum())
        print(*data.ix[onesem, di].tolist(), sep=sep)

        print('two seminars:', twosem.sum())
        print(*data.ix[twosem, di].tolist(), sep=sep)


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='Analyzes Blackboard Learn statistics')
    p.add_argument('infile', help='.xls filename')
    p.add_argument('--name', help='print name instead of email', action='store_true')
    p.add_argument('-e', '--email', help='text to append to end of username to make complete email address', default='')
    p = p.parse_args()

    fn = p.infile

    analyzeForms(fn, p.name, p.email)
