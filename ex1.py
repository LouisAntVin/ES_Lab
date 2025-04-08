import pandas as pd

def load_data(stock_file, sales_file):
    stock_data = pd.read_csv(stock_file)
    sales_data = pd.read_csv(sales_file)
    return stock_data, sales_data

def analyze_inventory(stock_data, sales_data, threshold=10):

    merged_df = pd.merge(stock_data, sales_data, on="Product ID", how="left")

    # Fill NaN values in Quantity Sold with 0
    merged_df["Quantity Sold"] = merged_df["Quantity Sold"].fillna(0)

    # Calculate the remaining stock
    merged_df["Remaining Stock"] = merged_df["Current Stock"] - merged_df["Quantity Sold"]

    # Identify products needing restock and suggest quantities
    merged_df["Restock Needed"] = merged_df["Remaining Stock"] < threshold
    merged_df["Suggested Restock Quantity"] = merged_df["Remaining Stock"].apply(
        lambda x: 50 - x if x < threshold else 0
    )
    # Filter products that need restocking
    restock_df = merged_df[merged_df["Restock Needed"]]
    print(restock_df)
    return restock_df[["Product ID", "Product Name", "Remaining Stock", "Suggested Restock Quantity"]]

def main():
    stock_file = 'stock.csv'
    sales_file = 'sales.csv'
    output_file = 'restock_recommendations.csv'

    stock_data, sales_data = load_data(stock_file, sales_file)
    recommendations = analyze_inventory(stock_data, sales_data)

    print("Products that need restocking:")
    print(recommendations)

    recommendations.to_csv(output_file, index=False)
    print(f"Recommendations saved to {output_file}")

if __name__ == "__main__":
    main()
