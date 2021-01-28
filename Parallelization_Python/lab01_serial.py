from pandas import read_csv
import matplotlib.pyplot as plt
from timeit import default_timer


def pat_plot(s, pattern):
    s.plot(title=f'Occurrences of the Pattern {pattern} per Protein').set(xlabel="Protein ID", ylabel="Amount of occurences")
    plt.show()

if __name__ == "__main__":
    # Ask the user to give a pattern string and capitalize it
    pat = str.upper(input('Pattern: '))

    # Start timing after receiving the pattern
    start = default_timer()

    # Load data to pandas dataframe
    df = read_csv('proteins.csv', sep=';', index_col='structureId')

    # Count occurences of pattern per row in the sequence column
    occ = df['sequence'].str.count(pat)

    # Calculate time difference and print protein with max occurences
    print(f'Time is {default_timer() - start}')
    print('No matches for the given pattern' if occ.max() < 1 else f'Protein that has the most matches has ID {occ.idxmax()} with {occ.max()} occurrences')

    # Plot the amount of occurences of pattern per protein ID
    pat_plot(occ, pat)
