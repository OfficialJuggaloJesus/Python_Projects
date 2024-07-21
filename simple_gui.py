import tkinter as tk
import math

def calculate():
    user_input = entry.get()
    try:
        if '**' in user_input:
            base, exponent = user_input.split('**')
            result = float(base) ** float(exponent)
        elif user_input.startswith('sqrt'):
            number = float(user_input[4:])
            result = math.sqrt(number)
        elif user_input.startswith('sin'):
            angle = float(user_input[3:])
            result = math.sin(math.radians(angle))  # Convert degrees to radians
        elif user_input.startswith('cos'):
            angle = float(user_input[3:])
            result = math.cos(math.radians(angle))  # Convert degrees to radians
        elif user_input.startswith('tan'):
            angle = float(user_input[3:])
            result = math.tan(math.radians(angle))  # Convert degrees to radians
        elif user_input.startswith('log'):
            number = float(user_input[3:])
            result = math.log10(number)
        else:
            result = eval(user_input)
        
        output_label.config(text="Result: " + str(result))
    
    except ValueError:
        output_label.config(text="Invalid input. Please enter a valid number or operation.")
    except ZeroDivisionError:
        output_label.config(text="Error: Division by zero.")
    except Exception as e:
        output_label.config(text="An error occurred: " + str(e))

# Function to handle button clicks
def button_click(symbol):
    if symbol == '=':
        calculate()
    elif symbol == '←':  # Backspace button
        current = entry.get()
        entry.delete(len(current) - 1, tk.END)
    else:
        current = entry.get()
        entry.delete(0, tk.END)
        entry.insert(0, current + symbol)

# Function to switch calculator mode
def switch_mode(mode):
    if mode == "Standard":
        # Clear entry and reset output label
        entry.delete(0, tk.END)
        output_label.config(text="")
        
        # Remove scientific calculator buttons
        for button_row in scientific_buttons:
            for button in button_row:
                button.grid_remove()
        
        # Add or show standard calculator buttons
        for button_row in standard_buttons:
            for button in button_row:
                button.grid()

    elif mode == "Scientific":
        # Clear entry and reset output label
        entry.delete(0, tk.END)
        output_label.config(text="")
        
        # Remove standard calculator buttons
        for button_row in standard_buttons:
            for button in button_row:
                button.grid_remove()
        
        # Add or show scientific calculator buttons
        for button_row in scientific_buttons:
            for button in button_row:
                button.grid()

# Create the main window
root = tk.Tk()
root.title("Calculator")

# Create entry widget for user input
entry = tk.Entry(root, width=40, font=("Arial", 14))
entry.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

# Create buttons for digits and operations in standard mode
standard_buttons = [
    [
        tk.Button(root, text='7', width=8, height=2, font=("Arial", 12), command=lambda: button_click('7')),
        tk.Button(root, text='8', width=8, height=2, font=("Arial", 12), command=lambda: button_click('8')),
        tk.Button(root, text='9', width=8, height=2, font=("Arial", 12), command=lambda: button_click('9')),
        tk.Button(root, text='/', width=8, height=2, font=("Arial", 12), command=lambda: button_click('/')),
    ],
    [
        tk.Button(root, text='4', width=8, height=2, font=("Arial", 12), command=lambda: button_click('4')),
        tk.Button(root, text='5', width=8, height=2, font=("Arial", 12), command=lambda: button_click('5')),
        tk.Button(root, text='6', width=8, height=2, font=("Arial", 12), command=lambda: button_click('6')),
        tk.Button(root, text='*', width=8, height=2, font=("Arial", 12), command=lambda: button_click('*')),
    ],
    [
        tk.Button(root, text='1', width=8, height=2, font=("Arial", 12), command=lambda: button_click('1')),
        tk.Button(root, text='2', width=8, height=2, font=("Arial", 12), command=lambda: button_click('2')),
        tk.Button(root, text='3', width=8, height=2, font=("Arial", 12), command=lambda: button_click('3')),
        tk.Button(root, text='-', width=8, height=2, font=("Arial", 12), command=lambda: button_click('-')),
    ],
    [
        tk.Button(root, text='0', width=8, height=2, font=("Arial", 12), command=lambda: button_click('0')),
        tk.Button(root, text='.', width=8, height=2, font=("Arial", 12), command=lambda: button_click('.')),
        tk.Button(root, text='+', width=8, height=2, font=("Arial", 12), command=lambda: button_click('+')),
        tk.Button(root, text='=', width=8, height=2, font=("Arial", 12), command=lambda: button_click('=')),
    ],
]

# Create buttons for scientific operations
scientific_buttons = [
    [
        tk.Button(root, text='sin', width=8, height=2, font=("Arial", 12), command=lambda: button_click('sin')),
        tk.Button(root, text='cos', width=8, height=2, font=("Arial", 12), command=lambda: button_click('cos')),
        tk.Button(root, text='tan', width=8, height=2, font=("Arial", 12), command=lambda: button_click('tan')),
        tk.Button(root, text='log', width=8, height=2, font=("Arial", 12), command=lambda: button_click('log')),
    ],
    [
        tk.Button(root, text='sqrt', width=8, height=2, font=("Arial", 12), command=lambda: button_click('sqrt')),
        tk.Button(root, text='(', width=8, height=2, font=("Arial", 12), command=lambda: button_click('(')),
        tk.Button(root, text=')', width=8, height=2, font=("Arial", 12), command=lambda: button_click(')')),
        tk.Button(root, text='**', width=8, height=2, font=("Arial", 12), command=lambda: button_click('**')),
    ],
]

# Layout for standard calculator buttons
for i, button_row in enumerate(standard_buttons):
    for j, button in enumerate(button_row):
        button.grid(row=i + 1, column=j, padx=5, pady=5)

# Initially hide scientific calculator buttons
for button_row in scientific_buttons:
    for button in button_row:
        button.grid_remove()

# Create label to display output
output_label = tk.Label(root, text="", font=("Arial", 14))
output_label.grid(row=6, column=0, columnspan=5, padx=10, pady=10)

# Create menu for calculator mode
mode_var = tk.StringVar(root)
mode_var.set("Standard")
mode_menu = tk.OptionMenu(root, mode_var, "Standard", "Scientific", command=switch_mode)
mode_menu.grid(row=7, column=0, columnspan=5, pady=10)

# Run the Tkinter event loop
root.mainloop()
