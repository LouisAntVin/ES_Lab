from flask import Flask, render_template, request, redirect
import pandas as pd

app = Flask(__name__)
file = "inventory.csv"

def load():
    try:
        return pd.read_csv(file)
    except:
        return pd.DataFrame(columns=["ID", "Name", "Category", "Price", "Stock", "Sales"])

def save(data):
    data.to_csv(file, index=False)

@app.route("/", methods=["GET", "POST"])
def home():
    inv = load()
    low = []

    if request.method == "POST":
        act = request.form["action"]

        if act == "add":
            row = {
                "ID": request.form["id"],
                "Name": request.form["name"],
                "Category": request.form["cat"],
                "Price": request.form["price"],
                "Stock": request.form["stock"],
                "Sales": 0
            }
            inv = pd.concat([inv, pd.DataFrame([row])], ignore_index=True)

        elif act == "delete":
            inv = inv[inv["ID"] != request.form["id"]]

        elif act == "update":
            val = request.form["val"]
            try:
                val = float(val) if request.form["field"] == "Price" else int(val)
            except:
                return redirect("/")
            inv.loc[inv["ID"] == request.form["id"], request.form["field"]] = val

        elif act == "restock":
            threshold = int(request.form["threshold"])
            low = inv[inv["Stock"].astype(int) < threshold].to_dict("records")

        save(inv)

    return render_template("index.html", inv=inv.to_dict("records"), low=low)

if __name__ == "__main__":
    app.run(debug=True)



'''from flask import Flask, render_template, request, redirect
import pandas as pd

app = Flask(__name__)
inventory_file = "inventory.csv"

def load_inventory():
    try:
        return pd.read_csv(inventory_file)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Product ID", "Product Name", "Category", "Price", "Stock", "Total Sales"])

def save_inventory(inventory):
    inventory.to_csv(inventory_file, index=False)

@app.route("/", methods=["GET", "POST"])
def home():
    inventory = load_inventory()
    low_stock_items = []

    if request.method == "POST":
        action = request.form.get("action")

        if action == "add":
            # Add Product
            product_id = request.form["product_id"]
            product_name = request.form["product_name"]
            category = request.form["category"]
            price = request.form["price"]
            stock = request.form["stock"]

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

        elif action == "delete":
            # Delete Product
            product_id = request.form["delete_id"]
            inventory = inventory[inventory["Product ID"] != product_id]
            save_inventory(inventory)

        elif action == "update":
            # Update Product
            product_id = request.form["update_id"]
            field = request.form["field"]
            new_value = request.form["new_value"]

            if field in ["Price", "Stock"]:
                try:
                    new_value = float(new_value) if field == "Price" else int(new_value)
                except ValueError:
                    return redirect("/")  # Invalid input, just refresh

            inventory.loc[inventory["Product ID"] == product_id, field] = new_value
            save_inventory(inventory)

        elif action == "restock":
            # Recommend Restock
            threshold = int(request.form["threshold"])
            low_stock_items = inventory[inventory["Stock"].astype(int) < threshold].to_dict(orient="records")

    return render_template("index.html", inventory=inventory.to_dict(orient="records"), low_stock_items=low_stock_items)

if __name__ == "__main__":
    app.run(debug=True)
'''