import pandas as pd

# Load the two Excel files
file1_path = "top_pairs_60_days_2023-07-21_to_2023-09-19.xlsx"
file2_path = "top_pairs_180_days_2023-03-23_to_2023-09-19.xlsx"
# file3_path = "top_pairs_365_days_2022-09-19_to_2023-09-19.xlsx"

df1 = pd.read_excel(file1_path)
df2 = pd.read_excel(file2_path)
# df3 = pd.read_excel(file3_path)

# Merge the dataframes based on common Stock 1 and Stock 2
common_stocks = pd.merge(df1, df2, on=["Stock 1", "Stock 2"], how="inner")
# common_stocks = pd.merge(common_stocks, df3, on=["Stock 1", "Stock 2"], how="inner")

# Create a new dataframe with the desired columns
new_columns = [
    "Stock 1",
    "Sector_Stock1_x",
    "Stock 2",
    "Sector_Stock2_x",
    "Correlation_x",
    "Correlation_y",
    # "Correlation",
    "p_value_x",
    "p_value_y",
    # "p_value"
]

new_df = common_stocks[new_columns]

# Rename the columns to remove "_x" and "_y" suffixes
new_df.columns = [
    "Stock 1",
    "Sector_Stock_1",
    "Stock 2",
    "Sector_Stock_2",
    "Correlation 2m",
    "Correlation 6m",
    # "Correlation 12m",
    "p_value 2m",
    "p_value 6m",
    # "p_value 12m"
]

# Save the new dataframe to a new Excel file
output_file = "common_stocks_09-20-2023_1.xlsx"
new_df.to_excel(output_file, index=False)
