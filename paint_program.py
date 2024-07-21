import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter import filedialog
import PIL.ImageGrab as ImageGrab

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Paint Application")
        
        self.pen_color = 'black'
        self.brush_size = 5
        self.eraser_on = False
        self.current_tool = 'brush'
        self.actions = []

        self.canvas = tk.Canvas(self.root, bg='white', width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Button-1>', self.start_draw)

        self.toolbar = tk.Frame(self.root)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_toolbar_buttons()

    def add_toolbar_buttons(self):
        self.color_button = tk.Button(self.toolbar, text='Choose Color', command=self.choose_color)
        self.color_button.pack(side=tk.LEFT)
        
        self.size_slider = tk.Scale(self.toolbar, from_=1, to=10, orient=tk.HORIZONTAL, command=self.change_size)
        self.size_slider.set(self.brush_size)
        self.size_slider.pack(side=tk.LEFT)
        
        self.brush_button = tk.Button(self.toolbar, text='Brush', command=self.use_brush)
        self.brush_button.pack(side=tk.LEFT)
        
        self.eraser_button = tk.Button(self.toolbar, text='Eraser', command=self.use_eraser)
        self.eraser_button.pack(side=tk.LEFT)
        
        self.line_button = tk.Button(self.toolbar, text='Line', command=self.use_line)
        self.line_button.pack(side=tk.LEFT)
        
        self.rect_button = tk.Button(self.toolbar, text='Rectangle', command=self.use_rect)
        self.rect_button.pack(side=tk.LEFT)
        
        self.oval_button = tk.Button(self.toolbar, text='Oval', command=self.use_oval)
        self.oval_button.pack(side=tk.LEFT)
        
        self.text_button = tk.Button(self.toolbar, text='Text', command=self.use_text)
        self.text_button.pack(side=tk.LEFT)
        
        self.undo_button = tk.Button(self.toolbar, text='Undo', command=self.undo)
        self.undo_button.pack(side=tk.LEFT)
        
        self.redo_button = tk.Button(self.toolbar, text='Redo', command=self.redo)
        self.redo_button.pack(side=tk.LEFT)
        
        self.save_button = tk.Button(self.toolbar, text='Save', command=self.save)
        self.save_button.pack(side=tk.LEFT)
        
        self.clear_button = tk.Button(self.toolbar, text='Clear', command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT)

    def paint(self, event):
        paint_color = 'white' if self.eraser_on else self.pen_color
        if self.current_tool == 'brush' or self.current_tool == 'eraser':
            x1, y1 = (event.x - self.brush_size), (event.y - self.brush_size)
            x2, y2 = (event.x + self.brush_size), (event.y + self.brush_size)
            self.canvas.create_oval(x1, y1, x2, y2, fill=paint_color, outline=paint_color)
            self.actions.append(('brush', x1, y1, x2, y2, paint_color))

    def reset(self, event):
        self.last_x, self.last_y = None, None

    def choose_color(self):
        self.pen_color = askcolor(color=self.pen_color)[1]
        self.eraser_on = False

    def change_size(self, new_size):
        self.brush_size = int(new_size)

    def use_brush(self):
        self.eraser_on = False
        self.current_tool = 'brush'

    def use_eraser(self):
        self.eraser_on = True
        self.current_tool = 'eraser'

    def use_line(self):
        self.eraser_on = False
        self.current_tool = 'line'

    def use_rect(self):
        self.eraser_on = False
        self.current_tool = 'rect'

    def use_oval(self):
        self.eraser_on = False
        self.current_tool = 'oval'

    def use_text(self):
        self.eraser_on = False
        self.current_tool = 'text'

    def clear_canvas(self):
        self.canvas.delete('all')
        self.actions = []

    def save(self):
        file = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG files', '*.png'), ('All files', '*.*')])
        if file:
            x = self.root.winfo_rootx() + self.canvas.winfo_x()
            y = self.root.winfo_rooty() + self.canvas.winfo_y()
            x1 = x + self.canvas.winfo_width()
            y1 = y + self.canvas.winfo_height()
            ImageGrab.grab().crop((x, y, x1, y1)).save(file)

    def undo(self):
        if self.actions:
            self.actions.pop()
            self.redraw()

    def redo(self):
        pass  # Implement redo functionality if needed

    def redraw(self):
        self.canvas.delete('all')
        for action in self.actions:
            if action[0] == 'brush':
                self.canvas.create_oval(action[1], action[2], action[3], action[4], fill=action[5], outline=action[5])

    def start_draw(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.current_shape = None
        if self.current_tool == 'line':
            self.current_shape = self.canvas.create_line(self.start_x, self.start_y, self.start_x, self.start_y, fill=self.pen_color)
        elif self.current_tool == 'rect':
            self.current_shape = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline=self.pen_color)
        elif self.current_tool == 'oval':
            self.current_shape = self.canvas.create_oval(self.start_x, self.start_y, self.start_x, self.start_y, outline=self.pen_color)
        elif self.current_tool == 'text':
            text = self.canvas.create_text(self.start_x, self.start_y, text='Your Text Here', fill=self.pen_color, font=('Arial', self.brush_size * 2))
            self.actions.append(('text', self.start_x, self.start_y, 'Your Text Here', self.pen_color, self.brush_size * 2))
            self.current_shape = text

    def draw_shape(self, event):
        if self.current_tool in ['line', 'rect', 'oval']:
            self.canvas.coords(self.current_shape, self.start_x, self.start_y, event.x, event.y)

if __name__ == '__main__':
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()
