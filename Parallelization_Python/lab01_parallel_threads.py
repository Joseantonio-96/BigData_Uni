from threading import Thread
import pandas as pd
import sys
from timeit import default_timer
import lab01_serial


def loop(j, func):
    for f in func:
        for i in j:
            f(i)


def thread_search(pattern, n_threads):
    out_list = []
    jobs = [Thread(target=search_pattern, args=(i, pattern, out_list)) for i in pd.read_csv('proteins.csv', sep=';', chunksize=250000//n_threads, index_col='structureId')]
    loop(jobs, [Thread.start, Thread.join])
    return pd.concat(out_list)


def search_pattern(df, pattern, out_list):
    out_list.append(df['sequence'].str.count(pattern))


pat = str.upper(input('Pattern: '))
start = default_timer()
occ = thread_search(pat, int(sys.argv[1]) if len(sys.argv) > 1 else 10)

print(f'Time is {default_timer() - start}')
print('No matches for the given pattern' if occ.max() < 1 else f'Protein that has the most matches has ID {occ.idxmax()} with {occ.max()} occurrences')

lab01_serial.pat_plot(occ, pat)
