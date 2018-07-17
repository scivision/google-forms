#!/usr/bin/env python
"""Historgram of Blackboard grades"""
from pathlib import Path
import pandas as pd
import numpy as np
from matplotlib.pyplot import show, figure


def main(fn: Path, assignment: str, minmax: list):
    fn = Path(fn).expanduser()

    dat = pd.read_csv(fn)
    dasg = dat[assignment].dropna()

    if minmax is not None:
        dasg.clip(minmax[0], minmax[1], inplace=True)

# %%
    ax = figure().gca()
    ptile = [10, 25, 75, 90]
    prc = np.percentile(dasg, ptile)
    dasg.hist(ax=ax, bins=32)
    ax.axvline(dasg.median(), color='red', linestyle='--', label='median')
    ax.axvline(dasg.mean(), color='magenta', linestyle='--', label='mean')
    for p, pt in zip(prc, ptile):
        ax.axvline(p, color='black', linestyle='--', label=f'{pt}th')
    ax.legend(loc='best')
    ax.set_title(f'{fn.stem} {assignment}, N={dasg.shape[0]}')

    return dasg


if __name__ == "__main__":
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('fn', help='.csv file exported from Full Grade Center')
    p.add_argument('assignment', help='column to plot')
    p.add_argument('course', help='course name', nargs='?', default='')
    p.add_argument('-k', '--minmax', help='discard <>', nargs=2, type=float)
    p = p.parse_args()

    fn = Path(p.fn).expanduser()

    if p.course:
        pat = f'{p.course}_*.csv'
    else:
        pat = '*.csv'

    if fn.is_dir():
        flist = sorted(fn.glob(pat))
    else:
        flist = [fn]

    # naming convention  COURSE_YEAR.csv
    years = [f.stem.split('_')[1] for f in flist]

    stats = pd.DataFrame(index=years,
                         columns=['median', 'mean'])
    for f, y in zip(flist, years):
        dasg = main(f, p.assignment, p.minmax)
        prc = np.percentile(dasg, [10, 25, 75, 90])
        stats.at[y, '10th'] = prc[0]
        stats.at[y, '25th'] = prc[1]
        stats.at[y, '75th'] = prc[2]
        stats.at[y, '90th'] = prc[3]
        stats.at[y, 'median'] = dasg.median()
        stats.at[y, 'mean'] = dasg.mean()

    ax = figure().gca()
    stats.plot(ax=ax)
    ax.set_xlabel('year')
    ax.set_title(f'{p.course} {p.assignment}')
    ax.axhline(12, linestyle='-.', color='grey')
    ax.set_ylabel('score')

    show()
