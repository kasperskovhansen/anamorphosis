import tkinter as tk
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import random
import math
from geom_3d.geom_3d import *
from data_anamorphosis import Data_anamorphosis

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
from geom_3d.geom_3d import *

# Animation
# https://www.youtube.com/watch?v=ZmYPzESC5YY
import matplotlib.animation as animation

from datetime import datetime
initialTime = datetime.now()

# Opsætning
screenWidth = 850
screenHeight = 415

class GUI_anamorphosis(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        
        self.data = Data_anamorphosis()

        # Opsætning af graf.
        self.fig = plt.figure()
        # self.ax = Axes3D(self.fig)
        # self.ax.azim = -40
        # self.ax.elev = 1
        self.shouldAnimate = False
        self.animationInterval = 100
        self.cornerX = 0
        self.ani = None


        self.build_GUI()
        # self.reload3DGraph()

        # plt.show()

    def on_object_selected(self, val):
        print(val)

    def add_object(self):
        def accept():
            objType = self.type_var.get()
            objScale = scale.get()
            self.data.addObject(Object.createType(str(objType), objScale, Vector(2,2,2)))

            self.reload3DGraph()
            dlg.destroy()

        def cancel():
            dlg.destroy()

        dlg = tk.Toplevel()
        dlg.title("Tilføj objekt")

        ttk.Label(dlg, text='Type:').grid(column =0, row = 0)
        types = ["Kasse", "Kasse"]
        self.type_var = tk.StringVar(dlg)
        self.type_var.set(types[0]) # Standardværdi.
        self.opt_axes = ttk.OptionMenu(dlg, self.type_var, *types).grid(sticky='nsew',column=1, row=0)

        ttk.Label(dlg, text='Scale:').grid(column =0, row = 1)
        scale = tk.Spinbox(dlg, from_=0.1, to_=5, increment=0.1)
        scale.grid(sticky='nsew',column=1, row=1)

        ttk.Button(dlg, text="Tilføj", command=accept).grid(column=0,row=20)
        ttk.Button(dlg, text="Annuller", command=cancel).grid(column=1,row=20)
    
    def edit_object(self):
        def save():
            print(scale.get())
            dlg.destroy()

        def cancel():
            dlg.destroy()

        def spinbox_update():
            print(scale.get())

        dlg = tk.Toplevel()
        dlg.title("Rediger objekt")

        ttk.Label(dlg, text='Scale:').grid(column =0, row = 0)
        scale = tk.Spinbox(dlg, from_=0.1, to_=5, increment=0.1, command=spinbox_update)
        scale.grid(sticky='nsew',column=1, row=0)

        ttk.Button(dlg, text="Gem", command=save).grid(column=0,row=20)
        ttk.Button(dlg, text="Annuller", command=cancel).grid(column=1,row=20)

    def delete_object(self):
        def delete():
            dlg.destroy()

        def cancel():
            dlg.destroy()

        dlg = tk.Toplevel()
        dlg.title("Slet objekt")

        ttk.Label(dlg, text='Er du sikker på, at du vil slette objektet?').grid(column =0, row = 0, columnspan = 2)
       
        ttk.Button(dlg, text="Slet", command=delete).grid(column=0,row=20)
        ttk.Button(dlg, text="Annuller", command=cancel).grid(column=1,row=20)

    def show_3D(self):
        print("show 3d")

        dlg = tk.Toplevel()
        dlg.title("3D visning")
        dlg.geometry("{}x{}".format(600, 600))

        canvas = FigureCanvasTkAgg(self.fig, master=dlg)  # A tk.DrawingArea.
        canvas.draw()
        self.ax = Axes3D(self.fig)
        self.ax.azim = -40
        self.ax.elev = 1
        toolbar = NavigationToolbar2Tk(canvas, dlg)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.ani = animation.FuncAnimation(self.fig, self.update3DGraph, interval=1)
        # self.reload3DGraph()



    def show_2D(self):
        print("show 2d")


    def rotate_clock(self): # pylint: disable=E0202
        print("rotate_clock")
    
    def move_up(self): # pylint: disable=E0202
        self.cornerX += 1
        print("move_up")
        self.reloadGraph()


    def move_down(self): # pylint: disable=E0202
        print("move_down")
        self.cornerX -= 1
        self.reloadGraph()

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
        self.btn_add = ttk.Button(main_frame, text="Tilføj objekt", command=self.add_object).grid(sticky='ew', column=2, row=1, columnspan=2)
        self.btn_edit = ttk.Button(main_frame, text="Rediger objekt", command=self.edit_object).grid(sticky='ew', column=2, row=2, columnspan=2)
        self.btn_delete = ttk.Button(main_frame, text="Slet objekt", command=self.delete_object).grid(sticky='ew', column=2, row=3, columnspan=2)
        self.btn_show_3d = ttk.Button(main_frame, text="Vis 3D", command=self.show_3D).grid(sticky='ew', column=2, row=6, columnspan=2)
        self.btn_show_2d = ttk.Button(main_frame, text="Vis 2D anamorfose", command=self.show_2D).grid(sticky='ew', column=2, row=7, columnspan=2)

        # Col 3 fra venstre.
        tk.Canvas(main_frame, width=math.floor(screenWidth/2 - 20), height=0).grid(column=4, row=20, columnspan=3)        
        ttk.Label(main_frame, text="Orientation", background="white").grid(sticky='ew', column=4, row=0, columnspan=3)
        
        self.btn_rotate_clock = ttk.Button(main_frame, text="Drej med uret", command=self.rotate_clock).grid(sticky='nsew', column=4, row=1, rowspan=24)
        self.btn_move_up = ttk.Button(main_frame, text="Flyt op", command=self.move_up).grid(sticky='nsew',column=5, row=1, rowspan=6)
        ttk.Label(main_frame, text="Vælg akse:", background="white").grid(sticky='ew', column=5, row=8, rowspan=1)
        axes = ["x-akse", "x-akse", "y-akse", "z-akse"]
        variable = tk.StringVar(main_frame)
        variable.set(axes[0]) # Standardværdi.
        self.opt_axes = ttk.OptionMenu(main_frame, variable, command=self.axis_change, *axes).grid(sticky='nsew',column=5, row=10, rowspan=2)
        self.btn_move_down = ttk.Button(main_frame, text="Flyt ned", command=self.move_down).grid(sticky='nsew',column=5, row=13, rowspan=12)
        self.btn_rotate_counter = ttk.Button(main_frame, text="Drej mod uret", command=self.rotate_counter).grid(sticky='nsew',column=6, row=1, rowspan=24)

        title_frame.pack( fill=tk.X , side = tk.TOP )
        main_frame.pack(fill=tk.X, side = tk.TOP)
        self.pack()


    def reloadGraph(self):
        self.ani.event_source.start()


    def update3DGraph(self, i=0):
        self.ax.clear()
        # Plan der agerer gulv
        pPoints = [Point(self.cornerX,0,-2), Point(10,0,-2), Point(10,10,4), Point(0,10,4)]
        T = self.pointsToCoords(pPoints)
        verts = [list(zip(T[0],T[1],T[2]))]
        # Tilføj plan til tegningen.
        self.ax.add_collection3d(Poly3DCollection(verts, alpha=0.5))

        # Matematisk repræsentation af planen.
        plane = Plane.createFromThreePoints(pPoints[0], pPoints[1], pPoints[2])

        # Punkt hvorfra iagttageren observerer.
        viewPoint = Point(5,0,12)
        self.ax.scatter(viewPoint.x, viewPoint.y, viewPoint.z, color='green')


        # Punkter i 3D figuren, der senere skal vises som anamorfose.
        # Box pos
        bpX = 4
        bpY = 4
        bpZ = 4
        # Box width
        bW = 2
        figPoints = [Point(bpX, bpY, bpZ), Point(bpX + bW, bpY, bpZ), Point(bpX + bW, bpY + bW, bpZ), Point(bpX, bpY + bW, bpZ), Point(bpX, bpY, bpZ + bW), Point(bpX + bW, bpY, bpZ + bW), Point(bpX + bW, bpY + bW, bpZ + bW), Point(bpX, bpY + bW, bpZ + bW)]

        T = self.pointsToCoords(figPoints)
        # Tilføj alle punkterne til tegningen.
        self.ax.scatter(T[0], T[1], T[2], color='red')


        # Linjer mellem viewPoint og figPoints.
        lines = self.getLines(figPoints, Vector.fromPoint(viewPoint))
        coordsList = self.linesToCoords(lines)

        for line in coordsList:
            self.ax.plot(line[0], line[1], line[2], color='blue', linestyle=':')

        # Lister over punkter projiceret på planen.
        pointsOnPlane = []
        for line in lines:
            intersectionPoint = intersection(plane, line)
            if intersectionPoint:
                pointsOnPlane.append(intersectionPoint)
            else:
                print("Line is parallel")

        T = self.pointsToCoords(pointsOnPlane)
        self.ax.scatter(T[0], T[1], T[2], color='blue')

        self.ani.event_source.stop()



    def pointsToCoords(self, l: list) -> list:
        # Transponer listen med koordinatsæt, så vi får tre lister med henholdsvis x, y, og z.
        coordsList = []
        for p in l:
            coordsList.append(p.coords())
        return np.transpose(coordsList)

    def linesToCoords(self, lines: list) -> list:
        coordsList = []
        for l in lines:
            coordsList.append([[l.p0.x, l.d.x + l.p0.x], [l.p0.y, l.d.y + l.p0.y], [l.p0.z, l.d.z + l.p0.z]])
        return coordsList

    def getLines(self, figPoints: list, viewPoint: Point):
        lineList = []
        for point in figPoints:
            lineList.append(Line.createTwoPoints(point, viewPoint))
        return lineList



root = tk.Tk()
root.geometry("{}x{}".format(screenWidth, screenHeight))
root.resizable(True, True)

app = GUI_anamorphosis(root)
app.master.title('Anamorfose Tegner')
app.mainloop()

