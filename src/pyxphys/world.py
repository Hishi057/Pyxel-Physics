import pyxel
from typing import List
from .engine import GameObject
from .collision import check_collision, BoxCollider, CircleCollider
from .resolver import  resolve_box_circle, resolve_circle_circle, resolve_box_box
import math
from itertools import combinations
from .spatial import Quadtree
from .geometry import Rect, RaycastHit, Ray

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
        sub_step = 4
        dt = 1 / sub_step

        for i in range(sub_step):
            for o in self.objects:
            # 位置が固定されていなければ物理的な挙動を計算
                if o.IS_FREEZE_POSITION == False:
                    o.vx += o.ax * dt
                    o.vy += (o.ay + self.gravity) * dt
                    o.x += o.vx * dt
                    o.y += o.vy *dt

                # aabbの位置更新
                for collider in o.colliders:
                    collider.update_aabb()
            
            quadtree = self.get_quadtree()

            for o in self.objects:
                self._check_collision(o, quadtree)
        
        for o in self.objects:
            # 速度が遅過ぎたらストップ
            if math.fabs(o.vx) < o.STILL_SHREHOLD:
                o.vx = 0
            if math.fabs(o.vy) < o.STILL_SHREHOLD:
                o.vy = 0
            # 個別のupdate処理
            o.update()

    # 衝突判定
    def _check_collision(self, o : GameObject, quadtree : Quadtree):
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
                    if isinstance(c1, BoxCollider) and isinstance(c2, BoxCollider):
                        resolve_box_box(c1, c2) 
                # ユーザー設定の処理
                c1.parent.on_collision(c2.parent) 
        
        found_list = []
        for collider in o.colliders:
            quadtree.query(collider.aabb, found_list)

        for c1 in o.colliders:
            for c2 in found_list:
                handle_physics_collision(c1, c2)       

    def get_quadtree(self):
        # 四分木 の準備
        max_x : float = float('-inf')
        min_x : float = float('inf')
        max_y : float = float('-inf')
        min_y : float = float('inf')
        for o in self.objects:
            max_x = max(max_x, o.x)
            min_x = min(min_x, o.x)
            max_y = max(max_y, o.y)
            min_y = min(min_y, o.y)

        quadtree = Quadtree(Rect(min_x - 1, min_y - 1, max_x + 1, max_y + 1))
        for o in self.objects:
                for collider in o.colliders:
                    quadtree.insert((collider, collider.aabb))

        return quadtree
    
    def raycast_angle(self, x : float, y : float, angle_deg : float, max_dist=float('inf')):
        rad = math.radians(angle_deg)
        dx = math.cos(rad)
        dy = math.sin(rad)
        return self.raycast(x, y, dx, dy, max_dist)
    
    def raycast_to(self, x1 : float, y1 : float, x2 : float, y2 : float, max_dist=float('inf')):
        return self.raycast(x1, y1, x2 - x1, y2 - y1)
    
    def raycast(self, x, y, dx, dy, max_dist=float('inf')):
        ray = Ray(x, y, dx, dy)
        return self.get_quadtree().query_ray(ray, max_dist)

    def draw(self):
        for o in self.objects:
            o.draw()

    def add_object(self, object : GameObject):
        self.objects.append(object)
        object.world = self
