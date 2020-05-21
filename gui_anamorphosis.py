import tkinter as tk
import tkinter.ttk as ttk
from tkinter import colorchooser
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

        # Plan der ikke kan slettes.
        self.data.addObject(Object.createType("Plan", 10, Vector(0,0,0), name="Plan", deleteable=False))

        # Observationspunkt, der ikke kan slettes.
        self.data.addObject(Object.createType("Observationspunkt", 1, Vector(5,5,8), name="Observationspunkt", deleteable=False))

        # Kasse, som godt kan slettes.
        self.data.addObject(Object.createType("Kasse", 2, Vector(2,1,1), name="{}. objekt".format(str(len(self.data.objects) +1))))


        # Plan 2
        # self.data.addObject(Object.createType("Plan", float(10), Vector(-5,0,5), name="{}. objekt".format(str(len(self.data.objects) +1))))
        # self.data.objects[3].applyRotation(0, math.pi/2, 0)

        # Opsætning af graf.
        self.fig = plt.figure()
        self.shouldAnimate = False
        self.animationInterval = 100
        self.cornerX = 0
        self.ani = None
        self.axis = "x-akse"

        # Antal rotationer til en hel omgang.
        self.rotationStep = 2*math.pi / 40
        
        # Synsvinkel.
        self.azim = -40
        self.elev = 10
        self.dist = 10
        self.axesLim = 10
 
        self.build_GUI()
        self.reload_table()
        self.show_3D()


    def on_object_selected(self, event):
        curItem = self.db_view.item(self.db_view.focus())['values']
        self.data.setSelectedId(curItem[2])
        
    def add_object(self):
        def accept():
            objType = self.type_var.get()
            objScale = scale.get()
            if objType == "Kasse":
                self.data.addObject(Object.createType("Kasse", float(objScale), Vector(1,1,1), name="{}. objekt".format(str(len(self.data.objects) +1))))
            elif objType == "Plan":
                self.data.addObject(Object.createType("Plan", float(objScale), Vector(0,0,0), name="{}. objekt".format(str(len(self.data.objects) +1))))
            elif objType == "Observationspunkt":
                self.data.addObject(Object.createType("Observationspunkt", float(objScale), Vector(0,0,6), name="{}. objekt".format(str(len(self.data.objects) +1))))
            elif objType == "Icosahedron":
                self.data.addObject(Object.createType("Icosahedron", float(objScale), Vector(1,1,1), name="{}. objekt".format(str(len(self.data.objects) +1))))
            
            self.reload_table()
            self.reloadGraph()
            dlg.destroy()

        def cancel():
            dlg.destroy()

        def color(self):
            color = colorchooser.askcolor()[1]

        dlg = tk.Toplevel()
        dlg.title("Tilføj objekt")

        ttk.Label(dlg, text='Type:').grid(column =0, row = 0)
        types = ["Kasse", "Kasse", "Plan", "Observationspunkt", "Icosahedron"]
        self.type_var = tk.StringVar(dlg)
        self.type_var.set(types[0]) # Standardværdi.
        self.opt_axes = ttk.OptionMenu(dlg, self.type_var, *types).grid(sticky='nsew',column=1, row=0)

        ttk.Label(dlg, text='Skalering:').grid(column =0, row = 1)
        var = tk.StringVar(root)
        var.set("2")        
        scale = tk.Spinbox(dlg, from_=0.1, to_=5, increment=0.1, textvariable=var)
        scale.grid(sticky='nsew',column=1, row=1)

        ttk.Label(dlg, text='Farve:').grid(column = 0, row = 2)
        color = "#00EE00"
        ttk.Button(dlg, text="Klik for at vælge", command=color).grid(column=1,row=2)

        ttk.Button(dlg, text="Tilføj", command=accept).grid(column=0,row=20)
        ttk.Button(dlg, text="Annuller", command=cancel).grid(column=1,row=20)
    
    def edit_object(self):
        def save():
            self.data.objects[self.data.getSelectedIdx()].scale = scale.get()
            dlg.destroy()

        def cancel():
            dlg.destroy()

        def spinbox_update():
            pass
        curItem = self.db_view.item(self.db_view.focus())['values']
        if not curItem:
            return

        dlg = tk.Toplevel()
        dlg.title("Rediger objekt")

        ttk.Label(dlg, text='Scale:').grid(column =0, row = 0)
        var = tk.DoubleVar(value=self.data.objects[self.data.getSelectedIdx()].scale)
        scale = tk.Spinbox(dlg, from_=0.1, to_=5, increment=0.1, textvariable=var, command=spinbox_update)
        scale.grid(sticky='nsew',column=1, row=0)

        ttk.Button(dlg, text="Gem", command=save).grid(column=0,row=20)
        ttk.Button(dlg, text="Annuller", command=cancel).grid(column=1,row=20)

    def delete_object(self):
        def delete():
            idx = self.data.getSelectedIdx()
            if self.data.objects[idx].deleteable == True:
                self.data.objects.pop(idx)
                self.reload_table()
                self.reloadGraph()
                dlg.destroy()

        def cancel():
            dlg.destroy()
        
        curItem = self.db_view.item(self.db_view.focus())['values']
        if not curItem:
            return
        
        dlg = tk.Toplevel()
        dlg.title("Slet objekt")

        ttk.Label(dlg, text='Er du sikker på, at du vil slette objektet "{}"?'.format(curItem[0])).grid(column =0, row = 0, columnspan = 2)
       
        ttk.Button(dlg, text="Slet", command=delete).grid(column=0,row=20)
        ttk.Button(dlg, text="Annuller", command=cancel).grid(column=1,row=20)

    def show_3D(self):
        dlg = tk.Toplevel()
        dlg.title("3D visning")
        dlg.geometry("{}x{}".format(600, 600))

        canvas = FigureCanvasTkAgg(self.fig, master=dlg)
        canvas.draw()
        # Aksen skal opsættes efter canvas, når det axes3D er indlejret i tkinter.
        self.ax = Axes3D(self.fig)
        self.resetView()

        toolbar = NavigationToolbar2Tk(canvas, dlg)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.ani = animation.FuncAnimation(self.fig, self.update3DGraph, interval=1)

    def show_2D(self):
        print("show 2d (Not implementet yet)")

    def rotate_clock(self): # pylint: disable=E0202
        xAng = 0
        yAng = 0
        zAng = 0
        if self.axis == "x-akse":
            xAng = -self.rotationStep
        elif self.axis == "y-akse":
            yAng = -self.rotationStep
        elif self.axis == "z-akse":
            zAng = -self.rotationStep
        self.data.objects[self.data.selectedIdx].applyRotation(xAng, yAng, zAng)
        self.reloadGraph()

    def move_up(self): # pylint: disable=E0202
        d = None
        if self.axis == "x-akse":
            d = Vector(1, 0, 0)
        elif self.axis == "y-akse":
            d = Vector(0, 1, 0)
        elif self.axis == "z-akse":
            d = Vector(0, 0, 1)
        
        self.data.objects[self.data.selectedIdx].translate(d)
        self.reloadGraph()

    def move_down(self): # pylint: disable=E0202        
        d = None
        if self.axis == "x-akse":
            d = Vector(-1, 0, 0)
        elif self.axis == "y-akse":
            d = Vector(0, -1, 0)
        elif self.axis == "z-akse":
            d = Vector(0, 0, -1)
        
        self.data.objects[self.data.selectedIdx].translate(d)
        self.reloadGraph()

    def rotate_counter(self): # pylint: disable=E0202
        xAng = 0
        yAng = 0
        zAng = 0
        if self.axis == "x-akse":
            xAng = self.rotationStep
        elif self.axis == "y-akse":
            yAng = self.rotationStep
        elif self.axis == "z-akse":
            zAng = self.rotationStep
        self.data.objects[self.data.selectedIdx].applyRotation(xAng, yAng, zAng)
        self.reloadGraph()

    def axis_change(self, val): # pylint: disable=E0202
        self.axis = val

    def reload_table(self):
        self.db_view.delete(*self.db_view.get_children())
        if len(self.data.objects) == 0:
            return
        for obj in self.data.objects:
            self.db_view.insert("", tk.END, values=(obj.name, obj.objType, obj.id))

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
        
        self.db_view = ttk.Treeview(main_frame, column=("column1", "column2", "column3"), show='headings')
        self.db_view.bind("<ButtonRelease-1>", self.on_object_selected)
        self.db_view.heading("#1", text="Navn")
        self.db_view.heading("#2", text="Type")
        self.db_view.heading("#3", text="Id")
        
        ysb = ttk.Scrollbar(main_frame, command=self.db_view.yview, orient=tk.VERTICAL)
        self.db_view.configure(yscrollcommand=ysb.set)

        xsb = ttk.Scrollbar(main_frame, command=self.db_view.xview, orient=tk.HORIZONTAL)
        self.db_view.configure(xscrollcommand=xsb.set)

        self.db_view.column("column1", width=math.floor(screenWidth/6), minwidth=math.floor(screenWidth/10), stretch=tk.NO)
        self.db_view.column("column2", width=math.floor(screenWidth/6/2), minwidth=math.floor(screenWidth/10), stretch=tk.NO)
        self.db_view.column("column3", width=math.floor(screenWidth/6/2), minwidth=0, stretch=tk.YES)
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
        axis_var = tk.StringVar(main_frame)
        axis_var.set(axes[0]) # Standardværdi.
        self.opt_axes = ttk.OptionMenu(main_frame, axis_var, command=self.axis_change, *axes).grid(sticky='nsew',column=5, row=10, rowspan=2)
        self.btn_move_down = ttk.Button(main_frame, text="Flyt ned", command=self.move_down).grid(sticky='nsew',column=5, row=13, rowspan=12)
        self.btn_rotate_counter = ttk.Button(main_frame, text="Drej mod uret", command=self.rotate_counter).grid(sticky='nsew',column=6, row=1, rowspan=24)

        title_frame.pack( fill=tk.X , side = tk.TOP )
        main_frame.pack(fill=tk.X, side = tk.TOP)
        self.pack()

    def reloadGraph(self):
        if self.ani:
            self.ani.event_source.start()

    def update3DGraph(self, i=0):
        # Gem, reload og indlæs indstillingerne for visningen.
        self.azim = self.ax.azim
        self.elev = self.ax.elev
        self.dist = self.ax.dist
        self.ax.clear()
        self.resetView()

        print("update3DGraph")

        for obj in self.data.objects:
            figPoints = obj.points

            if obj.objType == "Observationspunkt":
                # Tilføj punktet til tegningen.
                self.drawInSystem(obj.points[0], "Point", color="red")            

            elif obj.objType == "Kasse":
                # Segmenter i rummet.
                if obj.segments != None:
                    print(obj.segments)
                    for segment in obj.segments:
                        print(segment)
                        print("segment in obj.segments")
                        self.drawInSystem(segment, "Segment", color="green", alpha=0.3)
                        # Projicerede segmenter.
                        planes = self.data.getObjType("Plan")
                        viewPoints = self.data.getObjType("Observationspunkt")

                        # Tegn segmenter på alle planer set fra alle observationspunkter.
                        for viewPoint in viewPoints:
                            for plane in planes:
                                l1 = Line.createTwoPoints(segment.v1, viewPoint.points[0])
                                intersectionPoint1 = intersection(plane.mathPlane, l1)                            
                                
                                l2 = Line.createTwoPoints(segment.v2, viewPoint.points[0])
                                intersectionPoint2 = intersection(plane.mathPlane, l2)          

                                
                                planeVec = add(plane.mathPlane.d1, plane.mathPlane.d2)
                                isWithin1 = isWithinSegments(intersectionPoint1, planeVec, plane.segments)
                                isWithin2 = isWithinSegments(intersectionPoint2, planeVec, plane.segments)
                                print("isWithin1: {}".format(isWithin1))
                                print("isWithin2: {}".format(isWithin2))
                                seg = Segment(intersectionPoint1, intersectionPoint2)

                                for i in isWithin1[0]:                                
                                    self.drawInSystem(i, "Line", color="yellow", lineTMin=0)

                                for j in isWithin1[1]:                 
                                    self.drawInSystem(j, "Point", color="grey")

                                for k in isWithin1[2]:  
                                    self.drawInSystem(k, "Line", color="purple")


                                for i in isWithin2[0]:                                
                                    self.drawInSystem(i, "Line", color="yellow", lineTMin=0)

                                for j in isWithin2[1]:                 
                                    self.drawInSystem(j, "Point", color="grey")

                                for k in isWithin2[2]:  
                                    self.drawInSystem(k, "Line", color="purple")
                                
                                if isWithin1[3]:
                                    self.drawInSystem(intersectionPoint1, "Point", color="green")
                                else:
                                    self.drawInSystem(intersectionPoint1, "Point", color="red")                      
                                if isWithin2[3]:
                                    self.drawInSystem(intersectionPoint2, "Point", color="green")
                                else:
                                    self.drawInSystem(intersectionPoint2, "Point", color="red")                  

                                print("\nsegmentSegmentIntersection")
                                sect = segmentSegmentIntersection(seg, plane.segments)

                                # for lineSegSect in sect[0]:
                                #     self.drawInSystem(lineSegSect, "Line", color="orange")
                                
                                # print("Sect[2]: {}".format(sect[2]))
                                # for inter in sect[2]:
                                #     self.drawInSystem(inter, "Point", color="pink")

                                print()
                                print("seg: {}, sect: {}".format(seg, sect[1]))
                
                                if isWithin1[3] and isWithin2[3]:
                                    self.drawInSystem(seg, "Segment", color="darkgreen")                                                                        
                                elif not isWithin1[3] and not isWithin2[3]:
                                    pass
                                    # self.drawInSystem(Segment(seg.v1, seg.v2), "Segment", color="grey")
                                if sect[1]:
                                    self.drawInSystem(sect[1], "Point", color="pink")             
                                    if not isWithin1[3] and isWithin2[3]:                                    
                                        self.drawInSystem(Segment(sect[1], seg.v2), "Segment", color="darkgreen")
                                    elif isWithin1[3] and not isWithin2[3]:                                                                                
                                        self.drawInSystem(Segment(sect[1], seg.v1), "Segment", color="darkgreen")

                                # else:
                                #     for se in sect[0]:
                                #         self.drawInSystem(se, "Line", color="yellow")
                else:
                    for point in figPoints:
                        pass
                    # self.drawInSystem(point, "Point", color="green")                    

            elif obj.objType == "Icosahedron":
                for point in figPoints:
                    self.drawInSystem(point, "Point", color="darkgreen")
                planes = self.data.getObjType("Plan")
                viewPoints = self.data.getObjType("Observationspunkt")
                for viewPoint in viewPoints:
                    for plane in planes:
                        lines = self.getLines(figPoints, Vector.fromPoint(viewPoint.points[0]))
                        # Liste over punkter projiceret på planen.
                        for line in lines:
                            intersectionPoint = intersection(plane.mathPlane, line)
                            if intersectionPoint:
                                self.drawInSystem(intersectionPoint, "Point", color="yellow")
                            else:
                                print("Line is parallel")

            elif obj.objType == "Plan":
                # Plan der agerer gulv/lærred.
                coordsList = []
                for p in figPoints:
                    coordsList.append(p.coords())                
                T = np.transpose(coordsList)                
                verts = [list(zip(T[0],T[1],T[2]))]
                # Tilføj plan til tegningen.
                self.ax.add_collection3d(Poly3DCollection(verts, alpha=0.5))
                
                for segment in obj.segments:          
                    self.drawInSystem(segment, "Segment", color="darkblue")                                  

        self.ani.event_source.stop()

    def resetView(self):
        self.ax.azim = self.azim
        self.ax.elev = self.elev
        self.ax.dist = self.dist
        self.ax.set_xlim([0, self.axesLim])
        self.ax.set_ylim([0, self.axesLim])
        self.ax.set_zlim([0, self.axesLim])

    def drawInSystem(self, obj, objType: str, color="blue", alpha=1, lineTMin=-5, lineTMax=5) -> bool:
        if not obj: return False
        if objType == "Point":            
            self.ax.scatter(obj.x, obj.y, obj.z, color=color, alpha=alpha)
        elif objType == "Segment":
            self.ax.plot([obj.v1.x, obj.v2.x], [obj.v1.y, obj.v2.y], [obj.v1.z, obj.v2.z], color=color, alpha=alpha)
        elif objType == "Line":           
            p1 = obj.point(lineTMin)
            p2 = obj.point(lineTMax)
            self.ax.plot([p1.x, p2.x], [p1.y, p2.y], [p1.z, p2.z], color=color, alpha=alpha)
        elif objType == "Vector":
            self.ax.plot([0, obj.x], [0, obj.y], [0, obj.z], color=color, alpha=alpha)
        return True

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

