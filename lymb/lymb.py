from math import pi, sin, cos
import random
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import (
    LineSegs, NodePath, LColor,
    GeomVertexFormat, GeomVertexData, GeomVertexWriter,
    Geom, GeomTriangles, GeomNode
)

def make_gradient_cube(w, d, h):
    """Crée un cube avec dégradé blanc en haut, noir en bas."""
    fmt = GeomVertexFormat.getV3c4()
    vdata = GeomVertexData("cube", fmt, Geom.UHStatic)
    vdata.setNumRows(24)

    vertex = GeomVertexWriter(vdata, "vertex")
    color  = GeomVertexWriter(vdata, "color")

    # Couleurs selon la hauteur : blanc (z=h) → noir (z=0)
    def col(z_val):
        t = z_val / h  # 0.0 en bas, 1.0 en haut
        return (t, t, t, 1.0)

    # 6 faces, 4 sommets chacune
    # Ordre : bottom-left, bottom-right, top-right, top-left  (en coordonnées locales)
    faces = [
        # face avant  (y=0)
        [(0,0,0),(w,0,0),(w,0,h),(0,0,h)],
        # face arrière (y=d)
        [(w,d,0),(0,d,0),(0,d,h),(w,d,h)],
        # face gauche  (x=0)
        [(0,d,0),(0,0,0),(0,0,h),(0,d,h)],
        # face droite  (x=w)
        [(w,0,0),(w,d,0),(w,d,h),(w,0,h)],
        # face bas     (z=0)
        [(0,d,0),(w,d,0),(w,0,0),(0,0,0)],
        # face haut    (z=h)
        [(0,0,h),(w,0,h),(w,d,h),(0,d,h)],
    ]

    for face in faces:
        for (x, y, z) in face:
            vertex.addData3(x, y, z)
            r, g, b, a = col(z)
            color.addData4(r, g, b, a)

    tris = GeomTriangles(Geom.UHStatic)
    for i in range(6):
        base = i * 4
        # Deux triangles par face (quad)
        tris.addVertices(base+0, base+1, base+2)
        tris.addVertices(base+0, base+2, base+3)

    geom = Geom(vdata)
    geom.addPrimitive(tris)

    node = GeomNode("gradient_cube")
    node.addGeom(geom)
    return NodePath(node)


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()

        self.camera.setPos(0, -16, 40)
        self.camera.setHpr(0, -70, 0)
        self.camLens.setFov(50)

        self.plateau_w = 30
        self.plateau_h = 30
        self.grid_cols = 20
        self.grid_rows = 20
        self.patern = [
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
            1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1,
            1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1,
            1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1,
            1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1,
            1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1,
            1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1,
            1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1,
            1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1,
            1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1,
            1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1,
            1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1,
            1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1,
            1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1,
            1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1,
            1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1,
            1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1,
            1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1,
            1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1,
            0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        ]

        self.plateau_origin_x = -self.plateau_w / 2
        self.plateau_origin_y = -self.plateau_h / 2
        self.surface_z = 0.1

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

        for row in range(self.grid_rows + 1):
            y = oy + row * ch
            lines.moveTo(ox,      y, z)
            lines.drawTo(ox + pw, y, z)

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

        margin_x = cw * 0.1
        margin_y = ch * 0.1

        cube_w = cw - 2 * margin_x
        cube_d = ch - 2 * margin_y
        cube_h = cw - 2 * margin_x  # hauteur = largeur (cube)

        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                if not self.patern[row * 20 + col]:
                    continue

                x = ox + col * cw + margin_x
                y = oy + row * ch + margin_y

                cube_np = make_gradient_cube(cube_w, cube_d, cube_h)
                cube_np.setPos(x, y, z_base)
                # Désactiver l'éclairage pour que les couleurs par sommet soient visibles telles quelles
                cube_np.setLightOff()
                cube_np.reparentTo(self.render)


app = MyApp()
app.run()