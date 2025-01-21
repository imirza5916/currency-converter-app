import requests
import tkinter as tk
from tkinter import ttk

# Fetch available currencies from the API
def get_currency_list():
    api_url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        currency_dict = {currency: currency for currency in data['rates'].keys()}  # Placeholder for full names
        return currency_dict
    else:
        return {}

# Function to fetch exchange rate
def get_exchange_rate(base_currency, target_currency):
    api_url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if target_currency in data['rates']:
            return data['rates'][target_currency]
        else:
            print("Error: Target currency not found.")
            return None
    else:
        print("Error: Unable to fetch exchange rates.")
        return None

# Function to perform conversion
def convert_currency():
    base_currency = currency_dict[base_currency_var.get()]
    target_currency = currency_dict[target_currency_var.get()]
    amount = float(amount_entry.get())
    
    exchange_rate = get_exchange_rate(base_currency, target_currency)
    if exchange_rate:
        converted_amount = amount * exchange_rate
        result_label.config(text=f"{amount} {base_currency} is equal to {converted_amount:.2f} {target_currency}")
    else:
        result_label.config(text="Conversion failed. Please check your currency selection.")

# Setup Tkinter GUI
root = tk.Tk()
root.title("Currency Converter")
root.geometry("500x400")
root.eval('tk::PlaceWindow . center')  # Center the window on screen

currency_dict = get_currency_list()
if not currency_dict:
    currency_dict = {"United States Dollar (USD)": "USD", "Euro (EUR)": "EUR", "British Pound (GBP)": "GBP", "Japanese Yen (JPY)": "JPY", "Canadian Dollar (CAD)": "CAD"}  # Fallback options

currency_names = list(currency_dict.keys())

# Frame to center widgets
frame = tk.Frame(root)
frame.pack(expand=True)

# Dropdown menus for currency selection
base_currency_var = tk.StringVar()
target_currency_var = tk.StringVar()

base_currency_label = tk.Label(frame, text="Convert from:")
base_currency_label.pack()
base_currency_menu = ttk.Combobox(frame, textvariable=base_currency_var, values=currency_names, state="readonly")
base_currency_menu.pack()
base_currency_menu.current(0)
base_currency_menu.bind("<KeyPress>", lambda event: base_currency_menu.event_generate("<<ComboboxSelect>>"))

target_currency_label = tk.Label(frame, text="Convert to:")
target_currency_label.pack()
target_currency_menu = ttk.Combobox(frame, textvariable=target_currency_var, values=currency_names, state="readonly")
target_currency_menu.pack()
target_currency_menu.current(1)
target_currency_menu.bind("<KeyPress>", lambda event: target_currency_menu.event_generate("<<ComboboxSelect>>"))

# Input field for amount
amount_label = tk.Label(frame, text="Amount:")
amount_label.pack()
amount_entry = tk.Entry(frame)
amount_entry.pack()

# Convert button
convert_button = tk.Button(frame, text="Convert", command=convert_currency)
convert_button.pack()

# Result label
result_label = tk.Label(frame, text="")
result_label.pack()

root.mainloop()
