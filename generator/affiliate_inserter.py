import pandas as pd

def get_next_affiliate(csv_path="data/affiliate_products.csv") -> dict:
    df = pd.read_csv(csv_path)

    # Get next unused row
    unused = df[df["used"] == False]
    if unused.empty:
        # Reset if all used
        df["used"] = False
        df.to_csv(csv_path, index=False)
        df = pd.read_csv(csv_path)
        unused = df[df["used"] == False]

    row = unused.iloc[0]
    df.at[row.name, "used"] = True
    df.to_csv(csv_path, index=False)

    # Pull specific brain file (not folder)
    brain_path = row["product_brain_file"]
    with open(brain_path, "r", encoding="utf-8") as f:
        brain_text = f.read()

    return {
        "name": row["product_name"],
        "link": row["affiliate_link"],
        "brain": brain_text
    }
