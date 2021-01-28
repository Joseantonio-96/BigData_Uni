from pandas import read_csv, concat
from multiprocessing import Pool, cpu_count
from timeit import default_timer
import lab01_serial


def parallelize_dataframe(func, n_cores=cpu_count()):
    pool = Pool(n_cores)
    df = concat(pool.map(func, read_csv('proteins.csv', sep=';', chunksize=21000, index_col='structureId')))
    pool.close()
    return df

def search_pattern(df):
    return df['sequence'].str.count(pat)

pat = str.upper(input('Pattern: '))
start = default_timer()
occ = parallelize_dataframe(search_pattern)

print(f'Time is {default_timer()-start}')
print('No matches for the given pattern' if occ.max() < 1 else f'Protein that has the most matches has ID {occ.idxmax()} with {occ.max()} occurrences')

lab01_serial.pat_plot(occ, pat)
