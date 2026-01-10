import pyxel
from typing import List
from .engine import GameObject
from .collision import check_collision, BoxCollider, CircleCollider, resolve_box_circle, resolve_circle_circle
import math
from itertools import combinations

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
        sub_step = 3
        dt = 1 / sub_step
        for o in self.objects:
            # 位置が固定されていなければ物理的な挙動を計算
            if o.IS_FREEZE_POSITION == False:
                for i in range(sub_step):
                    o.vx += o.ax * dt
                    o.vy += (o.ay + self.gravity) * dt
                    o.x += o.vx * dt
                    o.y += o.vy *dt
                    self._check_collision()
                if math.fabs(o.vx / dt) < o.STILL_SHREHOLD:
                    o.vx = 0
                if math.fabs(o.vy / dt) < o.STILL_SHREHOLD:
                    o.vy = 0

            o.update()

    # 衝突判定
    def _check_collision(self):
        # 衝突時の処理
        def handle_physics_collision(c1, c2):
            if c1.parent != c2.parent and check_collision(c1, c2):
                # 物理的な挙動の計算
                if (not c1.is_trigger) and (not c2.is_trigger):
                    if isinstance(c1, CircleCollider) and isinstance(c2, CircleCollider):
                        resolve_circle_circle(c1, c2)
                    if isinstance(c1, BoxCollider) and isinstance(c2, CircleCollider):
                        resolve_box_circle(c1, c2)
                    if isinstance(c1, CircleCollider) and isinstance(c2, BoxCollider):
                        resolve_box_circle(c2, c1)        
                # ユーザー設定の処理
                c1.parent.on_collision(c2.parent) 
                c2.parent.on_collision(c1.parent) 

        all_dynamic_colliders = []
        all_static_colliders = []
        for o in self.objects:
            if o.IS_FREEZE_POSITION:
                all_static_colliders.extend(o.colliders)
            else:
                all_dynamic_colliders.extend(o.colliders)

        for c1 in all_dynamic_colliders:
            for c2 in all_static_colliders:
                handle_physics_collision(c1, c2)
            
        for c1, c2 in combinations(all_dynamic_colliders, 2):
                handle_physics_collision(c1, c2)          


    def draw(self):
        pyxel.cls(7)
        for o in self.objects:
            o.draw()

    def add_object(self, object : GameObject):
        self.objects.append(object)
        object.world = self
