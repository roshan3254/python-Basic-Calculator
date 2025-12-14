import tkinter as tk
from tkinter import ttk
import math
import re

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("AstroCalc Pro - Scientific Calculator")
        self.root.geometry("400x670")
        self.root.minsize(300,500)
        self.root.resizable(False, False)
        self.root.configure(bg='#1a1a2e')
        
        # Variables
        self.expression = ""
        self.memory = 0
        self.angle_mode = "deg"  # deg or rad
        
        # Physics Constants
        self.constants = {
            'c': 299792458,  # Speed of light (m/s)
            'G': 6.67430e-11,  # Gravitational constant
            'h': 6.62607015e-34,  # Planck constant
            'k': 1.380649e-23,  # Boltzmann constant
            'e': 2.71828182845904523536,  # Euler's number
            'π': math.pi
        }
        
        self.create_widgets()
    
    def create_widgets(self):
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        
        # Display Frame
        display_frame = tk.Frame(self.root, bg='#16213e', bd=10)
        display_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Expression display (smaller)
        self.expr_label = tk.Label(
            display_frame, 
            text="", 
            font=('Consolas', 12),
            bg='#16213e', 
            fg='#94a3b8',
            anchor='e',
            padx=10
        )
        self.expr_label.pack(fill=tk.BOTH, expand=True)
        
        # Result display (larger)
        self.result_label = tk.Label(
            display_frame, 
            text="0", 
            font=('Consolas', 28, 'bold'),
            bg='#16213e', 
            fg='#00d9ff',
            anchor='e',
            padx=10
        )
        self.result_label.pack(fill=tk.BOTH, expand=True)
        
        # Mode indicator
        self.mode_label = tk.Label(
            display_frame,
            text=f"Mode: {self.angle_mode.upper()} | Memory: {self.memory}",
            font=('Arial', 9),
            bg='#16213e',
            fg='#94a3b8',
            anchor='w',
            padx=10
        )
        self.mode_label.pack(fill=tk.X)
        
        # Button Frame
        button_frame = tk.Frame(self.root, bg='#1a1a2e')
        button_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Button layout
        buttons = [
            # Row 1: Memory and Constants
            [('MC', '#0f3460', 1), ('MR', '#0f3460', 1), ('M+', '#0f3460', 1), ('M-', '#0f3460', 1), ('π', '#533483', 1)],
            # Row 2: Advanced functions
            [('sin', '#533483', 1), ('cos', '#533483', 1), ('tan', '#533483', 1), ('√', '#533483', 1), ('x²', '#533483', 1)],
            # Row 3: More functions
            [('log', '#533483', 1), ('ln', '#533483', 1), ('eˣ', '#533483', 1), ('xʸ', '#533483', 1), ('1/x', '#533483', 1)],
            # Row 4: Additional functions
            [('(', '#0f3460', 1), (')', '#0f3460', 1), ('n!', '#533483', 1), ('DEG/RAD', '#0f3460', 1), ('C', '#e94560', 1)],
            # Row 5: Numbers
            [('7', '#16213e', 1), ('8', '#16213e', 1), ('9', '#16213e', 1), ('÷', '#e94560', 1), ('⌫', '#e94560', 1)],
            # Row 6: Numbers
            [('4', '#16213e', 1), ('5', '#16213e', 1), ('6', '#16213e', 1), ('×', '#e94560', 1), ('|x|', '#533483', 1)],
            # Row 7: Numbers
            [('1', '#16213e', 1), ('2', '#16213e', 1), ('3', '#16213e', 1), ('-', '#e94560', 1), ('e', '#533483', 1)],
            # Row 8: Bottom row
            [('0', '#16213e', 2), ('.', '#16213e', 1), ('+', '#e94560', 1), ('=', '#00d9ff', 1)]
        ]
        
        for i, row in enumerate(buttons):
            col = 0
            for btn_text, color, colspan in row:
                btn = tk.Button(
                    button_frame,
                    text=btn_text,
                    font=('Arial', 12, 'bold'),
                    bg=color,
                    fg='white',
                    activebackground='#00d9ff',
                    activeforeground='white',
                    bd=0,
                    command=lambda x=btn_text: self.on_button_click(x),
                    cursor='hand2'
                )
                btn.grid(row=i, column=col, columnspan=colspan, sticky='nsew', padx=2, pady=2)
                col += colspan
        
        # Configure grid weights
        for i in range(8):
            button_frame.grid_rowconfigure(i, weight=1)
        for i in range(5):
            button_frame.grid_columnconfigure(i, weight=1)
    
    def on_button_click(self, char):
        if char == 'C':
            self.clear()
        elif char == '=':
            self.calculate()
        elif char == '⌫':
            self.backspace()
        elif char == 'MC':
            self.memory = 0
            self.update_mode_display()
        elif char == 'MR':
            self.expression += str(self.memory)
            self.update_display()
        elif char == 'M+':
            try:
                self.memory += float(self.result_label.cget("text"))
                self.update_mode_display()
            except:
                pass
        elif char == 'M-':
            try:
                self.memory -= float(self.result_label.cget("text"))
                self.update_mode_display()
            except:
                pass
        elif char == 'DEG/RAD':
            self.angle_mode = 'rad' if self.angle_mode == 'deg' else 'deg'
            self.update_mode_display()
        elif char in ['sin', 'cos', 'tan', 'log', 'ln', '√', 'eˣ', 'n!', '1/x', '|x|']:
            self.add_function(char)
        elif char == 'x²':
            self.expression += '**2'
            self.update_display()
        elif char == 'xʸ':
            self.expression += '**'
            self.update_display()
        elif char == 'π':
            self.expression += str(math.pi)
            self.update_display()
        elif char == 'e':
            self.expression += str(math.e)
            self.update_display()
        elif char == '÷':
            self.expression += '/'
            self.update_display()
        elif char == '×':
            self.expression += '*'
            self.update_display()
        else:
            self.expression += str(char)
            self.update_display()
    
    def add_function(self, func):
        if func == '√':
            self.expression += 'sqrt('
        elif func == 'eˣ':
            self.expression += 'exp('
        elif func == 'n!':
            self.expression += 'factorial('
        elif func == '1/x':
            self.expression += '1/('
        elif func == '|x|':
            self.expression += 'abs('
        else:
            self.expression += f'{func}('
        self.update_display()
    
    def calculate(self):
        try:
            # Replace functions with math module equivalents
            expr = self.expression
            
            # Handle trigonometric functions
            if self.angle_mode == 'deg':
                expr = re.sub(r'sin\((.*?)\)', r'math.sin(math.radians(\1))', expr)
                expr = re.sub(r'cos\((.*?)\)', r'math.cos(math.radians(\1))', expr)
                expr = re.sub(r'tan\((.*?)\)', r'math.tan(math.radians(\1))', expr)
            else:
                expr = expr.replace('sin', 'math.sin')
                expr = expr.replace('cos', 'math.cos')
                expr = expr.replace('tan', 'math.tan')
            
            # Replace other functions
            expr = expr.replace('log', 'math.log10')
            expr = expr.replace('ln', 'math.log')
            expr = expr.replace('sqrt', 'math.sqrt')
            expr = expr.replace('exp', 'math.exp')
            expr = expr.replace('factorial', 'math.factorial')
            expr = expr.replace('abs', 'abs')
            
            # Evaluate
            result = eval(expr)
            
            # Format result
            if isinstance(result, float):
                if abs(result) > 1e6 or (abs(result) < 1e-4 and result != 0):
                    result_str = f"{result:.6e}"
                else:
                    result_str = f"{result:.10g}"
            else:
                result_str = str(result)
            
            self.result_label.config(text=result_str)
            self.expression = result_str
            
        except Exception as e:
            self.result_label.config(text="Error")
            self.expression = ""
    
    def clear(self):
        self.expression = ""
        self.result_label.config(text="0")
        self.expr_label.config(text="")
    
    def backspace(self):
        self.expression = self.expression[:-1]
        self.update_display()
        if not self.expression:
            self.result_label.config(text="0")
    
    def update_display(self):
        display_text = self.expression if self.expression else "0"
        self.expr_label.config(text=display_text)
    
    def update_mode_display(self):
        self.mode_label.config(text=f"Mode: {self.angle_mode.upper()} | Memory: {self.memory:.4g}")

if __name__ == "__main__":
    root = tk.Tk()
    calculator = ScientificCalculator(root)
    root.mainloop()