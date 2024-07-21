import tkinter as tk
import math

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        
        # Entry for displaying current input and results
        self.entry = tk.Entry(root, width=40, borderwidth=5)
        self.entry.grid(row=0, column=0, columnspan=6, padx=10, pady=10)
        
        # Buttons
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('+', 1, 3), ('sin', 1, 4),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3), ('cos', 2, 4),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('*', 3, 3), ('tan', 3, 4),
            ('0', 4, 0), ('.', 4, 1), ('(', 4, 2), ('/', 4, 3), (')', 4, 4),
            ('Clear', 5, 0), ('Clear All', 5, 1), ('^', 5, 2), ('sqrt', 5, 3), ('=', 5, 4),
            ('Memory Recall', 6, 0), ('Memory Clear', 6, 1), ('log', 6, 2), ('ln', 6, 3), ('History', 6, 4)
        ]
        
        # Create buttons
        for (text, row, col) in buttons:
            tk.Button(root, text=text, padx=20, pady=15, command=lambda t=text: self.button_click(t)).grid(row=row, column=col)
        
        self.current_text = ""  # To store current display text
        self.memory = None  # Memory for storing numbers
        
    def button_click(self, value):
        if value == 'Clear':
            self.entry.delete(0, tk.END)
            self.current_text = ""
        elif value == 'Clear All':
            self.entry.delete(0, tk.END)
            self.current_text = ""
        elif value == 'Memory Recall':
            if self.memory is not None:
                self.entry.delete(0, tk.END)
                self.entry.insert(0, str(self.memory))
        elif value == 'Memory Clear':
            self.memory = None
        elif value == 'History':
            # Implement history functionality
            pass
        elif value == '=':
            try:
                result = eval(self.entry.get())
                self.entry.delete(0, tk.END)
                self.entry.insert(0, result)
                self.current_text = str(result)
            except Exception as e:
                self.entry.delete(0, tk.END)
                self.entry.insert(0, "Error")
        elif value in ['sin', 'cos', 'tan', 'log', 'ln', '^', 'sqrt']:
            func_map = {
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'log': math.log10,
                'ln': math.log,
                '^': lambda x, y: x ** y,
                'sqrt': math.sqrt
            }
            try:
                if value == 'sqrt':
                    result = func_map[value](float(self.entry.get()))
                else:
                    result = func_map[value](float(self.entry.get()))
                self.entry.delete(0, tk.END)
                self.entry.insert(0, result)
                self.current_text = str(result)
            except Exception as e:
                self.entry.delete(0, tk.END)
                self.entry.insert(0, "Error")
        else:
            self.entry.insert(tk.END, value)
            self.current_text += value

# Main application loop
if __name__ == "__main__":
    root = tk.Tk()
    calculator = CalculatorApp(root)
    root.mainloop()
