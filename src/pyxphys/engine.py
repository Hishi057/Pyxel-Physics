import pyxel
from typing import List
from .collision import Collider
from .utils import clamp
import math

class GameObject:
    world : 'World'
    name : str
    is_alive : bool # 消去したければここをFalseにする
    x : float
    y : float
    vx : float
    vy : float
    mass : float
    tags : list[str]
    colliders : list[Collider]
    STILL_SHREHOLD : float
    IS_FREEZE_POSITION : bool

    def __init__(self, 
                 name : str = "",
                 x : float = 0,
                 y : float = 0,
                 vx : float = 0,
                 vy : float = 0,
                 ax : float = 0,
                 ay : float = 0,
                 mass : float = 1,
                 STILL_SHREHOLD : float = 0.5,
                 IS_FREEZE_POSITION : bool = False
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
        self.mass = mass
        self.tags = []
        self.colliders = []
        self.STILL_SHREHOLD = STILL_SHREHOLD
        self.IS_FREEZE_POSITION = IS_FREEZE_POSITION

        if self.IS_FREEZE_POSITION:
            self.mass = 1024 * 1024

    def add_collider(self, collider : Collider):
        self.colliders.append(collider)
        collider.parent = self

    def add_force(self, F_x : float, F_y : float):
        self.ax = F_x / self.mass
        self.ay = F_y / self.mass

    def update(self):
        pass
    
    def draw(self):
        pass
    
    def on_collision(self, other):
        pass