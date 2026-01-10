from .utils import distance, clamp
import math

class Collider:
    parent : "GameObject"
    is_trigger : bool

    def __init__(self, offset_x=0, offset_y=0, tag="", is_trigger = False):
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.tag = tag
        self.parent = None
        self.is_trigger = is_trigger

    # ある点がCollisionの中に入っているかどうか返す
    def contains(self, x : float, y : float):
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
    
    def contains(self, x : float, y : float):
        pass


# 2つのColliderの衝突判定
def check_collision(c1, c2):
    if isinstance(c1, CircleCollider) and isinstance(c2, CircleCollider):
        return _check_circle_circle(c1, c2)
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

def _check_box_circle(box, circle):
    """
    矩形と円の衝突判定
    box: BoxCollider（中心が座標の中心）
    circle: CircleCollider（中心が座標の中心）
    """
    
    # 円の中心から矩形の最も近い点を見つける
    closest_x = clamp(circle.center_x, box.center_x - box.width/2, box.center_x + box.width/2)
    closest_y = clamp(circle.center_y, box.center_y - box.height/2, box.center_y + box.height/2)
    
    # 最も近い点と円の中心の距離を計算
    dx = circle.center_x - closest_x
    dy = circle.center_y - closest_y
    distance_squared = dx * dx + dy * dy
    
    # 距離が半径以下なら衝突
    return distance_squared <= circle.radius * circle.radius
    
#
# 衝突時の物理演算
#

# circle, circle
def resolve_circle_circle(circle1, circle2):
    # 1. 法線ベクトル（正規化)
    dx = circle2.center_x - circle1.center_x
    dy = circle2.center_y - circle1.center_y
    dist = math.sqrt(dx**2 + dy**2)
    nx : float
    ny : float
    if dist == 0:
        nx, ny = 0, -1
        depth = circle1.radius + circle2.radius
    else:
        nx = dx / dist
        ny = dy / dist
        depth = (circle1.radius + circle2.radius) - dist

    # 2. 重なっている場合押し出す
    percent = 0.4 # 補正強度
    correction_x = nx * depth * percent
    correction_y = ny * depth * percent

    r = dist - (circle2.radius + circle1.radius)
    if r <= 0:
        if not circle1.parent.IS_FREEZE_POSITION:
            circle1.parent.x -= correction_x
            circle1.parent.y -= correction_y
        if not circle2.parent.IS_FREEZE_POSITION:
            circle2.parent.x += correction_x
            circle2.parent.y += correction_y

    # 3. 相対速度の計算
    v_rel_x = circle2.parent.vx - circle1.parent.vx
    v_rel_y = circle2.parent.vy - circle1.parent.vy

    # 4. 相対速度の法線方向の成分
    v_normal_mag = v_rel_x * nx + v_rel_y * ny

    # すでに離れようとしているならスキップ
    if v_normal_mag > 0:
        return

    # 5. 力積のスカラー量
    e = 0.9
    # 逆質量の計算
    inv_m1 = 1 / circle1.parent.mass if circle1.parent.mass != float('inf') else 0
    inv_m2 = 1 / circle2.parent.mass if circle2.parent.mass != float('inf') else 0
        
    inv_mass_sum = inv_m1 + inv_m2
    if inv_mass_sum == 0: return

    j = -(1 + e) * v_normal_mag / inv_mass_sum

    # 6. 速度の更新
    circle1.parent.vx -= (j * inv_m1) * nx
    circle1.parent.vy -= (j * inv_m1) * ny
    circle2.parent.vx += (j * inv_m2) * nx
    circle2.parent.vy += (j * inv_m2) * ny

# circle, box
def resolve_box_circle(box, circle):
    #  1. box上の「円の中心に最も近い点」を特定して法線ベクトルを計算
    closest_x = clamp(circle.center_x, box.center_x - box.width/2, box.center_x + box.width/2)
    closest_y = clamp(circle.center_y, box.center_y - box.height/2, box.center_y + box.height/2)

    dx = closest_x - circle.center_x
    dy = closest_y - circle.center_y
    dist = math.sqrt(dx**2 + dy**2)
    nx : float
    ny : float
    if dist == 0:
        nx, ny = 0, -1
        dist = 0.0001
        depth = circle.radius
    else:
        nx = dx / dist
        ny = dy / dist
        depth = circle.radius - dist

    # 2. 重なっている場合押し出す
    percent = 0.4 # 補正強度
    correction_x = nx * depth * percent
    correction_y = ny * depth * percent

    r = dist - circle.radius
    if r <= 0:
        if not circle.parent.IS_FREEZE_POSITION:
            circle.parent.x -= correction_x
            circle.parent.y -= correction_y
        if not box.parent.IS_FREEZE_POSITION:
            box.parent.x += correction_x
            box.parent.y += correction_y

    # 3. 相対速度
    v_rel_x = box.parent.vx - circle.parent.vx
    v_rel_y = box.parent.vy - circle.parent.vy

    # 4. 相対速度の法線方向の成分 (スカラー)
    v_normal_mag = v_rel_x * nx + v_rel_y * ny

    # すでに離れようとしているならスキップ
    if v_normal_mag > 0:
        return

    # 力積のスカラー量
    e = 0.9 
    # 5. 逆質量の計算
    inv_m1 = 1 / circle.parent.mass if circle.parent.mass != float('inf') else 0
    inv_m2 = 1 / box.parent.mass if box.parent.mass != float('inf') else 0
        
    inv_mass_sum = inv_m1 + inv_m2
    if inv_mass_sum == 0: return

    j = -(1 + e) * v_normal_mag / inv_mass_sum

    # 6. 速度の更新
    circle.parent.vx -= (j * inv_m1) * nx
    circle.parent.vy -= (j * inv_m1) * ny
    box.parent.vx += (j * inv_m2) * nx
    box.parent.vy += (j * inv_m2) * ny