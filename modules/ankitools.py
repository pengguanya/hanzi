import os
import pandas as pd
from ankipandas import Collection

def read_deck(user: str, deck_name: str) -> pd.DataFrame:
    anki_path = os.path.join(os.getenv('APPDATA'), 'Anki2')
    col = Collection(anki_path, user=user)

    # Get all cards from a specific deck
    cards_df = col.cards.query(f"cdeck == '{deck_name}'")

    # Get all notes from the collection
    notes_df = col.notes.fields_as_columns()

    # Join the notes and cards dataframes on the 'nid' column
    df = pd.merge(cards_df, notes_df, on="nid")
    
    return df