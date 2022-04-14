import tkinter as tk

from calculate import calculate

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.create_widgets()
        self.submit()

    def create_widgets(self):
        self.X_label = tk.Label(self, text = "Base")
        self.Y_label = tk.Label(self, text = "Height")
        
        self.X_var = tk.StringVar()
        self.Y_var = tk.StringVar()
        self.X_ent = tk.Entry(self, textvariable = self.X_var)
        self.Y_ent = tk.Entry(self, textvariable= self.Y_var)
        
        self.submit_button = tk.Button(self, text = 'Calcualte', command = self.submit)

        self.X_label.grid(row = 0, column = 0)
        self.Y_label.grid(row = 0, column = 3)
        self.X_ent.grid(row = 1, column = 0)
        self.Y_ent.grid(row = 1, column = 3)
        self.submit_button.grid(row = 2, column = 2)

    def submit(self):
        try:
            x = float(self.X_var.get())
            y = float(self.Y_var.get())
        except:
            x = 0.0
            y = 0.0

        result = calculate(float(x),float(y))
        
        self.result_title = tk.Label(self, text = "Area Size")
        self.result_title.grid(row = 3, column= 2)

        self.result_label = tk.Entry(self)
        self.result_label.insert(0, str(result))
        self.result_label.grid(row = 4, column = 2)

        self.X_var.set("")
        self.Y_var.set("")


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
    print(tk.TkVersion)