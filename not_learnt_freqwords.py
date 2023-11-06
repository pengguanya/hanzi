import pandas as pd
from modules.ankitools import read_deck

df = read_deck('peng', '自学中文')
freq = pd.read_excel('data/freq_table.xlsx')
more_words = pd.read_excel('data/jida_v1v2.xlsx')

def filter_and_sort_dataframes(N, df, freq, filter_column, freq_column, sort_key, output_columns):
    """
    Filters and sorts dataframes based on specified conditions.
    
    Parameters:
        N (int): Number of top characters to retrieve.
        df (pd.DataFrame): Dataframe containing the main data.
        freq (pd.DataFrame): Dataframe containing frequency data.
        filter_column (str): Column name to be used for filtering.
        sort_key (str): Column name to be used for sorting.
        output_columns (list): List of column names for the final output.
    
    Returns:
        pd.DataFrame: Resulting dataframe with specified columns.
    """
    # Get the set of values in the filter_column
    filter_values = set(df[filter_column])
    
    # Filter the freq dataframe to exclude values present in filter_column
    filtered_freq = freq[~freq[freq_column].isin(filter_values)]
    
    # Sort the filtered_freq dataframe by sort_key in descending order
    sorted_filtered_freq = filtered_freq.sort_values(by=sort_key, ascending=False)
    
    # Select the top N rows from the sorted_filtered_freq dataframe
    top_N_values = sorted_filtered_freq.head(N)
    
    # Create the resulting dataframe with desired columns
    result_df = top_N_values[output_columns]
    
    return result_df

def append_unique_non_existing_to_nfld_front(df, more_words):
    """
    Appends unique non-existing values from the first column of 'more_words' to the 'nfld_Front' column in 'df'.
    
    Parameters:
        df (pd.DataFrame): Main dataframe.
        more_words (pd.DataFrame): DataFrame containing additional words (2 columns).
    
    Returns:
        pd.DataFrame: Updated dataframe with unique non-existing values appended to 'nfld_Front' column.
    """
    # Make sure the 'more_words' dataframe has 2 columns
    if more_words.shape[1] != 2:
        raise ValueError("The 'more_words' dataframe should have exactly 2 columns.")
    
    # Get unique values from the first column of 'more_words'
    unique_values = more_words.iloc[:, 0].unique()
    
    # Get unique non-existing values
    unique_non_existing_values = list(set(unique_values) - set(df['nfld_Front']))
    
    # Create a new dataframe with the unique non-existing values
    new_rows = pd.DataFrame({'nfld_Front': unique_non_existing_values})
    
    # Concatenate 'df' and 'new_rows'
    updated_df = pd.concat([df, new_rows], ignore_index=True)
    
    return updated_df

# Call the function to append the values
updated_df = append_unique_non_existing_to_nfld_front(df, more_words)

# Example usage
N = 100
output_columns = ['char', 'times', 'freq', 'cumu_freq']
result_df = filter_and_sort_dataframes(N, updated_df, freq, 'nfld_Front', 'char', 'times', output_columns)
print(result_df)


# Write the result to an Excel file
output_path = 'data/notlearnt_freqwords.xlsx'
result_df.to_excel(output_path, index=False)


