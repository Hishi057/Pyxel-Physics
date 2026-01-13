from .utils import distance, clamp
import math
from .constants import CombineMode
from .geometry import Ray, Rect, RaycastHit
import pyxel

class Collider:
    parent : "GameObject"
    is_trigger : bool
    aabb : Rect
    restitution : float # 反発係数
    restitution_combine_mode : int # 反発係数の計算方法
    restitution_priority : int # 高い方が強い

    def __init__(self, 
                 offset_x=0, 
                 offset_y=0, 
                 tag="", 
                 is_trigger = False, 
                 restitution = 0.1, 
                 restitution_combine_mode = CombineMode.MAX,
                 restitution_priority = 0
                 ):
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.tag = tag
        self.parent = None
        self.is_trigger = is_trigger
        self.aabb = Rect(0,0,0,0)
        self.restitution = restitution
        self.restitution_combine_mode = restitution_combine_mode
        self.restitution_priority = restitution_priority


    # ある点がCollisionの中に入っているかどうか返す
    def contains(self, x : float, y : float):
        pass

    # AABBの当たり判定を更新
    def update_aabb(self):
        pass

    def intersect_ray(self, ray):
        pass
    
    # デバッグ用
    def draw_debug(self):
        pass

class CircleCollider(Collider):
    radius : float
    def __init__(self, 
                 radius, 
                 **kwargs):
        super().__init__(**kwargs)
        self.radius = radius

    # 世界（絶対）座標での中心位置を返す
    @property
    def center_x(self):
        return self.parent.x + self.offset_x
    @property
    def center_y(self):
        return self.parent.y + self.offset_y
    
    def contains(self, x : float, y : float):
        if distance(self.center_x, self.center_y, x, y) <= self.radius:
            return True
        return False
    
    def update_aabb(self):
        self.aabb = Rect(self.center_x - self.radius
                         ,self.center_y - self.radius 
                         ,self.radius * 2
                         ,self.radius * 2
                         )
    
    def intersect_ray(self, ray : Ray):
        # レイの原点から円の中心へのベクトル
        oc_x = ray.ox - self.center_x
        oc_y = ray.oy - self.center_y
        
        # 2次方程式の係数とへん別式
        a = ray.dx * ray.dx + ray.dy * ray.dy
        b = 2.0 * (oc_x * ray.dx + oc_y * ray.dy)
        c = oc_x * oc_x + oc_y * oc_y - self.radius * self.radius
        discriminant = b * b - 4 * a * c
        
        # 交差しない
        if discriminant < 0:
            return None
        
        # 2つの解を計算
        sqrt_disc = math.sqrt(discriminant)
        t1 = (-b - sqrt_disc) / (2 * a)
        t2 = (-b + sqrt_disc) / (2 * a)
        
        # 最も近い正の解を選択
        t = None
        if t1 > 0:
            t = t1
        elif t2 > 0:
            t = t2
        else:
            return None
        
        # 衝突地点
        hit_x = ray.ox + t * ray.dx
        hit_y = ray.oy + t * ray.dy
        
        # 法線（円の中心から衝突点への単位ベクトル）
        normal_x = (hit_x - self.center_x) / self.radius
        normal_y = (hit_y - self.center_y) / self.radius
        
        return RaycastHit(None, t, (hit_x, hit_y), (normal_x, normal_y))

    def draw_debug(self, color = pyxel.COLOR_RED):
        pyxel.circb(self.center_x, self.center_y, self.radius, color)


#
# offset を中心に、縦height, 横width の長方形のCollider
#
class BoxCollider(Collider):
    height : float
    width : float
    def __init__(self, 
                 width, 
                 height, 
                 **kwargs):
        super().__init__(**kwargs)
        self.height = height
        self.width = width

    # 世界（絶対）座標での中心位置を返す
    @property
    def center_x(self):
        return self.parent.x + self.offset_x
    @property
    def center_y(self):
        return self.parent.y + self.offset_y
    
    def update_aabb(self):
        self.aabb = Rect(self.center_x - self.width/2
                         ,self.center_y - self.height/2 
                         ,self.width
                         ,self.height
                         )
    
    def contains(self, x : float, y : float):
        pass
    

    def intersect_ray(self, ray : Ray):
        self.update_aabb()
        rect = self.aabb
        # スラブ計算
        tx1 = (rect.x - ray.ox) * ray.inv_dx
        tx2 = (rect.x + rect.w - ray.ox) * ray.inv_dx
        tmin = min(tx1, tx2)
        tmax = max(tx1, tx2)

        ty1 = (rect.y - ray.oy) * ray.inv_dy
        ty2 = (rect.y + rect.h - ray.oy) * ray.inv_dy
        t_near = max(tmin, min(ty1, ty2))
        t_far = min(tmax, max(ty1, ty2))

        # 交差判定
        if t_near > t_far or t_far <= 0:
            return None
        
        # 衝突地点
        hit_x = ray.ox + t_near * ray.dx
        hit_y = ray.oy + t_near * ray.dy

        # 法線
        if tmin > min(ty1, ty2):
            normal = (-1, 0) if ray.dx > 0 else (1, 0)
        else:
            normal = (0, -1) if ray.dy > 0 else (0, 1)
        if t_near < 0:
            normal = (0, 0) 

        return RaycastHit(None, t_near, (hit_x, hit_y), normal)

    def draw_debug(self, color = pyxel.COLOR_RED):
        pyxel.rectb(self.center_x - self.width/2, self.center_y - self.height/2, self.width, self.height, color)


# 2つのColliderの衝突判定
def check_collision(c1, c2):
    if isinstance(c1, CircleCollider) and isinstance(c2, CircleCollider):
        return _check_circle_circle(c1, c2)
    if isinstance(c1, BoxCollider) and isinstance(c2, BoxCollider):
        return _check_box_box(c1, c2)
    if isinstance(c1, BoxCollider) and isinstance(c2, CircleCollider):
        return _check_box_circle(c1, c2)
    if isinstance(c1, CircleCollider) and isinstance(c2, BoxCollider):
        return _check_box_circle(c2, c1)
    return False

def _check_circle_circle(c1, c2):
    dx = c1.center_x - c2.center_x
    dy = c1.center_y - c2.center_y
    dist_sq = dx**2 + dy**2
    return dist_sq < (c1.radius + c2.radius)**2

def _check_box_box(box1, box2):
    return (abs(box1.center_x - box2.center_x) < (box1.width + box2.width) / 2 and
            abs(box1.center_y - box2.center_y) < (box1.height + box2.height) / 2)

def _check_box_circle(box, circle):
    
    # 円の中心から矩形の最も近い点を見つける
    closest_x = clamp(circle.center_x, box.center_x - box.width/2, box.center_x + box.width/2)
    closest_y = clamp(circle.center_y, box.center_y - box.height/2, box.center_y + box.height/2)
    
    # 最も近い点と円の中心の距離を計算
    dx = circle.center_x - closest_x
    dy = circle.center_y - closest_y
    distance_squared = dx * dx + dy * dy
    
    # 距離が半径以下なら衝突
    return distance_squared <= circle.radius * circle.radius