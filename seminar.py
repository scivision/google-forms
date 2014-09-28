#!/usr/bin/env python3
import pandas as pd
from os.path import expanduser
'''Michael Hirsch 2014
'''

def analyzeForms(xlsfn):
    pd.options.display.max_colwidth=17

    data = pd.read_excel(expanduser(xlsfn))

    numeach = data.ix[:,2:].sum(axis=1,numeric_only=True)

    numone = (numeach==1).sum()
    numtwo = (numeach==2).sum()
    print(numone)
    print(numtwo)

    return data



if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='Analyzes attendance statistics')
    p.add_argument('-i','--infile',help='.xls filename',type=str,required=True)
    ar = p.parse_args()

    data = analyzeForms(ar.infile)
