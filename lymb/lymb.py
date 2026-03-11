from math import pi, sin, cos
import random
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import LineSegs, NodePath, LColor

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()

        self.camera.setPos(0, -40, 17)
        self.camera.setHpr(0, -20, 0)
        self.camLens.setFov(50)

        self.plateau_w = 30
        self.plateau_h = 30
        self.grid_cols = 20
        self.grid_rows = 20
        self.fill_ratio = 0.4

        self.plateau_origin_x = -self.plateau_w / 2
        self.plateau_origin_y = -self.plateau_h / 2
        self.surface_z = 0.1

        # Taille d'une case calculée automatiquement
        self.cell_w = self.plateau_w / self.grid_cols
        self.cell_h = self.plateau_h / self.grid_rows

        # Plateau
        plane = self.loader.loadModel("models/box")
        plane.setScale(self.plateau_w, self.plateau_h, 0.1)
        plane.setPos(self.plateau_origin_x, self.plateau_origin_y, 0)
        plane.reparentTo(self.render)

        self.create_grid(z=self.surface_z + 0.01)
        self.place_cubes()

    def create_grid(self, z=0.11):
        lines = LineSegs()
        lines.setThickness(1.5)
        lines.setColor(LColor(1, 1, 1, 0.8))

        ox = self.plateau_origin_x
        oy = self.plateau_origin_y
        pw = self.plateau_w
        ph = self.plateau_h
        cw = self.cell_w
        ch = self.cell_h

        # Lignes horizontales
        for row in range(self.grid_rows + 1):
            y = oy + row * ch
            lines.moveTo(ox,      y, z)
            lines.drawTo(ox + pw, y, z)

        # Lignes verticales
        for col in range(self.grid_cols + 1):
            x = ox + col * cw
            lines.moveTo(x, oy,      z)
            lines.drawTo(x, oy + ph, z)

        node = lines.create()
        grid_np = NodePath(node)
        grid_np.reparentTo(self.render)
        grid_np.setTransparency(True)

    def place_cubes(self):
        ox = self.plateau_origin_x
        oy = self.plateau_origin_y
        cw = self.cell_w
        ch = self.cell_h
        z_base = self.surface_z

        margin_x = cw * 0.1  # marge proportionnelle à la case
        margin_y = ch * 0.1

        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                if random.random() > self.fill_ratio:
                    continue

                x = ox + col * cw + margin_x
                y = oy + row * ch + margin_y

                cube = self.loader.loadModel("models/box")
                cube.setScale(cw - 2 * margin_x, ch - 2 * margin_y, cw - 2 * margin_x)
                cube.setPos(x, y, z_base)

                r = random.uniform(0.3, 1.0)
                g = random.uniform(0.3, 1.0)
                b = random.uniform(0.3, 1.0)
                cube.setColor(r, g, b, 1)
                cube.reparentTo(self.render)

app = MyApp()
app.run()