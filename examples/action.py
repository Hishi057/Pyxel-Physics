import pyxphys
import pyxel
import math

class Player(pyxphys.GameObject):
    counter : int
    width : float = 20
    height : float = 36
    scale_y : float

    def __init__(self):
        super().__init__(x = 150, y = 50)
        self.add_collider(pyxphys.BoxCollider(self.width, self.height))
        self.scale_y = 1
    
    def update(self):
        self.vx = self.vx * -1/10
        if pyxel.btnp(pyxel.KEY_SPACE) and self.is_ground():
            self.vy = -12
            self.scale_y = 1.3
        if pyxel.btn(pyxel.KEY_D):
            self.vx = 3
        if pyxel.btn(pyxel.KEY_A):
            self.vx = -3
        
        self.scale_y += (1.0 - self.scale_y) * 0.2

    # rayを使った接地判定
    def is_ground(self):
        raycast1 = world.raycast(self.x + self.width/2 + 2, self.y, 0, 1)
        raycast2 = world.raycast(self.x - self.width/2 - 2, self.y, 0, 1)
        if raycast1 and "map" in raycast1.obj.tags and raycast1.distance <= self.height/2 + 3:
            return True
        elif raycast2 and "map" in raycast2.obj.tags and raycast2.distance <= self.height/2 + 3:
            return True
        else:
            return False

    def draw(self):
        width = self.width / self.scale_y
        height = self.height * self.scale_y
        height_diff = height - self.height
        pyxel.rect(self.x - width/2, 
                   self.y - height/2 - height_diff, 
                   width, 
                   height, 
                   pyxel.COLOR_WHITE)
        
    def on_collision(self, other):
        if self.is_ground == False:
            self.scale_y = 0.85



class Wall(pyxphys.GameObject):
    height : float
    width : float
    def __init__(self, x = 0, y = 0, height = 10, width = 10):
        super().__init__(x = x, y = y, IS_FREEZE_POSITION = True)
        self.name = "box"
        self.height = height
        self.width = width
        self.add_collider(pyxphys.BoxCollider(self.width, self.height))
        self.tags.append("map")
    
    def draw(self):
        pyxel.rect(self.x - self.width/2, 
                   self.y - self.height/2, 
                   self.width, 
                   self.height, 
                   pyxel.COLOR_WHITE)

# 初期設定
app = pyxphys.App(screen_x=300, screen_y=300, background_color=pyxel.COLOR_BLACK)
world = pyxphys.World(gravity = 0.9)
ui = pyxphys.World(gravity = 0)
app.add_world(world)
app.add_world(ui)

world.add_object(Wall(x = 150, y = 290, height = 30 , width = 300))
world.add_object(Player())

app.run() # アプリを実行