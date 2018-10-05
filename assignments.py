#!/usr/bin/env python
import pandas
from pathlib import Path
from matplotlib.pyplot import show, figure
from argparse import ArgumentParser
from matplotlib.ticker import MaxNLocator
import seaborn as sns
sns.set_context('talk')

MINTEAM = 5

def main():
    p = ArgumentParser()
    p.add_argument('assignfn')
    p = p.parse_args()

    assignments = pandas.read_excel(Path(p.assignfn).expanduser(), usecols="D:E")
    projects = pandas.unique(assignments['PROJECT'].dropna(0,how='any').values.ravel()).tolist()

    assignments.dropna(0, how='any', inplace=True)
    teams = pandas.DataFrame(index=projects, columns=range(6))

    for proj in projects:
        ind = assignments['PROJECT'].str.match(proj)
        members = assignments.loc[ind, 'Email'].values
        teams.loc[proj, 'count'] = members.size
        teams.loc[proj, range(members.size)] = members

# %% plots
    ax = figure().gca()
    teams['count'].plot.bar()
    ax.set_title('2018 team counts')

    show()


if __name__ == '__main__':
    main()
