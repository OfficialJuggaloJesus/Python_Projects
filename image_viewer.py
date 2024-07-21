import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, colorchooser
from PIL import Image, ImageTk, ImageEnhance, ImageFilter, ImageOps
import os

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")

        self.image = None
        self.image_tk = None
        self.selection_tool = None
        self.selection_start = None
        self.selection_end = None
        self.undo_stack = []
        self.redo_stack = []
        self.zoom_scale = 1.0

        self.create_widgets()
        self.create_menus()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, bg='gray')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.scroll_x = tk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.scroll_y = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.config(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)

        self.toolbar = tk.Frame(self.root)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        buttons = [
            ("Open", self.open_image),
            ("Save", self.save_image),
            ("Undo", self.undo),
            ("Redo", self.redo),
            ("Zoom In", self.zoom_in),
            ("Zoom Out", self.zoom_out),
            ("Fit to Window", self.fit_to_window),
            ("Reset Zoom", self.reset_zoom),
            ("Rotate Left", self.rotate_left),
            ("Rotate Right", self.rotate_right),
            ("Flip Horizontal", self.flip_horizontal),
            ("Flip Vertical", self.flip_vertical),
            ("Brightness", self.adjust_brightness),
            ("Contrast", self.adjust_contrast),
            ("Blur", self.apply_blur),
            ("Sharpen", self.apply_sharpen),
            ("Edge Enhance", self.apply_edge_enhance),
            ("Crop", self.crop_image),
            ("New Layer", self.new_layer),
            ("Delete Layer", self.delete_layer),
            ("Layer Properties", self.layer_properties),
            ("Draw Tool", self.draw_tool),
            ("Erase Tool", self.erase_tool),
            ("Color Balance", self.adjust_color_balance)
        ]

        for text, command in buttons:
            tk.Button(self.toolbar, text=text, command=command).pack(side=tk.LEFT)

    def create_menus(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_image)
        file_menu.add_command(label="Save", command=self.save_image)
        file_menu.add_command(label="Save As", command=self.save_image_as)
        file_menu.add_command(label="Export as", command=self.export_as_image)
        file_menu.add_command(label="Page Setup", command=self.page_setup)
        file_menu.add_command(label="Print", command=self.print_image)
        file_menu.add_command(label="Exit", command=self.root.quit)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)
        edit_menu.add_command(label="Resize", command=self.resize_image_dialog)
        edit_menu.add_command(label="Rotate Left", command=self.rotate_left)
        edit_menu.add_command(label="Rotate Right", command=self.rotate_right)
        edit_menu.add_command(label="Flip Horizontal", command=self.flip_horizontal)
        edit_menu.add_command(label="Flip Vertical", command=self.flip_vertical)
        edit_menu.add_command(label="Brightness", command=self.adjust_brightness)
        edit_menu.add_command(label="Contrast", command=self.adjust_contrast)
        edit_menu.add_command(label="Blur", command=self.apply_blur)
        edit_menu.add_command(label="Sharpen", command=self.apply_sharpen)
        edit_menu.add_command(label="Edge Enhance", command=self.apply_edge_enhance)
        edit_menu.add_command(label="Crop", command=self.crop_image)

        select_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Select", menu=select_menu)
        select_menu.add_command(label="Rectangle Select", command=self.rectangle_select)
        select_menu.add_command(label="Freehand Select", command=self.freehand_select)
        select_menu.add_command(label="Move Selection", command=self.move_selection)
        select_menu.add_command(label="Delete Selection", command=self.delete_selection)
        select_menu.add_command(label="Show Rulers", command=self.show_rulers)
        select_menu.add_command(label="Show Grid", command=self.show_grid)

        view_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Reset View", command=self.reset_view)

        image_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Image", menu=image_menu)
        image_menu.add_command(label="Rotate Left", command=self.rotate_left)
        image_menu.add_command(label="Rotate Right", command=self.rotate_right)
        image_menu.add_command(label="Flip Horizontal", command=self.flip_horizontal)
        image_menu.add_command(label="Flip Vertical", command=self.flip_vertical)

        layer_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Layer", menu=layer_menu)
        layer_menu.add_command(label="New Layer", command=self.new_layer)
        layer_menu.add_command(label="Delete Layer", command=self.delete_layer)
        layer_menu.add_command(label="Layer Properties", command=self.layer_properties)

        colors_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Colors", menu=colors_menu)
        colors_menu.add_command(label="Adjust Color Balance", command=self.adjust_color_balance)

        tools_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Draw Tool", command=self.draw_tool)
        tools_menu.add_command(label="Erase Tool", command=self.erase_tool)

        filters_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Filters", menu=filters_menu)
        filters_menu.add_command(label="Apply Blur", command=self.apply_blur)
        filters_menu.add_command(label="Apply Sharpen", command=self.apply_sharpen)
        filters_menu.add_command(label="Apply Edge Enhance", command=self.apply_edge_enhance)

        windows_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Windows", menu=windows_menu)
        windows_menu.add_command(label="New Window", command=self.new_window)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def new_window(self):
        new_root = tk.Toplevel(self.root)
        ImageEditor(new_root)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if file_path:
            self.image = Image.open(file_path)
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def save_image(self):
        if self.image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
            if file_path:
                self.image.save(file_path)

    def save_image_as(self):
        # This method does the same thing as save_image but can be extended if needed
        self.save_image()

    def export_as_image(self):
        # Placeholder for export functionality
        pass

    def page_setup(self):
        # Placeholder for page setup functionality
        pass

    def print_image(self):
        if self.image:
            temp_file = "temp_image.png"
            self.image.save(temp_file)

            preview_window = tk.Toplevel(self.root)
            preview_window.title("Print Preview")

            preview_canvas = tk.Canvas(preview_window, width=600, height=800)
            preview_canvas.pack()

            preview_image = Image.open(temp_file)
            preview_image.thumbnail((600, 800))
            preview_image_tk = ImageTk.PhotoImage(preview_image)
            preview_canvas.create_image(0, 0, anchor=tk.NW, image=preview_image_tk)

            preview_window.mainloop()

            os.remove(temp_file)

    def resize_image_dialog(self):
        if self.image:
            width = simpledialog.askinteger("Resize", "Enter new width:", initialvalue=self.image.width)
            height = simpledialog.askinteger("Resize", "Enter new height:", initialvalue=self.image.height)
            if width and height:
                self.image = self.image.resize((width, height), Image.ANTIALIAS)
                self.image_tk = ImageTk.PhotoImage(self.image)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
                self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def rotate_left(self):
        if self.image:
            self.image = self.image.rotate(90, expand=True)
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def rotate_right(self):
        if self.image:
            self.image = self.image.rotate(-90, expand=True)
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def flip_horizontal(self):
        if self.image:
            self.image = ImageOps.mirror(self.image)
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def flip_vertical(self):
        if self.image:
            self.image = ImageOps.flip(self.image)
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def adjust_brightness(self):
        if self.image:
            factor = simpledialog.askfloat("Brightness", "Enter brightness factor (1.0 is original):", initialvalue=1.0)
            if factor:
                enhancer = ImageEnhance.Brightness(self.image)
                self.image = enhancer.enhance(factor)
                self.image_tk = ImageTk.PhotoImage(self.image)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
                self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def adjust_contrast(self):
        if self.image:
            factor = simpledialog.askfloat("Contrast", "Enter contrast factor (1.0 is original):", initialvalue=1.0)
            if factor:
                enhancer = ImageEnhance.Contrast(self.image)
                self.image = enhancer.enhance(factor)
                self.image_tk = ImageTk.PhotoImage(self.image)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
                self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def apply_blur(self):
        if self.image:
            radius = simpledialog.askfloat("Blur", "Enter blur radius:", initialvalue=2.0)
            if radius:
                self.image = self.image.filter(ImageFilter.GaussianBlur(radius))
                self.image_tk = ImageTk.PhotoImage(self.image)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
                self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def apply_sharpen(self):
        if self.image:
            self.image = self.image.filter(ImageFilter.SHARPEN)
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def apply_edge_enhance(self):
        if self.image:
            self.image = self.image.filter(ImageFilter.EDGE_ENHANCE)
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def crop_image(self):
        if self.image:
            x1, y1, x2, y2 = self.selection_start[0], self.selection_start[1], self.selection_end[0], self.selection_end[1]
            self.image = self.image.crop((x1, y1, x2, y2))
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def new_layer(self):
        # Placeholder for new layer functionality
        pass

    def delete_layer(self):
        # Placeholder for delete layer functionality
        pass

    def layer_properties(self):
        # Placeholder for layer properties functionality
        pass

    def draw_tool(self):
        # Placeholder for draw tool functionality
        pass

    def erase_tool(self):
        # Placeholder for erase tool functionality
        pass

    def adjust_color_balance(self):
        # Placeholder for color balance adjustment functionality
        pass

    def rectangle_select(self):
        self.selection_tool = 'rectangle'

    def freehand_select(self):
        self.selection_tool = 'freehand'

    def move_selection(self):
        self.selection_tool = 'move'

    def delete_selection(self):
        self.selection_tool = 'delete'

    def show_rulers(self):
        # Placeholder for showing rulers functionality
        pass

    def show_grid(self):
        # Placeholder for showing grid functionality
        pass

    def reset_view(self):
        # Placeholder for resetting view functionality
        pass

    def undo(self):
        # Placeholder for undo functionality
        pass

    def redo(self):
        # Placeholder for redo functionality
        pass

    def fit_to_window(self):
        # Placeholder for fitting image to window functionality
        pass

    def reset_zoom(self):
        self.zoom_scale = 1.0
        self.apply_zoom()

    def zoom_in(self):
        self.zoom_scale *= 1.1
        self.apply_zoom()

    def zoom_out(self):
        self.zoom_scale *= 0.9
        self.apply_zoom()

    def apply_zoom(self):
        if self.image:
            width, height = int(self.image.width * self.zoom_scale), int(self.image.height * self.zoom_scale)
            resized_image = self.image.resize((width, height), Image.ANTIALIAS)
            self.image_tk = ImageTk.PhotoImage(resized_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def show_about(self):
        messagebox.showinfo("About", "Image Editor v1.0\nDeveloped by Your Name")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop()
