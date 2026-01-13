import pyxphys
import pyxel
import math

class Nail(pyxphys.GameObject):
    color : int = pyxel.COLOR_CYAN
    radius : int = 8

    def __init__(self):
        super().__init__(x = 150, y = 30)
        self.name = "nail"
        self.IS_FREEZE_POSITION = True
        self.add_collider(pyxphys.CircleCollider(self.radius, restitution=1.0))

    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, self.color)

class Ball(pyxphys.GameObject):
    color : int = pyxel.COLOR_DARK_BLUE
    radius : int = 8

    def __init__(self):
        super().__init__(x = pyxel.rndi(170,230), y = 130)
        self.name = "ball"
        self.IS_FREEZE_POSITION = False
        self.add_collider(pyxphys.CircleCollider(self.radius, restitution=1.0))

    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, self.color)

class Spring(pyxphys.GameObject):
    length : float = 100
    k : float = 1 / 200
    object1 : pyxphys.GameObject
    object2 : pyxphys.GameObject

    def __init__(self, object1, object2):
        super().__init__(x = 150, y = 30)
        self.name = "spring"
        self.object1 = object1
        self.object2 = object2
    
    def update(self):
        rx = self.object2.x - self.object1.x
        ry = self.object2.y - self.object1.y
        d = math.sqrt(rx ** 2 + ry ** 2)
        nx = rx / d
        ny = ry / d

        displacement = d - self.length
        force = self.k * displacement
        fx = nx * force
        fy = ny * force

        self.object1.add_force(fx, fy)
        self.object2.add_force(-fx, -fy)

    def draw(self):
        pyxel.line(object1.x, object1.y, object2.x, object2.y, pyxel.COLOR_BLACK)

# 初期設定
app = pyxphys.App(screen_x = 300,screen_y= 300)
world = pyxphys.World(gravity = 0.5)
ui = pyxphys.World(gravity = 0)
app.add_world(world)
app.add_world(ui)

object1 = Ball()
object2 = Nail()
world.add_object(object1)
world.add_object(object2)
world.add_object(Spring(object1, object2))
world.add_object(Ball())

app.run() # アプリを実行