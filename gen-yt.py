import os
import csv
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename

title_list = []
svg_text = ""
filepath = ""

def open_file():
    """Open a file for editing."""
    _filepath = askopenfilename(
        filetypes=[("SVG Files", "*.svg"), ("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not _filepath:
        return
    txt_edit.delete("1.0", tk.END)
    with open(_filepath, mode="r", encoding="utf-8") as input_file:
        global svg_text
        svg_text = input_file.read()
        txt_edit.insert(tk.END, svg_text)
    window.title(f"Simple Text Editor - {_filepath}")

def save_file():
    """Save the current file as a new file."""
    _filepath = asksaveasfilename(
        defaultextension=".svg",
        _filepath=[("SVG Files", "*.svg"), ("Text Files", "*.txt"), ("All Files", "*.*")],
    )
    if not _filepath:
        return
    with open(_filepath, mode="w", encoding="utf-8") as output_file:
        text = txt_edit.get("1.0", tk.END)
        output_file.write(text)
    window.title(f"Simple Text Editor - {_filepath}")

def load_csv():
    """Import a CSV file."""
    _filepath = askopenfilename(
        filetypes=[("Text Files", "*.csv"), ("All Files", "*.*")]
    )
    if not _filepath:
        return
    
    global filepath
    filepath = _filepath
    print(filepath)
    print(os.path.basename(filepath))
    print(os.path.splitext(os.path.basename(filepath))[0])
    dirname = os.path.dirname(filepath)
    print(dirname)
    
    txt_edit.delete("1.0", tk.END)
    with open(_filepath, mode="r", encoding="utf-8") as csvfile:
        global title_list
        reader_list = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader_list:
            # print(', '.join(row))
            title_list.append(row)
            tree.insert("", tk.END, values=row)
            # replace(row)
        tree.grid(row=0, column=2, sticky="nsew", padx=5)        
        txt_edit.grid(row=0, column=1, sticky="nsew")
    window.title(f"Load CSV - {_filepath}")

def process_svg():
    """Process SVG with data from CSV file."""
    global title_list
    _c = 0
    for row in title_list:
        # print(', '.join(row))
        if (_c==0): 
            replace(row)
            _c = _c+0

def replace(_row):
    """Replaces"""
    global svg_text
    tmp_text = txt_edit.get(1.0,tk.END)

    _series = _row[1]
    # print(_series)
    tmp_text = svg_text.replace("{{series}}",_series)

    _title = _row[2]
    # print(_title)
    tmp_text = tmp_text.replace("{{title}}",_title)

    txt_edit.delete(1.0,tk.END)
    txt_edit.insert(tk.END, tmp_text)
    save_svg(tmp_text,_filename=_row[4])

def save_svg(_svg_text,_filename):
    """Save the current SVG file as a new file."""
    global filepath
    print(filepath)
    print(os.path.basename(filepath))
    print(os.path.splitext(os.path.basename(filepath))[0])
    dirname = os.path.dirname(filepath)
    print(dirname)
    _separator = '/'    
    _filepath = dirname + _separator+ _filename + ".svg"
    
    print(_filepath)

    with open(_filepath, mode="w", encoding="utf-8") as output_file:
        text = _svg_text
        output_file.write(text)
    



window = tk.Tk()
window.title("Simple Text Editor")

# define columns
columns = ('c_number', 'c_series', 'c_title', 'c_yturl','c_fname')
tree = ttk.Treeview(window, columns=columns, show='headings')
tree.column('c_number', width=50)

# define headings
tree.heading('c_number', text='Number')
tree.heading('c_series', text='Series')
tree.heading('c_title', text='Title')
tree.heading('c_yturl', text='YT URL')
tree.heading('c_fname', text='Filename')

window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

txt_edit = tk.Text(window)
frm_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
btn_open = tk.Button(frm_buttons, text="Open", command=open_file)
btn_save = tk.Button(frm_buttons, text="Save As...", command=save_file)
btn_load_csv = tk.Button(frm_buttons, text="Load CSV...", command=load_csv)
btn_process_svg = tk.Button(frm_buttons, text="Process SVG...", command=process_svg)

lbl_lines_count = tk.Label()


btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5)
btn_load_csv.grid(row=2, column=0, sticky="ew", padx=5)
btn_process_svg.grid(row=3, column=0, sticky="ew", padx=5)
frm_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")

window.mainloop()