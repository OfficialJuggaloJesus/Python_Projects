import tkinter as tk

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        
        # Entry widget for displaying calculations
        self.display = tk.Entry(root, width=16, font=('Arial', 24), borderwidth=2, relief="solid")
        self.display.grid(row=0, column=0, columnspan=4)
        
        # Define button text and layout
        self.buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            'C', '0', '=', '+'
        ]
        
        # Create buttons and add to grid
        self.create_buttons()
        
        # Variable to store the expression
        self.expression = ""

    def create_buttons(self):
        row, col = 1, 0
        for button_text in self.buttons:
            button = tk.Button(self.root, text=button_text, padx=20, pady=20, font=('Arial', 18),
                               command=lambda text=button_text: self.on_button_click(text))
            button.grid(row=row, column=col)
            col += 1
            if col > 3:
                col = 0
                row += 1

    def on_button_click(self, text):
        if text == 'C':
            self.expression = ""
        elif text == '=':
            try:
                self.expression = str(eval(self.expression))
            except:
                self.expression = "Error"
        else:
            self.expression += text
        
        self.update_display()

    def update_display(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression)

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()
