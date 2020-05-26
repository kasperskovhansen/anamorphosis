import tkinter as tk
import tkinter.ttk as ttk
from tkinter import colorchooser
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import random
import math
from geom_3d.geom_3d import *
from DataAnamorphosis import DataAnamorphosis

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
from geom_3d.geom_3d import *

# Animation
# https://www.youtube.com/watch?v=ZmYPzESC5YY
import matplotlib.animation as animation

class AnamorphosisGUI(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)        
        self.data = DataAnamorphosis()

        # Opsætning af den indledende "scene"
        self.data.add_object(Object.create_type("Plan", 10, Vector(0,0,0), name="Plan", deleteable=True))
        # self.data.get_objects()[0]
        self.data.add_object(Object.create_type("Observationspunkt", 1, Vector(9,-5,10), name="Observationspunkt", deleteable=True))
        self.data.add_object(Object.create_type("K", 1.5, Vector(5,1,1), name="{}. objekt".format(str(len(self.data.objects) +1))))

        # Opsætning af graf
        self.data.fig = plt.figure()
        self.data.ani = None
        self.data.axis = "x-akse"        
 
        self.build_GUI()
        self.reload_table()
        self.show_3D()

    def on_object_selected(self, event):
        '''
        Opdaterer det valgte id i datalaget
        '''
        cur_item = self.db_view.item(self.db_view.focus())['values']
        self.data.set_selected_id(cur_item[2])
        
    def add_object(self):
        '''
        Viser dialog med mulighed for at tilføje et nyt objekt
        '''
        def accept():
            '''
            Opretter det nye objekt
            '''
            obj_type = self.type_var.get()
            obj_scale = scale.get()
            if obj_type == "Kasse":
                self.data.add_object(Object.create_type("Kasse", float(obj_scale), Vector(1,1,1), name="{}. objekt".format(str(len(self.data.objects) +1))))
            if obj_type == "K":                
                self.data.add_object(Object.create_type("K", float(obj_scale), Vector(1,1,1), name="{}. objekt".format(str(len(self.data.objects) +1))))
            elif obj_type == "Plan":
                self.data.add_object(Object.create_type("Plan", float(obj_scale), Vector(0,0,0), name="{}. objekt".format(str(len(self.data.objects) +1))))
            elif obj_type == "Observationspunkt":
                self.data.add_object(Object.create_type("Observationspunkt", float(obj_scale), Vector(0,0,6), name="{}. objekt".format(str(len(self.data.objects) +1))))
            elif obj_type == "Icosahedron":
                self.data.add_object(Object.create_type("Icosahedron", float(obj_scale), Vector(1,1,1), name="{}. objekt".format(str(len(self.data.objects) +1))))
            
            self.reload_table()
            self.reload_graph()
            dlg.destroy()

        def cancel():
            dlg.destroy()

        def color(self):
            # Valg af farve virker ikke helt endnu
            color = colorchooser.askcolor()[1]            

        dlg = tk.Toplevel()
        dlg.title("Tilføj objekt")

        ttk.Label(dlg, text='Type:').grid(column =0, row = 0)
        types = ["Kasse", "Kasse", "K", "Plan", "Observationspunkt", "Icosahedron"]
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
        '''
        Viser en dialog med mulighed for at redigere et valgt objekt
        '''
        def save():
            '''
            Gemmer ændringerne til objektet
            '''
            self.data.objects[self.data.get_selected_idx()].set_scale(scale.get())
            self.reload_graph()
            dlg.destroy()

        def cancel():
            dlg.destroy()

        cur_item = self.db_view.item(self.db_view.focus())['values']
        if not cur_item:
            return

        dlg = tk.Toplevel()
        dlg.title("Rediger objekt")

        ttk.Label(dlg, text='Scale:').grid(column =0, row = 0)
        var = tk.DoubleVar(value=self.data.objects[self.data.get_selected_idx()].scale)
        scale = tk.Spinbox(dlg, from_=0.1, to_=5, increment=0.1, textvariable=var)
        scale.grid(sticky='nsew',column=1, row=0)

        ttk.Button(dlg, text="Gem", command=save).grid(column=0,row=20)
        ttk.Button(dlg, text="Annuller", command=cancel).grid(column=1,row=20)

    def delete_object(self):
        '''
        Slet et valgt objekt
        '''
        def delete():
            idx = self.data.get_selected_idx()
            if self.data.objects[idx].deleteable == True:
                self.data.objects.pop(idx)
                self.reload_table()
                self.reload_graph()
                dlg.destroy()

        def cancel():
            dlg.destroy()
        
        cur_item = self.db_view.item(self.db_view.focus())['values']
        if not cur_item:
            return
        
        dlg = tk.Toplevel()
        dlg.title("Slet objekt")

        ttk.Label(dlg, text='Er du sikker på, at du vil slette objektet "{}"?'.format(cur_item[0])).grid(column =0, row = 0, columnspan = 2)
       
        ttk.Button(dlg, text="Slet", command=delete).grid(column=0,row=20)
        ttk.Button(dlg, text="Annuller", command=cancel).grid(column=1,row=20)

    def show_3D(self):
        '''
        Åbner et vindue med 3D-koordinatsystemet
        '''
        dlg = tk.Toplevel()
        dlg.title("3D visning")
        dlg.geometry("{}x{}".format(600, 600))

        canvas = FigureCanvasTkAgg(self.data.fig, master=dlg)
        canvas.draw()
        # Aksen skal opsættes efter canvas, når det axes3D er indlejret i tkinter
        self.data.ax = Axes3D(self.data.fig)
        self.reset_view()

        toolbar = NavigationToolbar2Tk(canvas, dlg)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.data.ani = animation.FuncAnimation(self.data.fig, self.update_3D_graph, interval=1)

    def show_2D(self):
        '''
        Viser et 2D-koordinatsystem med elemementerne på en plan
        '''
        # Virker ikke endnu.
        pass
        
    def rotate_clock(self): # pylint: disable=E0202
        '''
        Roterer den valgte figur et step med uret
        '''
        x_ang = 0
        y_ang = 0
        z_ang = 0
        if self.data.axis == "x-akse":
            x_ang = -self.data.rotation_step
        elif self.data.axis == "y-akse":
            y_ang = -self.data.rotation_step
        elif self.data.axis == "z-akse":
            z_ang = -self.data.rotation_step
        self.data.objects[self.data.selected_idx].apply_rotation(x_ang, y_ang, z_ang)
        self.reload_graph()

    def move_up(self): # pylint: disable=E0202
        '''
        Flytter den valgte figur et step opad
        '''
        d = None
        if self.data.axis == "x-akse":
            d = Vector(1, 0, 0)
        elif self.data.axis == "y-akse":
            d = Vector(0, 1, 0)
        elif self.data.axis == "z-akse":
            d = Vector(0, 0, 1)
        
        self.data.objects[self.data.selected_idx].translate(d)
        self.reload_graph()

    def move_down(self): # pylint: disable=E0202      
        '''
        Flytter den valgte figur et step opad
        '''  
        d = None
        if self.data.axis == "x-akse":
            d = Vector(-1, 0, 0)
        elif self.data.axis == "y-akse":
            d = Vector(0, -1, 0)
        elif self.data.axis == "z-akse":
            d = Vector(0, 0, -1)
        
        self.data.objects[self.data.selected_idx].translate(d)
        self.reload_graph()

    def toggle_visibility(self):
        '''
        Slår synligheden af det valgte objekt til eller fra
        '''
        idx = self.data.get_selected_idx()
        if self.data.objects[idx].visible == True:
            self.data.objects[idx].visible == False

        self.data.objects[idx].visible = False if self.data.objects[idx].visible else True
            
        self.reload_graph()

    def toggle_anamorphosis(self):
        '''
        Slår synligheden af anamorfosetegningen dannet af det valgte objekt til eller fra
        '''
        idx = self.data.get_selected_idx()
        if self.data.objects[idx].anamorphosis_visible == True:
            self.data.objects[idx].anamorphosis_visible == False

        self.data.objects[idx].anamorphosis_visible = False if self.data.objects[idx].anamorphosis_visible else True
            
        self.reload_graph()

    def toggle_hud(self):
        '''
        Slår synligheden af gitterlinjer i koordinatsystemet til eller fra
        '''
        self.data.hud_visible = False if self.data.hud_visible else True
        print(self.data.hud_visible) 
        self.reload_graph()       
            
    def reset_view(self):
        '''
        Indstiller koordinatsystemet til de gemte parametre
        '''
        self.data.ax.azim = self.data.azim
        self.data.ax.elev = self.data.elev
        self.data.ax.dist = self.data.dist
        self.data.ax.set_xlim([0, self.data.axes_lim])
        self.data.ax.set_ylim([0, self.data.axes_lim])
        self.data.ax.set_zlim([0, self.data.axes_lim])
        
        if self.data.hud_visible:     
            self.data.ax.grid(True)            
        else:
            self.data.ax.grid(False)           

    def rotate_counter(self): # pylint: disable=E0202
        '''
        Roterer den valgte figur et step mod uret
        '''
        x_ang = 0
        y_ang = 0
        z_ang = 0
        if self.data.axis == "x-akse":
            x_ang = self.data.rotation_step
        elif self.data.axis == "y-akse":
            y_ang = self.data.rotation_step
        elif self.data.axis == "z-akse":
            z_ang = self.data.rotation_step
        self.data.objects[self.data.selected_idx].apply_rotation(x_ang, y_ang, z_ang)
        self.reload_graph()

    def axis_change(self, val): # pylint: disable=E0202
        '''
        Skifter den valgte akse
        '''
        self.data.axis = val

    def reload_table(self):
        '''
        Genindlæser tabellen med objekter
        '''
        self.db_view.delete(*self.db_view.get_children())
        if len(self.data.objects) == 0:
            return
        for obj in self.data.objects:
            self.db_view.insert("", tk.END, values=(obj.name, obj.obj_type, obj.id))

    def build_GUI(self):
        '''
        Bygger den grafiske brugerflade
        '''
        # Titel.
        title_frame = tk.Frame(self)
        ttk.Label(title_frame, text="Anamorfose Tegner", background="white", font=("Arial Bold", 40)).grid(sticky='ew', column=0, row=0, columnspan=7)     
        tk.Canvas(title_frame, width=screen_width, height=0).grid(column=0, row=1, columnspan=7)

        # Main.
        main_frame = tk.Frame(self)
        # Ensartet højde i alle cellerne.
        for colH in range(24):
            tk.Canvas(main_frame, height=5, width=0).grid(column=20, row=colH+1)

        # Col 1 fra venstre.
        tk.Canvas(main_frame, width=math.floor(screen_width/3), height=0).grid(column=0, row=20, columnspan=2)
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

        self.db_view.column("column1", width=math.floor(screen_width/6), minwidth=math.floor(screen_width/10), stretch=tk.NO)
        self.db_view.column("column2", width=math.floor(screen_width/6/2), minwidth=math.floor(screen_width/10), stretch=tk.NO)
        self.db_view.column("column3", width=math.floor(screen_width/6/2), minwidth=0, stretch=tk.YES)
        self.db_view.grid(sticky='ew', column=0, row=1, columnspan=2, rowspan=100)
        
        # Col 2 fra venstre.
        tk.Canvas(main_frame, width=math.floor(screen_width/6), height=0).grid(column=2, row=20, columnspan=2)
        ttk.Label(main_frame, text="Funktioner", background="white").grid(sticky='ew', column=2, row=0, columnspan=2)
        
        # Funktionsknapper.
        self.btn_add = ttk.Button(main_frame, text="Tilføj objekt", command=self.add_object).grid(sticky='ew', column=2, row=1, columnspan=2)
        self.btn_edit = ttk.Button(main_frame, text="Rediger objekt", command=self.edit_object).grid(sticky='ew', column=2, row=2, columnspan=2)
        self.btn_delete = ttk.Button(main_frame, text="Slet objekt", command=self.delete_object).grid(sticky='ew', column=2, row=3, columnspan=2)
        self.btn_visible = ttk.Button(main_frame, text="Ændr synlighed", command=self.toggle_visibility).grid(sticky='ew', column=2, row=4, columnspan=2)
        self.btn_anamorphosis = ttk.Button(main_frame, text="Anamorfose synlighed", command=self.toggle_anamorphosis).grid(sticky='ew', column=2, row=5, columnspan=2)

        self.btn_hud = ttk.Button(main_frame, text="Ændr HUD synlighed", command=self.toggle_hud).grid(sticky='ew', column=2, row=6, columnspan=2)

        self.btn_show_3d = ttk.Button(main_frame, text="Vis 3D", command=self.show_3D).grid(sticky='ew', column=2, row=7, columnspan=2)
        self.btn_show_2d = ttk.Button(main_frame, text="Vis 2D anamorfose", command=self.show_2D).grid(sticky='ew', column=2, row=8, columnspan=2)

        # Col 3 fra venstre.
        tk.Canvas(main_frame, width=math.floor(screen_width/2 - 20), height=0).grid(column=4, row=20, columnspan=3)        
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

    def reload_graph(self):
        '''
        Genindlæser koordinatsystemet med de seneste ændringer til objekterne
        '''
        if self.data.ani:
            self.data.ani.event_source.start()

    def update_3D_graph(self, i=0):
        '''
        Indlæser alle objekter i koordinatsystemet fra datalaget
        '''
        # Gem, reload og indlæs indstillingerne for visningen.
        self.data.azim = self.data.ax.azim
        self.data.elev = self.data.ax.elev
        self.data.dist = self.data.ax.dist
        self.data.ax.clear()
        self.reset_view()

        for obj in self.data.objects:
            figPoints = obj.points
            # print(obj.obj_type)
            if obj.obj_type == "Observationspunkt":
                # Tilføj punktet til tegningen.
                if obj.visible == True:
                    self.draw_in_system(obj.points[0], "Point", color="red")            

            elif obj.obj_type == "Kasse" or obj.obj_type == "K":
                # Segmenter i rummet.
                if obj.segments != None:
                    for segment in obj.segments:
                        # print(segment)
                        # print("segment in obj.segments")
                        if obj.visible == True:
                            self.draw_in_system(segment, "Segment", alpha=0.5, color=segment.color)
                        # Projicerede segmenter.
                        if obj.anamorphosis_visible == False:
                            continue
                        planes = self.data.get_objs_of_type("Plan")
                        viewPoints = self.data.get_objs_of_type("Observationspunkt")

                        # Tegn segmenter på alle planer set fra alle observationspunkter.
                        for viewPoint in viewPoints:
                            for plane in planes:
                                # print("ViewPoint plane loop")
                                l1 = Line.create_two_points(segment.v1, viewPoint.points[0])
                                intersectionPoint1 = plane_line_intersection(plane.mathPlane, l1)                            
                                
                                l2 = Line.create_two_points(segment.v2, viewPoint.points[0])
                                intersectionPoint2 = plane_line_intersection(plane.mathPlane, l2)

                                planeVec = add(plane.mathPlane.d1, plane.mathPlane.d2)
                                                           
                                isWithin1 = is_within_segments(intersectionPoint1, planeVec, plane.segments)
                                isWithin2 = is_within_segments(intersectionPoint2, planeVec, plane.segments)                                
                                seg = Segment(intersectionPoint1, intersectionPoint2)

                                sect = segment_segments_intersection(seg, plane.segments)
                
                                if isWithin1 and isWithin2:
                                    self.draw_in_system(seg, "Segment", color=segment.color)                                
                                if sect[1]:                                    
                                    if not isWithin1 and isWithin2:                                    
                                        self.draw_in_system(Segment(sect[1], seg.v2), "Segment", color=segment.color)
                                    elif isWithin1 and not isWithin2:                                                                                
                                        self.draw_in_system(Segment(sect[1], seg.v1), "Segment", color=segment.color)
                else:
                    for point in figPoints:                        
                        self.draw_in_system(point, "Point", color="green")                    

            elif obj.obj_type == "Icosahedron":
                if obj.visible == True:                          
                    for point in figPoints:
                        self.draw_in_system(point, "Point", color="darkgreen")
                if obj.anamorphosis_visible == False:
                    continue
                planes = self.data.get_objs_of_type("Plan")
                viewPoints = self.data.get_objs_of_type("Observationspunkt")
                for viewPoint in viewPoints:
                    for plane in planes:
                        lines = []
                        for point in figPoints:
                            lines.append(Line.create_two_points(point, viewPoint.points[0]))                        
                        # Liste over punkter projiceret på planen.
                        for line in lines:
                            intersectionPoint = plane_line_intersection(plane.mathPlane, line)
                            if intersectionPoint:
                                self.draw_in_system(intersectionPoint, "Point", color="yellow")                            

            elif obj.obj_type == "Plan":
                if obj.visible == True:                           
                    # Plan der agerer gulv/lærred.
                    coordsList = []
                    for p in figPoints:
                        coordsList.append(p.coords())  
                    T = np.transpose(coordsList)        
                    verts = [list(zip(T[0],T[1],T[2]))]                    
                    # Tilføj plan til tegningen.
                    self.data.ax.add_collection3d(Poly3DCollection(verts, alpha=0.4))                    
                    for segment in obj.segments:          
                        self.draw_in_system(segment, "Segment", color="darkblue")                                  
        self.data.ani.event_source.stop()

    def draw_in_system(self, obj, obj_type: str, color="black", alpha=1, lineTMin=-5, lineTMax=5, linewidth=2) -> bool:
        '''
        Tegner et objekt af en given type i koordinatsystemet
        '''
        if not obj: return False
        if obj_type == "Point":            
            self.data.ax.scatter(obj.x, obj.y, obj.z, color=color, alpha=alpha, linewidth=linewidth)
        elif obj_type == "Segment":
            self.data.ax.plot([obj.v1.x, obj.v2.x], [obj.v1.y, obj.v2.y], [obj.v1.z, obj.v2.z], color=color, alpha=alpha, linewidth=linewidth)
        elif obj_type == "Line":           
            p1 = obj.point(lineTMin)
            p2 = obj.point(lineTMax)
            self.data.ax.plot([p1.x, p2.x], [p1.y, p2.y], [p1.z, p2.z], color=color, alpha=alpha, linewidth=linewidth)
        elif obj_type == "Vector":
            self.data.ax.plot([0, obj.x], [0, obj.y], [0, obj.z], color=color, alpha=alpha, linewidth=linewidth)
        return True    

# Opsætning
root = tk.Tk()
screen_width = 850
screen_height = 415
root.geometry("{}x{}".format(screen_width, screen_height))
root.resizable(True, True)

app = AnamorphosisGUI(root)
app.master.title('Anamorfose Tegner')
app.mainloop()