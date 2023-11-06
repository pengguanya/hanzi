import pandas as pd

relearn = pd.read_excel('data/relearn.xlsx')
freq = pd.read_excel('data/freq_table.xlsx')

relearn_freq = pd.merge(relearn, freq, on='char', how='left')
relearn_freq = relearn_freq[['char', 'times', 'freq', 'cumu_freq']]
relearn_freq = relearn_freq.sort_values(by = 'freq', ascending=True)

# load anki list
from ankipandas import Collection
import os
anki_path = os.path.join(os.getenv('APPDATA'), 'Anki2')
col = Collection(anki_path, user='peng')

# Get all cards from a specific deck
deck_name = "自学中文"
cards_df = col.cards.query(f"cdeck == '{deck_name}'")

# Get all notes from the collection
notes_df = col.notes.fields_as_columns()

# Join the notes and cards dataframes on the 'nid' column
df = pd.merge(cards_df, notes_df, on="nid")

# Sort the freq DataFrame in ascending order by the 'freq' column and select the top 500 rows
top_500_freq = freq.sort_values(by='times', ascending=False).head(500)

# Find rows where 'char' values do not appear in 'nfld_Front' column of the df DataFrame
result = top_500_freq[~top_500_freq['char'].isin(df['nfld_Front'])][['char', 'times', 'freq', 'cumu_freq']]

result.to_excel('data/freq_not_in_anki.xlsx', index=False, header=True)
