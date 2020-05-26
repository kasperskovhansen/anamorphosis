class DataAnamorphosis:
    def __init__(self):
        self.objects = []
        self.selected_id = None
        self.selected_idx = 0

        self.fig = None
        self.ani = None
        self.axis = "x-akse"
        
        # Synsvinkel.
        self.azim = -40
        self.elev = 10
        self.dist = 10
        self.axes_lim = 10
        self.hud_visible = True

        # Antal rotationer til en hel omgang.
        self.rotation_step = 0.2

    def add_object(self, obj):
        self.objects.append(obj)

    def set_selected_id(self, selected_id):
        self.selected_id = selected_id
        self.selected_idx = self.get_selected_idx()

    def get_selected_idx(self):
        for i in range(len(self.objects)):
            if str(self.objects[i].id) == str(self.selected_id):
                return i

    def get_objects(self):
        return self.objects

    def get_objs_of_type(self, obj_type: str):
        objects = []
        for obj in self.objects:
            if obj.obj_type == obj_type:
                objects.append(obj)
        return objects