# This is a sample Python script.
import pandas as pd
from tqdm import tqdm
from pandasgui import show

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def import_bobcatfile(filename):
    df_bobcat = pd.read_csv(filename, sep='\t')
    df_bobcat.set_index('Material', inplace=True)
    return df_bobcat

def import_quickbooksfile(filename):
    df_quick = pd.read_csv(filename, index_col='Item')
    df_updated = df_quick.copy()
    return df_updated


def update_data(row):
    pbar.update(1)
    # Check if Item name exists in Bobcats list
    if row.name in df_bobcat.index:
        # If Price is less than MSRP
        if row['Price'] < df_bobcat.loc[row.name].at['US List']:
            df_updated.loc[row.name, 'Price'] = df_bobcat.loc[row.name].at['US List']
        # If Cost is Less
        if df_bobcat.loc[row.name].at['US Dnet'] < row['Cost']:
            return df_bobcat.loc[row.name].at['US Dnet']
        # If Cost is higher
        elif df_bobcat.loc[row.name].at['US Dnet'] > row['Cost']:
            df_updated.loc[row.name, 'Price'] = row['Price'] + (df_bobcat.loc[row.name].at['US Dnet'] - row['Cost'])
            return df_bobcat.loc[row.name].at['US Dnet']
        else:
            return df_quick.loc[row.name].at['Cost']
    else:
        return df_quick.loc[row.name].at['Cost']


if __name__ == '__main__':
   df_updated = import_quickbooksfile('item_pricing.CSV')
   df_quick = df_updated.copy()
   df_bobcat = import_bobcatfile('bobcat_pricing.txt')


with tqdm(total=len(df_updated['Cost'])) as pbar:
    df_updated['Cost'] = df_updated.apply(update_data, axis=1)
    pbar.set_description(desc="Updating Records", refresh=True)

    show(df_updated, settings={'block': True})
    #df_updated.to_csv('updated.CSV')
