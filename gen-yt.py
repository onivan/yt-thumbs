import os
import csv
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from cairosvg import svg2png

title_list = []
svg_text = ""
filepath = ""
images = []

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
    window.title(f"Gen-YT - {_filepath}")

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
    window.title(f"Gen-YT - {_filepath}")

def load_csv():
    """Import a CSV file."""
    _filepath = askopenfilename(
        filetypes=[("Text Files", "*.csv"), ("All Files", "*.*")]
    )
    if not _filepath:
        return
    
    global filepath
    global title_list

    filepath = _filepath
    print(filepath)
    print(os.path.basename(filepath))
    print(os.path.splitext(os.path.basename(filepath))[0])
    dirname = os.path.dirname(filepath)
    print(dirname)
    
    tree.delete(*tree.get_children())
    title_list = []

    txt_edit.delete("1.0", tk.END)
    with open(_filepath, mode="r", encoding="utf-8") as csvfile:
        
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
    populate_pics()

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
    _pic_format = "png"    
    _filepath_svg = dirname + _separator+ _filename + ".svg"
    _filepath_pic = dirname + _separator+ _filename + '.' + _pic_format
    print(_filepath_svg)

    with open(_filepath_svg, mode="w", encoding="utf-8") as output_file:
        text = _svg_text
        output_file.write(text)
    convert2pic(_filepath_svg, _filepath_pic, _pic_format)
    global images
    from wand.image import Image
    
    #from PIL import Image, ImageTk

    _image = Image(filename=_filepath_pic)
    print(_image)
    _img = Image(_image) 
    print(_img.width, _img.height)
    _img.resize(75,50)
    print(_img.width, _img.height)
    #ph = ImageTk.PhotoImage(im)    
    #images.append([_filepath_pic,_image,_img])
 

def populate_pics():
    """Populate pics"""
    global images
    if not images:
        return
    print(images)
    for img in images:
        print(img)
        #pic_tree.insert("", tk.END, text=img[0], image=img[1])

def convert2pic(svg_file, pic_file, pic_format, resolution = 72):
    """Convert svg to png """
    #svg2png(bytestring=_svg_code,write_to='output.png')
    
    from wand.image import Image

    ny = Image(filename = svg_file)
    ny_convert = ny.convert(pic_format)
    ny_convert.save(filename = pic_file)
    

def convert(svg_file, png_file, resolution = 72):
    from wand.api import library
    import wand.color
    import wand.image

    with open(svg_file, "r") as svg_file:
        with wand.image.Image() as image:
            svg_blob = svg_file.read().encode('utf-8')
            image.read(blob=svg_blob, resolution = resolution)
            png_image = image.make_blob("png32")

    with open(png_file, "wb") as out:
        out.write(png_image)


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


txt_edit = tk.Text(window,height=5)

frm_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
btn_open = tk.Button(frm_buttons, text="Open SVG", command=open_file)
btn_save = tk.Button(frm_buttons, text="Save As...", command=save_file)
btn_load_csv = tk.Button(frm_buttons, text="Load CSV...", command=load_csv)
btn_process_svg = tk.Button(frm_buttons, text="Process SVG...", command=process_svg)

lbl_lines_count = tk.Label()

# define columns
#pic_columns = ('c_fname', 'c_pic')
#pic_tree = ttk.Treeview(window, columns=pic_columns, show='headings')
#pic_tree.column('c_fname', width=150)
#pic_tree.column('c_pic', width=500)
#pic_tree.rowconfigure()
# define headings
#pic_tree.heading('c_fname', text='Fname')
#pic_tree.heading('c_pic', text='Pic')

pic_tree = ttk.Treeview(window)

btn_load_csv.grid(row=0, column=0, sticky="ew", padx=5)
btn_open.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
btn_process_svg.grid(row=2, column=0, sticky="ew", padx=5)
btn_save.grid(row=3, column=0, sticky="ew", padx=5)


frm_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="new")
pic_tree.grid(row=1, column=1, sticky="nsew")

window.rowconfigure(0, minsize=100, weight=1)
window.columnconfigure(1, minsize=500, weight=1)


window.mainloop()