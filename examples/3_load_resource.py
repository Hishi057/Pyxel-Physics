import pyxphys 
import pyxel

class Looper(pyxphys.GameObject):
    def __init__(self):
        super().__init__(x=100 - 8, y=0)
        self.name = "looper"
        self.time = 0
        self.vy = 1

    def update(self):
        self.time += 1
        if self.y >= 210:
            self.y = -16

    def draw(self):
        if self.time % 30 <= 15:
            pyxel.blt(self.x,self.y,0,16,0,16,16,0)
        else:
            pyxel.blt(self.x,self.y,0,0,0,16,16,0)

# 初期設定
app = pyxphys.App()
app.load_resource("assets/3_resource.pyxres")
# pyxel.load("assets/3_resource.pyxres") これはダメ。絶対パスならok
world = pyxphys.World(gravity = 0)
app.add_world(world)

world.add_object(Looper())

app.run()