import argparse
import pandas as pd #WAITING TO CORRECT ERROR

from packages.acquire import getting_data
from packages.wrangle import cleaning_data
from packages.analize import enriching_data
from packages.repor import plotting_data

### ONLY UNTIL I CAN BE ABLE TO SOLVE THE ERROR
file_name = 'CristopherRL.db'

def main():

    #raw_data = getting_data(file_name)
    #print(raw_data.head(5))

    ### ONLY UNTIL I CAN BE ABLE TO SOLVE THE ERROR
    raw_data = pd.read_csv('data/raw/raw_data.csv', sep='|')

    proc_data = cleaning_data(raw_data)

    table,top = enriching_data(proc_data)

    plotting_data(table,top)

if __name__ == "__main__":
    main()
