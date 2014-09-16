#!/usr/bin/env python3
import pandas as pd
from os.path import expanduser
'''Michael Hirsch 2014
Ref:
http://stackoverflow.com/questions/22093006/python-pandas-filter-dataframe-by-applying-regular-expression
http://pandas.pydata.org/pandas-docs/version/0.8.1/missing_data.html
'''

def analyzeForms(xlsfn,mplots,pick,full):
    pd.options.display.max_colwidth=17

    xlsfn = expanduser(xlsfn)
    data = pd.read_excel(xlsfn)

    #this can be looped in a smarter way, but just for clarity...
    rechoice(data,pick[0],'choice one',full)
    rechoice(data,pick[1],'choice two',full)
    rechoice(data,pick[2],'choice three',full)

    return data

def rechoice(data,choice,choicenum,full):
    if choice is not None:
        dsl = data[ data[choicenum].str.contains(choice).fillna(False) ]
        nsl = dsl.shape[0]
        print(str(nsl) + ' students chose ' + choice + ' as ' + choicenum)
        if full:
            print(dsl.ix[:,1:].to_string(justify='left'))
        else:
            print(dsl.ix[:,1:3].to_string(justify='left'))

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='Loads Google Forms responses XLS and analyses')
    p.add_argument('-i','--infile',help='.xls filename with Google Forms responses',type=str,required=True)
    p.add_argument('-p','--plot',help='list plots you want made',nargs='+',default=[None],type=str)
    p.add_argument('--profile',help='profile performance',action='store_true')
    p.add_argument('--p1',help='list who picked for project one this project choice',type=str,default=None)
    p.add_argument('--p2',help='list who picked for project two this project choice',type=str,default=None)
    p.add_argument('--p3',help='list who picked for project three this project choice',type=str,default=None)
    p.add_argument('--full',help='print maximum amount of detail about respondant',action='store_true')

    ar = p.parse_args()
    pick = [ar.p1, ar.p2, ar.p3]

    if ar.profile:
        import cProfile
        from readprofiler import goCprofile
        profFN = 'analyzeforms.pstats'
        print('saving profile results to ' + profFN)
        cProfile.run('analyzeForms(ar.infile,ar.plot, pick,ar.full)',profFN)
        goCprofile(profFN)
    else:
        data = analyzeForms(ar.infile, ar.plot, pick,ar.full)
        #print(data)