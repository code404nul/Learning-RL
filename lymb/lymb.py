from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()  # Désactive le contrôle souris par défaut

        # --- Position de la caméra ---
        self.camera.setPos(0, -40, 17)  # X, Y, Z
        self.camera.setHpr(0, -20, 0)   # Heading, Pitch, Roll
        self.camLens.setFov(50)
        
        plane = self.loader.loadModel("models/box")  # selon ton install
        plane.setScale(30, 30, 0.1)
        plane.setPos(-15, -15, 0)
        plane.reparentTo(self.render)
        # Chargement de la scène


app = MyApp()
app.run()