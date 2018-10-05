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
    p.add_argument('fn')
    p = p.parse_args()

    fn = Path(p.fn).expanduser()

    choices = pandas.read_excel(fn, usecols="R:T")
    projects = pandas.unique(choices.values.ravel())

    picks = pandas.DataFrame(index=projects, columns=choices.columns)
    for proj in projects:
        for c in choices:
            picks.loc[proj, c] = choices[c].str.match(proj).sum()

    popularity = picks.sum(axis=1).sort_values(ascending=False)

    rejected = popularity.index.values[popularity < MINTEAM]
    print('rejected:')
    print(rejected)

    # picks = picks[picks > MINTEAM]
    picks.sort_values(' [1st Choice]', inplace=True, ascending=False)

# %% plots
    fg = figure()
    ax = fg.gca()
    popularity.plot.bar(ax=ax)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.axhline(4, color='red', linestyle='--')
    ax.set_title('Overall selections (1st + 2nd + 3rd)')
    fg.tight_layout()

    fg = figure()
    axs = fg.subplots(picks.shape[1], 1, sharex=True, sharey=True)
    for ax, c in zip(axs, picks):
        picks[c].plot.bar(ax=ax)
        ax.set_title(c)
        ax.axhline(4, color='red', linestyle='--')
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))


    show()


if __name__ == '__main__':
    main()
