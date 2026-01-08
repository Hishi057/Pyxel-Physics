import pyxel
from typing import List
from .engine import GameObject

class World:
    app : 'App'
    objects : list[GameObject]
    gravity : float
    def __init__(self, gravity : float = 0):
        self.objects = []
        self.gravity = gravity

    def update_physics(self):
        # オブジェクトを削除する処理
        new_objects = []
        for o in self.objects:
            if o.is_alive:
                new_objects.append(o)
        self.objects = new_objects

        # 物理演算
        sub_step = 10
        dt = 1 / sub_step
        for o in self.objects:
            for i in range(sub_step):
                o.vx += o.ax * dt
                o.vy += (o.ay + self.gravity) * dt
                o.x += o.vx * dt
                o.y += o.vy *dt
            o.update()
        
        # 衝突の処理 
        for o1 in self.objects:
            for o2 in self.objects:
                o1.collide(o2)

    def draw(self):
        pyxel.cls(7)
        for o in self.objects:
            o.draw()

    def add_object(self, object : GameObject):
        self.objects.append(object)
        object.world = self
