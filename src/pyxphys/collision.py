from .utils import distance, clamp
import math
from .spatial import Rect

class Collider:
    parent : "GameObject"
    is_trigger : bool
    aabb : Rect

    def __init__(self, offset_x=0, offset_y=0, tag="", is_trigger = False):
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.tag = tag
        self.parent = None
        self.is_trigger = is_trigger
        self.aabb = Rect(0,0,0,0)

    # ある点がCollisionの中に入っているかどうか返す
    def contains(self, x : float, y : float):
        pass

    # AABBの当たり判定を更新
    def update_aabb(self):
        pass

class CircleCollider(Collider):
    radius : float
    def __init__(self, radius, offset_x=0, offset_y=0, tag="", is_trigger = False):
        super().__init__(offset_x, offset_y, tag, is_trigger)
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

#
# offset を中心に、縦height, 横width の長方形のCollider
#
class BoxCollider(Collider):
    height : float
    width : float
    def __init__(self, width, height, offset_x=0, offset_y=0, tag="", is_trigger = False):
        super().__init__(offset_x, offset_y, tag, is_trigger)
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