#!/usr/bin/env python
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""
Given spreadsheet with:
sheets: choices, projects
choices columns: choice one, choice two, choice three

Michael Hirsch 2014
Ref:
http://stackoverflow.com/questions/22093006/python-pandas-filter-dataframe-by-applying-regular-expression
http://pandas.pydata.org/pandas-docs/version/0.8.1/missing_data.html
"""


def analyzeForms(fn: Path, req, pick: tuple) -> pd.DataFrame:
    fn = Path(fn).expanduser()

    pd.options.display.max_colwidth = 17

    data = pd.read_excel(fn, sheet_name='choices')
    projdata = pd.read_excel(fn, sheet_name='projects')

    # this can be looped in a smarter way, but just for clarity...
    rechoice(data, pick[0], 'choice one', req)
    rechoice(data, pick[1], 'choice two', req)
    rechoice(data, pick[2], 'choice three', req)

    for i, proj in enumerate(projdata['Name']):
        projdata.ix[i, 'vote1'] = (data['choice one'] == proj).sum()
        projdata.ix[i, 'vote2'] = (data['choice two'] == proj).sum()
        projdata.ix[i, 'vote3'] = (data['choice three'] == proj).sum()
# %% did students get what they wanted?
    if req.match:
        matchquery = data['assignment'][:, None] == data.ix[:, 'choice one':'choice three']  # type: ignore
        match = matchquery.sum(axis=0)
        # print(data.ix[matchquery,'Username'])
        print(matchquery)
        print(match)

    if req.totals is not None:
        print(projdata.ix[:, 1:].sort('vote' + str(req.totals), ascending=False))

    if req.pie:
        makepie(projdata, 'vote1')
        makepie(projdata, 'vote2')
        makepie(projdata, 'vote3')

    plt.show()

    return data


def rechoice(data: pd.DataFrame, choice: str, choicenum: str, req):
    if choice is not None:
        dsl = data[data[choicenum].str.contains(choice).fillna(False)]
        nsl = dsl.shape[0]
        print(nsl, 'students chose', choice, 'as', choicenum)
        if req.full:
            print(dsl.ix[:, 1:].to_string(justify='left'))
        else:
            print(dsl.ix[:, 1:3].to_string(justify='left'))


def makepie(projdata: pd.DataFrame, choice: str):
    ax = plt.figure().gca()
    # data.hist(column=['choice one'])
    # show integer totals
    projsum = sum(projdata[choice])

    def apct(p): return f'{p * (projsum / 100):.0f}'
    cmap = plt.cm.jet
    colors = cmap(np.linspace(0, 1, projdata.shape[0]))

    projdata[choice].plot(kind='pie', ax=ax, labels=projdata['Name'],
                          autopct=apct, shadow=False, colors=colors)


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='Loads Google Forms responses XLS and analyses')
    p.add_argument('infile', help='.xls filename with Google Forms responses')
    p.add_argument('--profile', help='profile performance', action='store_true')
    p.add_argument('--p1', help='list who picked for project one this project choice')
    p.add_argument('--p2', help='list who picked for project two this project choice')
    p.add_argument('--p3', help='list who picked for project three this project choice')
    p.add_argument('--full', help='print maximum amount of detail about respondant', action='store_true')
    p.add_argument('--pie', help='Pie Chart of choices', action='store_true')
    p.add_argument('--totals', help='print totals for 1,2,3 choice', type=int)
    p.add_argument('--match', help='show student assignment vs request', action='store_true')

    P = p.parse_args()
    pick = (P.p1, P.p2, P.p3)

    data = analyzeForms(P.infile, P, pick)
