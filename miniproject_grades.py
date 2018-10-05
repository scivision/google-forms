#!/usr/bin/env python
"""
Miniproject Histograms
"""
import pandas
from pathlib import Path
from matplotlib.pyplot import figure, show
from argparse import ArgumentParser
from matplotlib.ticker import MaxNLocator
# import numpy as np

Y = 5


def main():
    p = ArgumentParser()
    p.add_argument('fn', help='path to .xlsx')
    p = p.parse_args()

    fn = Path(p.fn).expanduser()

    df = pandas.read_excel(fn, skiprows=[1], index_col=0, sheet_name='hardware', header=0,
                           usecols='A,F:Q,U')

    total = df['Total1']

    ax = figure().gca()
    total.hist(bins=24, ax=ax)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    std = total.std()
    median = total.median()

    low = median - 0.5*std
    hi = median + 0.5*std

    # prc = np.percentile(total, [10, 90])

    # for p in prc:
    #    ax.axvline(p, color='red', linestyle='--')
# %%
    ax.axvline(median, color='magenta', linestyle='--')

    ax.axvline(hi, color='red', linestyle='--')
    ax.annotate('+1/2 $\sigma$', (hi, Y), ha='center')

    ax.axvline(low, color='red', linestyle='--')
    ax.annotate('-1/2 $\sigma$', (low, Y), ha='center')

    # ax.annotate('10th', (prc[0], Y), ha='center')
    # ax.annotate('90th', (prc[1], Y), ha='center')
    ax.annotate('median', (median, Y), ha='center')
# %%
    Nbelow = (total < low).sum()
    Nok = ((low <= total) & (total < 90)).sum()
    Ngood = (total >= 90).sum()

    ax.set_title('count of teams at performance levels:\n'
                 f'below: {Nbelow}  OK: {Nok}   good: {Ngood}')

    ax.set_ylabel('Number of teams')
    ax.set_xlabel('score [%]')

    show()


if __name__ == '__main__':
    main()
