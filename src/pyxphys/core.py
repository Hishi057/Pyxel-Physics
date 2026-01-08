import pyxel #pyxel というライブラリをインポート
import math
from typing import List

class App:
    screen_x : int
    screen_y : int
    def __init__(self,screen_x,screen_y):
        self.screen_x = screen_x
        self.screen_y = screen_y
        pyxel.init(screen_x, screen_y)

class World:
    objects : list[GameObject]
    gravity : float
    def __init__(self, gravity : float = 0):
        self.objects = []
        self.gravity = gravity
    
    def update(self):
        # is_alive = False の オブジェクトを削除する処理
        new_objects = []
        for o in self.objects:
            if o.is_alive:
                new_objects.append(o)
        self.objects = new_objects
            
        # オブジェクトごとの処理
        for o in self.objects:
            o.move()
            o.update()
    
        # 衝突の処理 
        for o1 in self.objects:
            for o2 in self.objects:
                o1.collide(o2)
    
    def draw(self):
        pyxel.cls(7)
        for o in self.objects:
            o.draw()

class GameObject:
    world : World
    name : str
    is_alive : bool # 消去したければここをFalseにする
    x : float
    y : float
    vx : float
    vy : float
    tags : list[str]

    def __init__(self, 
                 world : World,
                 name : str = "",
                 x : float = 0,
                 y : float = 0,
                 vx : float = 0,
                 vy : float = 0,
                 ax : float = 0,
                 ay : float = 0,
                 ):
        self.world = world
        world.objects.append(self)

        # 変数の設定
        self.is_alive = True
        self.name = name
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay
        self.tags = []

    
    def move(self):
        self.vx += self.ax
        self.vy += self.ay + self.world.gravity
        self.x += self.vx
        self.y += self.vy

    def update(self):
        pass
    
    def draw(self):
        pass
    
    def collide(self, target):
        pass