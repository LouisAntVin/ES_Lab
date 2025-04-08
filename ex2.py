import csv
import pandas as pd

inventory_file = "inventory.csv"

def load_inventory():
    return pd.read_csv(inventory_file)

def save_inventory(inventory):
    inventory.to_csv(inventory_file, index=False)

def add_product():
    inventory = load_inventory()
    product_id = input("Enter Product ID: ")
    if product_id in inventory["Product ID"].values:
        print("Error: Product ID already exists.")
        return

    product_name = input("Enter Product Name: ")
    category = input("Enter Category: ")
    price = input("Enter Price: ")
    stock = input("Enter Stock: ")

    new_product = pd.DataFrame({
        "Product ID": [product_id],
        "Product Name": [product_name],
        "Category": [category],
        "Price": [price],
        "Stock": [stock],
        "Total Sales": [0]
    })

    inventory = pd.concat([inventory, new_product], ignore_index=True)
    save_inventory(inventory)
    print("Product added successfully!")

def update_product():
    inventory = load_inventory()
    product_id = int(input("Enter Product ID to update: "))

    if product_id not in inventory["Product ID"].values:
        print("Error: Product ID not found.")
        return

    field_to_update = input("Enter field to update (Product Name, Category, Price, Stock): ")
    if field_to_update not in inventory.columns:
        print("Error: Invalid field.")
        return

    new_value = input(f"Enter new value for {field_to_update}: ")

    if field_to_update == "Price":
        new_value = float(new_value)
    elif field_to_update == "Stock":
        new_value = int(new_value)

    inventory.loc[inventory["Product ID"] == product_id, field_to_update] = new_value
    save_inventory(inventory)
    print("Product updated successfully!")

def record_sale():
    inventory = load_inventory()
    product_id = int(input("Enter Product ID for sale: "))

    if product_id not in inventory["Product ID"].values:
        print("Error: Product ID not found.")
        return

    stock = inventory.loc[inventory["Product ID"] == product_id, "Stock"].astype(int).values[0]
    quantity = int(input("Enter quantity sold: "))

    if stock >= quantity:
        inventory.loc[inventory["Product ID"] == product_id, "Stock"] = stock - quantity
        inventory.loc[inventory["Product ID"] == product_id, "Total Sales"] += quantity
        save_inventory(inventory)
        print("Sale recorded successfully!")
    else:
        print("Error: Insufficient stock.")

def view_inventory():
    inventory = load_inventory()
    if not inventory.empty:
        print("\nCurrent Inventory:")
        print(inventory.to_string(index=False))
    else:
        print("Inventory is empty.")

def delete_product():
    inventory = load_inventory()
    product_id = int(input("Enter Product ID to delete: "))

    if product_id not in inventory["Product ID"].values:
        print("Error: Product ID not found.")
        return

    inventory = inventory[inventory["Product ID"] != product_id]
    save_inventory(inventory)
    print("Product deleted successfully!")

def recommend_restock():
    inventory = load_inventory()
    threshold = int(input("Enter stock threshold: "))
    low_stock = inventory[inventory["Stock"].astype(int) < threshold]
    if not low_stock.empty:
        print("\nProducts needing restocking:")
        print(low_stock.to_string(index=False))
    else:
        print("No products need restocking.")

def main_menu():
    while True:
        print("\nInventory Management System")
        print("1. Add Product")
        print("2. Update Product")
        print("3. Record Sale")
        print("4. View Inventory")
        print("5. Recommend Restocks")
        print("6. Delete Product")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_product()
        elif choice == "2":
            update_product()
        elif choice == "3":
            record_sale()
        elif choice == "4":
            view_inventory()
        elif choice == "5":
            recommend_restock()
        elif choice == "6":
            delete_product()
        elif choice == "7":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Error: Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
