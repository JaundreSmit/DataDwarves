import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

def preprocess_csv(file_path):
    fixed_lines = []
    with open(file_path, 'r', encoding='utf-8') as infile:
        for line in infile:
            # Remove any HTML tags (if any)
            line = remove_html_tags(line)

            # Fix unmatched quotes by replacing quotes on the end of the line
            if line.count('"') % 2 != 0:
                line = line.rstrip() + '"'  # Append closing quote if missing
            
            # Add the line to the fixed list
            fixed_lines.append(line.strip())
    
    return fixed_lines

def remove_html_tags(text):
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def clean_csv_with_pandas(file_path, output_path, row_limit=None):
    try:
        # Preprocess the CSV to fix common formatting issues
        fixed_lines = preprocess_csv(file_path)

        # Create a temporary fixed CSV string for Pandas
        temp_csv = '\n'.join(fixed_lines)

        # Use StringIO to read the fixed CSV
        from io import StringIO
        df = pd.read_csv(StringIO(temp_csv), quotechar='"', on_bad_lines='warn')

        # Limit the number of rows if specified
        if row_limit is not None:
            df = df.head(row_limit)

        # Replace commas in the last column
        if df.shape[1] > 1:
            df[df.columns[-1]] = df[df.columns[-1]].str.replace(',', ' ', regex=False)

        # Save the cleaned data
        df.to_csv(output_path, index=False)
        print("File cleaned and saved successfully!")
        messagebox.showinfo("Success", "File cleaned and saved successfully!")

    except PermissionError:
        messagebox.showerror("Error", "Permission denied. Please check file permissions or ensure the file is not open in another program.")
    except pd.errors.ParserError as e:
        messagebox.showerror("Error", f"ParserError: {str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        file_label.config(text=file_path)
        # Read the number of columns from the selected file and display it
        df = pd.read_csv(file_path, nrows=0)
        column_count = len(df.columns)
        column_label.config(text=f"Column count: {column_count}")

def save_file():
    output_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if output_path:
        row_limit = int(row_limit_entry.get()) if row_limit_var.get() else None
        clean_csv_with_pandas(file_label.cget("text"), output_path, row_limit)

# Create the main application window
app = tk.Tk()
app.title("CSV Cleaner")

# Create and place GUI elements
file_label = tk.Label(app, text="No file selected")
file_label.pack(pady=10)

browse_button = tk.Button(app, text="Browse for CSV File", command=browse_file)
browse_button.pack(pady=5)

column_label = tk.Label(app, text="Column count: ")
column_label.pack(pady=10)

row_limit_var = tk.IntVar()
row_limit_check = tk.Checkbutton(app, text="Limit row count", variable=row_limit_var)
row_limit_check.pack(pady=5)

row_limit_entry = tk.Entry(app, width=10)
row_limit_entry.pack(pady=5)
row_limit_entry.insert(0, "Enter limit")

save_button = tk.Button(app, text="Clean and Save CSV", command=save_file)
save_button.pack(pady=20)

# Run the application
app.mainloop()
