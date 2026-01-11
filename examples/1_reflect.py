import pyxphys
import pyxel

class GameManager(pyxphys.GameObject):
    counter : int
    def __init__(self):
        super().__init__()
        self.counter = 1
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            if pyxel.rndi(0, 2) <= 1:
                self.world.add_object(Ball())
            else:
                self.world.add_object(Box())
            self.counter += 1
            print(self.counter)

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

class Ball(pyxphys.GameObject):
    color : int = 6 # ボールの色
    radius : int = 8 # ボールの半径

    def __init__(self):
        super().__init__()
        self.name = "ball"
        self.x = pyxel.rndi(130, 170)
        self.y = 100
        angle = pyxel.rndi(30, 150)
        self.vx = pyxel.cos(angle) * 3 + 3
        self.vy = pyxel.rndi(0, 10) * -1
        self.add_collider(pyxphys.CircleCollider(self.radius))

    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, self.color)

class Box(pyxphys.GameObject):
    color : int = 6 # ボールの色
    radius : int = 8 # ボールの半径
    width : float = 20
    height : float = 32

    def __init__(self):
        super().__init__()
        self.name = "box"
        self.x = pyxel.rndi(130, 170)
        self.y = 100
        angle = pyxel.rndi(30, 150)
        self.vx = pyxel.cos(angle) * 3 + 3
        self.vy = pyxel.rndi(0, 10) * -1
        self.mass = 3
        self.add_collider(pyxphys.BoxCollider(self.width, self.height))

    def draw(self):
        pyxel.rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height, self.color)

class UI_text(pyxphys.GameObject):
    def __init__(self):
        super().__init__()
        self.IS_FREEZE_POSITION = True
    def draw(self):
        pyxel.text(self.x, self.y, "PRESS SPACE BUTTON", 0)

# 初期設定
app = pyxphys.App(screen_x = 300,screen_y= 300)
world = pyxphys.World(gravity = 0.9)
ui = pyxphys.World(gravity = 0)
app.add_world(world)
app.add_world(ui)

ui.add_object(UI_text())
world.add_object(GameManager())
world.add_object(Ball())
world.add_object(Wall(x = 150, y = 290, height = 30 , width = 300))
world.add_object(Wall(x = 295, y = 150, height = 300, width = 30))
world.add_object(Wall(x =  5, y = 150,  height = 300, width = 30))

app.run() # アプリを実行