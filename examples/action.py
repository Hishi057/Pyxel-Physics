import pyxphys
import pyxel

class Player(pyxphys.GameObject):
    counter : int
    width : float = 20
    height : float = 36
    def __init__(self):
        super().__init__(x = 150, y = 50)
        self.add_collider(pyxphys.BoxCollider(self.width, self.height))
    
    def update(self):
        self.vx = self.vx * -1/10
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.vy = -5
        if pyxel.btn(pyxel.KEY_D):
            self.vx = 1
        if pyxel.btn(pyxel.KEY_A):
            self.vx = -1

    def draw(self):
        pyxel.rect(self.x - self.width/2, 
                   self.y - self.height/2, 
                   self.width, 
                   self.height, 
                   pyxel.COLOR_BLACK)


class Wall(pyxphys.GameObject):
    height : float
    width : float
    def __init__(self, x = 0, y = 0, height = 10, width = 10):
        super().__init__(x = x, y = y, IS_FREEZE_POSITION = True)
        self.name = "box"
        self.height = height
        self.width = width
        self.add_collider(pyxphys.BoxCollider(self.width, self.height))
    
    def draw(self):
        pyxel.rect(self.x - self.width/2, 
                   self.y - self.height/2, 
                   self.width, 
                   self.height, 
                   pyxel.COLOR_DARK_BLUE)

# 初期設定
app = pyxphys.App(300,300)
world = pyxphys.World(gravity = 0.9)
ui = pyxphys.World(gravity = 0)
app.add_world(world)
app.add_world(ui)

world.add_object(Wall(x = 150, y = 290, height = 30 , width = 300))
world.add_object(Player())

app.run() # アプリを実行