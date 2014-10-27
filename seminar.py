#!/usr/bin/env python3
import pandas as pd
from os.path import expanduser
'''Michael Hirsch 2014
'''

def analyzeForms(xlsfn):
    pd.options.display.max_colwidth=17

    data = pd.read_excel(expanduser(xlsfn))

    semrep(data)

    return data

def semrep(data):
    numeach = data.ix[:,3:].sum(axis=1,numeric_only=True)



    print("students who have attended NO seminars yet: " + str(numeach.isnull().sum()))
    print(*data.ix[numeach.isnull(),2].tolist(),sep=';')
    print('------------------------------')


    print('students that attended exactly one seminar: ' + str((numeach==1).sum()))
    print(*data.ix[numeach==1,2].tolist(),sep=';')
    print('------------------------------')

    print('students that attended exactly two seminars: ' + str((numeach==2).sum()))
    print(*data.ix[numeach==2,2].tolist(),sep=';')
    print('------------------------------')



if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='Analyzes attendance statistics')
    p.add_argument('infile',help='.xls filename',type=str)
    ar = p.parse_args()

    data = analyzeForms(ar.infile)
