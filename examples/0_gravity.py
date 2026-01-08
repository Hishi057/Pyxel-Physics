import pyxphys 
import pyxel

class Ball(pyxphys.GameObject):
    color : int = 6 # ボールの色
    radius : int = 10 # ボールの半径

    def __init__(self, world):
        super().__init__(world)
        self.name = "ball"
        self.x = pyxel.rndi(0, 199)
        self.y = 0
        angle = pyxel.rndi(30, 150)
        self.vx = pyxel.cos(angle)
        self.vy = pyxel.sin(angle)
    
    def update(self):
        if self.x < self.radius:
            self.x = self.radius
            self.vx *= -1
        if app.screen_x - self.radius < self.x:
            self.x = app.screen_x - self.radius
            self.vx *= -1
        if app.screen_y - self.radius < self.y:
            self.y = app.screen_y - self.radius 
            self.vy *= -1

    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, self.color)

app = pyxphys.App(200,200)
world = pyxphys.World(gravity = 0.9)
Ball(world)

pyxel.run(world.update, world.draw)


