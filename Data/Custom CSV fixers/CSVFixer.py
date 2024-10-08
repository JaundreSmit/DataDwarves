import csv
import re
import tkinter as tk
from tkinter import filedialog, messagebox

import csv
import re
from tkinter import messagebox

def clean_csv(file_path, output_path, row_limit=None):
    try:
        with open(file_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', newline='', encoding='utf-8') as outfile:
            reader = csv.reader(infile, quotechar='"', delimiter=',', quoting=csv.QUOTE_MINIMAL)
            writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)

            header = next(reader)
            column_limit = len(header)
            writer.writerow(header)

            for i, row in enumerate(reader):
                if row_limit and i >= row_limit:
                    break

                # Check for HTML tags and skip rows that contain them
                if any(re.search('<.*?>', cell) for cell in row):
                    continue

                # If row is longer than expected, adjust it
                if len(row) > column_limit:
                    # Join the remaining cells as part of the last cell
                    row = row[:column_limit - 1] + [" ".join(row[column_limit - 1:])]
                
                # Replace commas in the last cell
                if len(row) == column_limit:
                    row[column_limit - 1] = row[column_limit - 1].replace(',', ' ')

                writer.writerow(row)

        messagebox.showinfo("Success", "File cleaned and saved successfully!")

    except PermissionError:
        messagebox.showerror("Error", "Permission denied. Please check file permissions or ensure the file is not open in another program.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")




def browse_input_file():
    input_file = filedialog.askopenfilename(title="Select Input CSV File", filetypes=[("CSV files", "*.csv")])
    input_entry.delete(0, tk.END)
    input_entry.insert(0, input_file)
    
    if input_file:
        # Update column count after reading the first line of the CSV
        try:
            with open(input_file, 'r', encoding='utf-8') as infile:
                reader = csv.reader(infile, quotechar='"', delimiter=',', quoting=csv.QUOTE_MINIMAL)
                header = next(reader)
                column_count = len(header)
                column_count_label.config(text=f"Column Count: {column_count}")
        except Exception as e:
            column_count_label.config(text=f"Error reading file: {str(e)}")

def start_cleaning():
    input_file = input_entry.get()
    
    if row_limit_var.get():
        row_limit = int(row_limit_entry.get())
    else:
        row_limit = None

    if not input_file:
        messagebox.showwarning("Input Error", "Please select an input file.")
        return
    
    # Ask for output file only after cleaning starts
    output_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if not output_file:
        return  # User canceled the file save dialog

    clean_csv(input_file, output_file, row_limit)

def toggle_row_limit():
    if row_limit_var.get():
        row_limit_entry.config(state='normal')  # Enable row limit entry if checkbox is checked
    else:
        row_limit_entry.config(state='disabled')  # Disable row limit entry if checkbox is unchecked

# Initialize GUI
root = tk.Tk()
root.title("CSV Cleaner")

# Input File
tk.Label(root, text="Input CSV File:").grid(row=0, column=0, padx=10, pady=10)
input_entry = tk.Entry(root, width=50)
input_entry.grid(row=0, column=1, padx=10, pady=10)
browse_input_button = tk.Button(root, text="Browse", command=browse_input_file)
browse_input_button.grid(row=0, column=2, padx=10, pady=10)

# Column Count Display
column_count_label = tk.Label(root, text="Column Count: Not loaded")
column_count_label.grid(row=1, column=1, padx=10, pady=10)

# Row Limit Checkbox
row_limit_var = tk.IntVar()
row_limit_checkbox = tk.Checkbutton(root, text="Limit Rows", variable=row_limit_var, command=toggle_row_limit)
row_limit_checkbox.grid(row=2, column=0, padx=10, pady=10)

# Row Limit Entry (disabled by default)
row_limit_entry = tk.Entry(root, width=10)
row_limit_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")
row_limit_entry.config(state='disabled')  # Initially disabled

# Start Button
start_button = tk.Button(root, text="Start Cleaning", command=start_cleaning)
start_button.grid(row=3, column=1, pady=20)

# Run the GUI event loop
root.mainloop()
