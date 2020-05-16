import tkinter as tk
import tkinter.ttk as ttk
import random
import math

# Opsætning
screenWidth = 850
screenHeight = 415

class GUI_anamorphosis(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.build_GUI()

    def on_object_selected(self, val):
        print(val)
        print("Selected")

    def add_object(self):
        print("Tilføj")
    
    def delete_object(self):
        print("Slet")

    def scale_up_object(self):
        print("Gør større")

    def scale_down_object(self):
        print("Gør mindre")

    def show_3D(self):
        print("show 3d")

    def show_2D(self):
        print("show 2d")


    def rotate_clock(self): # pylint: disable=E0202
        print("rotate_clock")
    
    def move_up(self): # pylint: disable=E0202
        print("move_up")

    def move_down(self): # pylint: disable=E0202
        print("move_down")

    def rotate_counter(self): # pylint: disable=E0202
        print("rotate_counter")

    def axis_change(self, val): # pylint: disable=E0202
        print(val)


    def build_GUI(self):
        # Titel.
        title_frame = tk.Frame(self)
        ttk.Label(title_frame, text="Anamorfose Tegner", background="white", font=("Arial Bold", 40)).grid(sticky='ew', column=0, row=0, columnspan=7)     
        tk.Canvas(title_frame, width=screenWidth, height=0).grid(column=0, row=1, columnspan=7)

        # Main.
        main_frame = tk.Frame(self)
        # Ensartet højde i alle cellerne.
        for colH in range(24):
            tk.Canvas(main_frame, height=5, width=0).grid(column=20, row=colH+1)


        # Col 1 fra venstre.
        tk.Canvas(main_frame, width=math.floor(screenWidth/3), height=0).grid(column=0, row=20, columnspan=2)
        ttk.Label(main_frame, text="Objekter", background="white").grid(sticky='ew', column=0, row=0, columnspan=2)
        
        s = ttk.Style()
        s.configure('Treeview', rowheight=31)
        s.configure("TSeparator", background="red")
        
        self.db_view = ttk.Treeview(main_frame, column=("column1", "column2"), show='headings')
        self.db_view.bind("<ButtonRelease-1>", self.on_object_selected)
        self.db_view.heading("#1", text="Navn")
        self.db_view.heading("#2", text="Type")
        ysb = ttk.Scrollbar(main_frame, command=self.db_view.yview, orient=tk.VERTICAL)
        self.db_view.configure(yscrollcommand=ysb.set)

        self.db_view.column("column1", width=math.floor(screenWidth/6), minwidth=math.floor(screenWidth/10), stretch=tk.NO)
        self.db_view.column("column2", width=math.floor(screenWidth/6), minwidth=math.floor(screenWidth/10), stretch=tk.NO)
        self.db_view.grid(sticky='ew', column=0, row=1, columnspan=2, rowspan=100)
        
        # Col 2 fra venstre.
        tk.Canvas(main_frame, width=math.floor(screenWidth/6), height=0).grid(column=2, row=20, columnspan=2)
        ttk.Label(main_frame, text="Funktioner", background="white").grid(sticky='ew', column=2, row=0, columnspan=2)
        
        # Funktionsknapper.
        self.add_button = ttk.Button(main_frame, text="Tilføj objekt", command=self.add_object).grid(sticky='ew', column=2, row=1, columnspan=2)
        self.delete_button = ttk.Button(main_frame, text="Slet objekt", command=self.delete_object).grid(sticky='ew', column=2, row=2, columnspan=2)
        self.scale_up_button = ttk.Button(main_frame, text="Gør større", command=self.scale_up_object).grid(sticky='ew', column=2, row=3, columnspan=2)
        self.scale_down_button = ttk.Button(main_frame, text="Gør mindre", command=self.scale_down_object).grid(sticky='ew', column=2, row=4, columnspan=2)
        self.show_3d = ttk.Button(main_frame, text="Vis 3D", command=self.show_3D).grid(sticky='ew', column=2, row=5, columnspan=2)
        self.show_2d = ttk.Button(main_frame, text="Vis 2D anamorfose", command=self.show_2D).grid(sticky='ew', column=2, row=6, columnspan=2)

        # Col 3 fra venstre.
        tk.Canvas(main_frame, width=math.floor(screenWidth/2 - 20), height=0).grid(column=4, row=20, columnspan=3)        
        ttk.Label(main_frame, text="Orientation", background="white").grid(sticky='ew', column=4, row=0, columnspan=3)
        
        self.rotate_clock = ttk.Button(main_frame, text="Drej med uret", command=self.rotate_clock).grid(sticky='nsew', column=4, row=1, rowspan=24)
        self.move_up = ttk.Button(main_frame, text="Flyt op", command=self.move_up).grid(sticky='nsew',column=5, row=1, rowspan=6)
        ttk.Label(main_frame, text="Vælg akse:", background="white").grid(sticky='ew', column=5, row=8, rowspan=1)
        axes = ["x-akse", "x-akse", "y-akse", "z-akse"]
        variable = tk.StringVar(main_frame)
        variable.set(axes[0]) # Standardværdi.
        self.w = ttk.OptionMenu(main_frame, variable, command=self.axis_change, *axes).grid(sticky='nsew',column=5, row=10, rowspan=2)
        self.move_down = ttk.Button(main_frame, text="Flyt ned", command=self.move_down).grid(sticky='nsew',column=5, row=13, rowspan=12)
        self.rotate_counter = ttk.Button(main_frame, text="Drej mod uret", command=self.rotate_counter).grid(sticky='nsew',column=6, row=1, rowspan=24)

        title_frame.pack( fill=tk.X , side = tk.TOP )
        main_frame.pack(fill=tk.X, side = tk.TOP)
        self.pack()

root = tk.Tk()
root.geometry("{}x{}".format(screenWidth, screenHeight))
root.resizable(False, False)

app = GUI_anamorphosis(root)
app.master.title('Anamorfose Tegner')
app.mainloop()