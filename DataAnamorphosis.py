# Datalaget for anamorfose-tegneprogrammet
class DataAnamorphosis:
    def __init__(self):
        self.figures = []
        self.selected_id = None
        self.selected_idx = 0
        
        self.fig = None
        self.ani = None
        self.axis = "x-akse"
        
        # Synsvinkel
        self.azim = -40
        self.elev = 10
        self.dist = 10
        self.axes_lim = 10
        self.hud_visible = True

        # Antal rotations-steps til en hel omgang
        self.rotation_step = 0.2

    def add_figure(self, fig):
        '''
        Tilføjer en figur til listen med figurer
        '''
        self.figures.append(fig)

    def set_selected_id(self, selected_id):
        '''
        Opdaterer variablerne med valgt index og id
        '''
        self.selected_id = selected_id
        self.selected_idx = self.get_selected_idx()

    def get_selected_idx(self):
        '''
        Returnerer indexet for figurer med det givne id
        '''
        for i in range(len(self.figures)):
            if str(self.figures[i].id) == str(self.selected_id):
                return i

    def get_figures(self):
        '''
        Returnerer alle figurer
        '''
        return self.figures

    def get_figs_of_type(self, fig_type: str):
        '''
        Returnerer en liste med alle figurer af en given type
        '''
        figures = []
        for fig in self.figures:
            if fig.fig_type == fig_type:
                figures.append(fig)
        return figures