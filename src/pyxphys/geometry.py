from dataclasses import dataclass
@dataclass
class RaycastHit:
    obj : "GameObject"
    distance : float
    point : tuple
    normal : tuple

class Ray:
    # 発射地点
    ox : float
    oy : float
    # 方向ベクトル (正規化)
    dx : float
    dy : float
    # 逆数 (キャッシュ)
    inv_dx : float
    inv_dy : float
    # 方向の符号
    sign_x : int
    sign_y : int
    def __init__(self, ox : float, oy : float, nx : float, ny : float):
        self.ox = ox
        self.oy = oy

        mag = (nx**2 + ny**2)**0.5
        if mag == 0: return None
        self.dx = nx/mag
        self.dy = ny/mag



        self.inv_dx = 1.0 / self.dx if self.dx != 0 else float('inf')
        self.inv_dy = 1.0 / self.dy if self.dy != 0 else float('inf')
        self.sign_x = 1 if self.dx >= 0 else 0
        self.sign_y = 1 if self.dy >= 0 else 0


class Rect:
    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = x, y, w, h

    # 他のRectと重なっているか
    def intersects(self, other):
        return not (other.x > self.x + self.w or
                    other.x + other.w < self.x or
                    other.y > self.y + self.h or
                    other.y + other.h < self.y)

    # 完全に内包しているか
    def contains(self, other_rect):
        return (other_rect.x >= self.x and
                other_rect.x + other_rect.w <= self.x + self.w and
                other_rect.y >= self.y and
                other_rect.y + other_rect.h <= self.y + self.h)

    @property
    def left(self): return self.x
    @property
    def right(self): return self.x + self.w
    @property
    def top(self): return self.y
    @property
    def bottom(self): return self.y + self.h

# スラブ法でRayとRectの衝突判定
def intersect_ray_aabb(ray, rect):
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