from math import pi
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import (
    LineSegs, NodePath, LColor,
    GeomVertexFormat, GeomVertexData, GeomVertexWriter,
    Geom, GeomTriangles, GeomNode,
    Camera, PerspectiveLens
)
import queue

command_queue = queue.Queue()

def make_gradient_cube(w, d, h):
    fmt = GeomVertexFormat.getV3c4()
    vdata = GeomVertexData("cube", fmt, Geom.UHStatic)
    vdata.setNumRows(24)

    vertex = GeomVertexWriter(vdata, "vertex")
    color  = GeomVertexWriter(vdata, "color")

    def col(z_val):
        t = z_val / h
        return (t, t, t, 1.0)

    faces = [
        [(0,0,0),(w,0,0),(w,0,h),(0,0,h)],
        [(w,d,0),(0,d,0),(0,d,h),(w,d,h)],
        [(0,d,0),(0,0,0),(0,0,h),(0,d,h)],
        [(w,0,0),(w,d,0),(w,d,h),(w,0,h)],
        [(0,d,0),(w,d,0),(w,0,0),(0,0,0)],
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

        # --- Paramètres plateau ---
        self.plateau_w   = 30
        self.plateau_h   = 30
        self.grid_cols   = 20
        self.grid_rows   = 20
        self.surface_z   = 0.1

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
        self.cell_w = self.plateau_w / self.grid_cols
        self.cell_h = self.plateau_h / self.grid_rows

        # --- Position robot (entrée : bas-gauche row=19, col=0) ---
        self.robot_col = 1.0
        self.robot_row = 18.0

        # --- Caméra principale : vue de dessus (moitié gauche) ---
        self.cam.node().getDisplayRegion(0).setDimensions(0, 0.5, 0, 1)
        self.camera.setPos(0, -16, 40)
        self.camera.setHpr(0, -70, 0)
        
        props = self.win.getProperties()
        win_w = props.getXSize()
        win_h = props.getYSize()
        self.camLens.setAspectRatio(2)
        self.camLens.setFov(50)

        # --- Caméra robot : 3ème personne (moitié droite) ---
        robot_lens = PerspectiveLens()
        robot_lens.setAspectRatio((win_w * 0.5) / win_h)
        robot_lens.setFov(70)
        robot_cam_node = Camera("robot_cam")
        robot_cam_node.setLens(robot_lens)
        self.robot_cam_np = self.render.attachNewNode(robot_cam_node)

        dr = self.win.makeDisplayRegion(0.5, 1, 0, 1)
        dr.setCamera(self.robot_cam_np)
        dr.setSort(1)

        # --- Scène ---
        plane = self.loader.loadModel("models/box")
        plane.setScale(self.plateau_w, self.plateau_h, 0.1)
        plane.setPos(self.plateau_origin_x, self.plateau_origin_y, 0)
        plane.reparentTo(self.render)

        self.create_grid(z=self.surface_z + 0.01)
        self.place_cubes()

        # --- Modèle robot GLTF ---
        self.model = self.loader.loadModel("models/robot.gltf")
        self.model.reparentTo(self.render)
        self.model.setHpr(0, 0, 0)
        self._sync_model()

        # --- Contrôles clavier ---
        self.accept("arrow_up",    self.move_robot, [0,  -1])
        self.accept("arrow_down",  self.move_robot, [0,   1])
        self.accept("arrow_left",  self.move_robot, [1,  0])
        self.accept("arrow_right", self.move_robot, [-1,  0])

        # --- Tâche caméra robot ---
        self.taskMgr.add(self.update_robot_cam, "update_robot_cam")
        self.taskMgr.doMethodLater(0.1, self._fix_aspect, "fix_aspect")
        # Ajouter cette tâche à la fin de __init__ :
        self.taskMgr.add(self.process_commands, "process_commands")

    def process_commands(self, task):
        """Consomme les commandes envoyées depuis d'autres fichiers."""
        while not command_queue.empty():
            dcol, drow = command_queue.get_nowait()
            self.move_robot(dcol, drow)
        return Task.cont

    def _fix_aspect(self, task):
        props = self.win.getProperties()
        win_w = props.getXSize()
        win_h = props.getYSize()
        self.camLens.setAspectRatio((win_w * 0.5) / win_h)
        return task.done
    
    def _robot_world_pos(self):
        """Retourne la position monde (x, y, z) du robot."""
        x = self.plateau_origin_x + self.robot_col * self.cell_w + self.cell_w / 2
        y = self.plateau_origin_y + self.robot_row * self.cell_h + self.cell_h / 2
        z = self.surface_z
        return x, y, z

    def _sync_model(self):
        """Déplace le modèle GLTF à la position courante du robot."""
        x, y, z = self._robot_world_pos()
        self.model.setPos(x, y, z)

    def move_robot(self, dcol, drow):
        new_col = self.robot_col + dcol
        new_row = self.robot_row + drow

        if 0 <= new_col < self.grid_cols and 0 <= new_row < self.grid_rows:
            idx = int(new_row) * self.grid_cols + int(new_col)
            if self.patern[idx] == 0:
                self.robot_col = new_col
                self.robot_row = new_row
                self._sync_model()

                if dcol ==  1: self.model.setH(270)
                if dcol == -1: self.model.setH(90)
                if drow == -1: self.model.setH(0)
                if drow ==  1: self.model.setH(180)

    def update_robot_cam(self, task):
        x, y, z = self._robot_world_pos()

        h = self.model.getH()
        angle = h * (pi / 180)
        dist_back = self.cell_h * -2.0   # un peu moins loin
        dist_up   = self.cell_h * 4.0   # beaucoup plus haut (était 1.5)

        cam_x = x + dist_back+3
        cam_y = y - dist_back
        cam_z = z + dist_up

        self.robot_cam_np.setPos(cam_x, cam_y, cam_z)
        self.robot_cam_np.lookAt(x, y, z + 0.3)

        return Task.cont

    # ------------------------------------------------------------------

    def create_grid(self, z=0.11):
        lines = LineSegs()
        lines.setThickness(1.5)
        lines.setColor(LColor(1, 1, 1, 0.8))

        ox = self.plateau_origin_x
        oy = self.plateau_origin_y
        pw = self.plateau_w
        ph = self.plateau_h

        for row in range(self.grid_rows + 1):
            y = oy + row * self.cell_h
            lines.moveTo(ox,      y, z)
            lines.drawTo(ox + pw, y, z)

        for col in range(self.grid_cols + 1):
            x = ox + col * self.cell_w
            lines.moveTo(x, oy,      z)
            lines.drawTo(x, oy + ph, z)

        NodePath(lines.create()).reparentTo(self.render)

    def place_cubes(self):
        ox     = self.plateau_origin_x
        oy     = self.plateau_origin_y
        z_base = self.surface_z

        margin_x = self.cell_w * 0.1
        margin_y = self.cell_h * 0.1
        cube_w   = self.cell_w - 2 * margin_x
        cube_d   = self.cell_h - 2 * margin_y
        cube_h   = cube_w

        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                if not self.patern[row * self.grid_cols + col]:
                    continue
                x = ox + col * self.cell_w + margin_x
                y = oy + row * self.cell_h + margin_y
                cube_np = make_gradient_cube(cube_w, cube_d, cube_h)
                cube_np.setPos(x, y, z_base)
                cube_np.setLightOff()
                cube_np.reparentTo(self.render)

if __name__ == "__main__":
    app = MyApp()
    app.run()