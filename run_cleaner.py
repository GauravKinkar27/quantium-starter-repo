import os
import pandas as pd

DATA_DIR = "./data"
OUTPUT_FILE = "./formatted_output.csv"
dfs = []

print("--- RUNNING TRIPLE-CHECKED DATA CLEANER ---")

for filename in os.listdir(DATA_DIR):
    if filename.endswith(".csv"):
        file_path = os.path.join(DATA_DIR, filename)
        print(f"Processing: {file_path}")

        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip()

        # Filter for Pink Morsel immediately
        df = df[df["product"].str.strip().str.lower() == "pink morsel"].copy()

        # Strip spaces and wipe out the dollar sign safely
        df["price"] = df["price"].astype(str).str.replace("$", "", regex=False).str.strip()
        
        # Safely convert to numbers
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

        # Drop invalid rows and calculate total sales
        df = df.dropna(subset=["price", "quantity"])
        df["sales"] = df["quantity"] * df["price"]

        # Keep only the requested fields
        df = df[["sales", "date", "region"]]
        dfs.append(df)

if dfs:
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df = combined_df.sort_values(by="date")
    combined_df.to_csv(OUTPUT_FILE, index=False)
    
    print("\n--- Success! Done! ---")
    print(f"File created: {OUTPUT_FILE}")
    print(f"Total Rows: {len(combined_df)}")
else:
    print("\nNo data folders or CSV files found.")