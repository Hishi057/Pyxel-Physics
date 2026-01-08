import pyxel
from typing import List

class GameObject:
    world : 'World'
    name : str
    is_alive : bool # 消去したければここをFalseにする
    x : float
    y : float
    vx : float
    vy : float
    tags : list[str]

    def __init__(self, 
                 name : str = "",
                 x : float = 0,
                 y : float = 0,
                 vx : float = 0,
                 vy : float = 0,
                 ax : float = 0,
                 ay : float = 0,
                 ):

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
        return self

    def update(self):
        pass
    
    def draw(self):
        pass
    
    def collide(self, target):
        pass