#!/usr/bin/env python3
import pandas as pd
from os.path import expanduser
from numpy import s_
from pdb import set_trace
'''Michael Hirsch 2014
'''

def analyzeForms(xlsfn,name):
    pd.options.display.max_colwidth=17

    data = pd.read_excel(expanduser(xlsfn))

    semrep(data,name)

    return data

def semrep(data,name):

    numeach = data.ix[:,3:].sum(axis=1,numeric_only=True)
    if name:
        di = s_[:2]
       # set_trace()
        print("NO seminars:",numeach.isnull().sum() )
        print(data.ix[numeach.isnull(),di].values,sep=';')

        print('one seminar:',(numeach==1).sum())
        print(data.ix[numeach==1,di].values,sep=';')

        print('two seminars:',(numeach==2).sum())
        print(data.ix[numeach==2,di].values,sep=';')
    else: #email
        di = 2
        print("NO seminars:",numeach.isnull().sum() )
        print(*data.ix[numeach.isnull(),di].tolist(),sep=';')

        print('one seminar:',(numeach==1).sum())
        print(*data.ix[numeach==1,di].tolist(),sep=';')

        print('two seminars:',(numeach==2).sum())
        print(*data.ix[numeach==2,di].tolist(),sep=';')



if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='Analyzes attendance statistics')
    p.add_argument('infile',help='.xls filename',type=str)
    p.add_argument('--name',help='print name instead of email',action='store_true')
    ar = p.parse_args()

    data = analyzeForms(ar.infile,ar.name)
