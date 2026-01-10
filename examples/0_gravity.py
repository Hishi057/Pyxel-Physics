import pyxphys 
import pyxel

class Floor(pyxphys.GameObject):
    height : int = 10
    width : int = 200
    def __init__(self, x = 0, y = 0):
        super().__init__(x = x, y = y, IS_FREEZE_POSITION = True)
        self.name = "floor"
        self.add_collider(pyxphys.BoxCollider(self.height, self.width))
    
    def draw(self):
        pyxel.rect(self.x - self.width/2, 
                   self.y - self.height/2, 
                   self.width, 
                   self.height, 
                   pyxel.COLOR_DARK_BLUE)


class Ball(pyxphys.GameObject):
    color : int = 6 # ボールの色
    radius : int = 10 # ボールの半径

    def __init__(self):
        super().__init__()
        self.name = "ball"
        self.x = pyxel.rndi(0, 199)
        self.y = 100
        angle = pyxel.rndi(30, 150)
        self.vx = pyxel.cos(angle) * 3 + 3
        self.vy = -10
        self.add_collider(pyxphys.CircleCollider(self.radius))
    
    def update(self):
        if self.x < self.radius:
            self.x = self.radius
            self.vx *= -1
        if app.screen_x - self.radius < self.x:
            self.x = app.screen_x - self.radius
            self.vx *= -1

    def draw(self):
        pyxel.circ(self.x, self.y, self.radius, self.color)

# 初期設定
app = pyxphys.App(200,200) # アプリ本体
world = pyxphys.World(gravity = 0.9) # アプリの中における世界
app.add_world(world) # ゲーム本体に、世界を追加

world.add_object(Ball()) # "world"という世界にBallオブジェクトを追加
world.add_object(Floor(x = 100, y = 180)) # "world"という世界にFloorオブジェクトを追加

app.run() # アプリを実行