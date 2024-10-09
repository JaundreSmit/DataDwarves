import pandas as pd
from tkinter import filedialog, Tk, Button, messagebox

def clean_weird_characters(file_path):
    try:
        # Read the CSV file while handling errors
        df = pd.read_csv(file_path, on_bad_lines='warn', quotechar='"')
        
        # Example cleaning: Remove non-ASCII characters (you can modify as needed)
        df = df.applymap(lambda x: ''.join([i for i in x if ord(i) < 128]) if isinstance(x, str) else x)

        # Save cleaned data
        output_path = file_path.replace('.csv', '_cleaned.csv')
        df.to_csv(output_path, index=False)
        messagebox.showinfo("Success", f"File cleaned and saved as: {output_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        clean_weird_characters(file_path)

# Create a simple GUI
root = Tk()
root.title("CSV Cleaner")
select_button = Button(root, text="Select CSV File", command=select_file)
select_button.pack(pady=20)

root.mainloop()
