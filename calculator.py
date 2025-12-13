import tkinter as tk
from tkinter import messagebox

# Create main window
window = tk.Tk()
window.title("Simple Calculator")
window.geometry("300x400")

# Input fields
tk.Label(window, text="First Number:").pack(pady=5)
num1_entry = tk.Entry(window, font=("Arial", 14))
num1_entry.pack(pady=5)

tk.Label(window, text="Second Number:").pack(pady=5)
num2_entry = tk.Entry(window, font=("Arial", 14))
num2_entry.pack(pady=5)

# Result label
result_label = tk.Label(window, text="Result: ", font=("Arial", 16, "bold"))
result_label.pack(pady=20)

# Calculate function
def calculate(operation):
    try:
        A = int(num1_entry.get())
        B = int(num2_entry.get())
        
        if operation == "+":
            result = A + B
            result_label.config(text=f"Result: {result}")
        
        elif operation == "-":
            result = A - B
            result_label.config(text=f"Result: {result}")
        
        elif operation == "*":
            result = A * B
            result_label.config(text=f"Result: {result}")
        
        elif operation == "/":
            if B == 0:
                messagebox.showerror("Error", "Cannot divide by zero!")
            else:
                result = A / B
                result_label.config(text=f"Result: {result}")
    
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers!")

# Operation buttons
button_frame = tk.Frame(window)
button_frame.pack(pady=10)

tk.Button(button_frame, text="+", width=5, height=2, 
          command=lambda: calculate("+")).grid(row=0, column=0, padx=5)

tk.Button(button_frame, text="-", width=5, height=2, 
          command=lambda: calculate("-")).grid(row=0, column=1, padx=5)

tk.Button(button_frame, text="*", width=5, height=2, 
          command=lambda: calculate("*")).grid(row=0, column=2, padx=5)

tk.Button(button_frame, text="/", width=5, height=2, 
          command=lambda: calculate("/")).grid(row=0, column=3, padx=5)

# Clear button
def clear_all():
    num1_entry.delete(0, tk.END)
    num2_entry.delete(0, tk.END)
    result_label.config(text="Result: ")

tk.Button(window, text="Clear", width=10, height=2, 
          command=clear_all).pack(pady=10)

# Run the application
window.mainloop()

