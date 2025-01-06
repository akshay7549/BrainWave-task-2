import sqlite3
from tkinter import *
from tkinter import messagebox, ttk

# Database Setup
conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    category TEXT,
                    quantity INTEGER,
                    price REAL)''')
conn.commit()

# GUI Setup
root = Tk()
root.title("Inventory Management System")
root.geometry("800x500")
root.configure(bg="#f0f0f0")

# Add Product Function
def add_product():
    try:
        name = name_entry.get()
        category = category_entry.get()
        quantity = int(quantity_entry.get())
        price = float(price_entry.get())

        cursor.execute("INSERT INTO products (name, category, quantity, price) VALUES (?, ?, ?, ?)",
                       (name, category, quantity, price))
        conn.commit()
        messagebox.showinfo("Success", "Product added successfully!")
        clear_entries()
        show_products()
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

# Show Products Function
def show_products():
    for row in product_list.get_children():
        product_list.delete(row)

    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    for row in rows:
        product_list.insert("", END, values=row)

# Delete Product Function
def delete_product():
    selected = product_list.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a product to delete.")
        return

    product_id = product_list.item(selected)['values'][0]
    cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    messagebox.showinfo("Success", "Product deleted successfully!")
    show_products()

# Select Product Function
def select_product():
    selected = product_list.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a product to edit.")
        return

    values = product_list.item(selected)['values']
    name_entry.delete(0, END)
    category_entry.delete(0, END)
    quantity_entry.delete(0, END)
    price_entry.delete(0, END)

    name_entry.insert(0, values[1])
    category_entry.insert(0, values[2])
    quantity_entry.insert(0, values[3])
    price_entry.insert(0, values[4])

# Update Product Function
def update_product():
    try:
        selected = product_list.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product to update.")
            return

        product_id = product_list.item(selected)['values'][0]
        name = name_entry.get()
        category = category_entry.get()
        quantity = int(quantity_entry.get())
        price = float(price_entry.get())

        cursor.execute("UPDATE products SET name=?, category=?, quantity=?, price=? WHERE id=?",
                       (name, category, quantity, price, product_id))
        conn.commit()
        messagebox.showinfo("Success", "Product updated successfully!")
        clear_entries()
        show_products()
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

# Low Stock Alert Function
def low_stock_alert():
    cursor.execute("SELECT * FROM products WHERE quantity < 5")
    rows = cursor.fetchall()
    alert_message = "Low Stock Products:\n"
    for row in rows:
        alert_message += f"{row[1]} - Only {row[3]} left!\n"
    messagebox.showinfo("Low Stock Alert", alert_message)

# Clear Entries Function
def clear_entries():
    name_entry.delete(0, END)
    category_entry.delete(0, END)
    quantity_entry.delete(0, END)
    price_entry.delete(0, END)

# GUI Widgets
Label(root, text="Product Name", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
Label(root, text="Category", bg="#f0f0f0", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)
Label(root, text="Quantity", bg="#f0f0f0", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10)
Label(root, text="Price", bg="#f0f0f0", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=10)

name_entry = Entry(root, font=("Arial", 12))
category_entry = Entry(root, font=("Arial", 12))
quantity_entry = Entry(root, font=("Arial", 12))
price_entry = Entry(root, font=("Arial", 12))

name_entry.grid(row=0, column=1, padx=10, pady=10)
category_entry.grid(row=1, column=1, padx=10, pady=10)
quantity_entry.grid(row=2, column=1, padx=10, pady=10)
price_entry.grid(row=3, column=1, padx=10, pady=10)

Button(root, text="Add Product", command=add_product, bg="#4caf50", fg="white", font=("Arial", 12)).grid(row=4, column=0, pady=10)
Button(root, text="Update Product", command=update_product, bg="#2196f3", fg="white", font=("Arial", 12)).grid(row=4, column=1, pady=10)
Button(root, text="Delete Product", command=delete_product, bg="#f44336", fg="white", font=("Arial", 12)).grid(row=5, column=0, pady=10)
Button(root, text="Select Product", command=select_product, bg="#ff9800", fg="white", font=("Arial", 12)).grid(row=5, column=1, pady=10)
Button(root, text="Low Stock Alert", command=low_stock_alert, bg="#673ab7", fg="white", font=("Arial", 12)).grid(row=6, column=0, columnspan=2, pady=10)

# Product List
product_list = ttk.Treeview(root, columns=("ID", "Name", "Category", "Quantity", "Price"), show='headings')
product_list.heading("ID", text="ID")
product_list.heading("Name", text="Name")
product_list.heading("Category", text="Category")
product_list.heading("Quantity", text="Quantity")
product_list.heading("Price", text="Price")
product_list.grid(row=0, column=2, rowspan=7, padx=20, pady=10)

# Initialize Product List
show_products()

# Run the Application
root.mainloop()

# Close Database Connection
conn.close()
