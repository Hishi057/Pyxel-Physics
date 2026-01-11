from __future__ import annotations

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

class Quadtree:
    bounds : Rect # 担当領域
    objects : list[("Collider", Rect)]
    children : list["Quadtree"]
    divided : bool
    level : int
    max_level : int
    capacity : int = 3

    def __init__(self, bounds : Rect, level = 0, max_level = 10):
        self.bounds = bounds
        self.objects = []
        self.children = []
        self.divided = False
        self.level = level
        self.max_level = max_level
    
    def _split(self):
        if self.level >= self.max_level:
            return False
        if self.divided: 
            return True
        
        x = self.bounds.x
        y = self.bounds.y
        w = self.bounds.w / 2
        h = self.bounds.h / 2
        self.children.append(Quadtree(Rect(x,y,w,h) , level = self.level + 1, max_level = self.max_level))
        self.children.append(Quadtree(Rect(x+w,y,w,h) , level = self.level + 1, max_level = self.max_level))
        self.children.append(Quadtree(Rect(x,y+h,w,h) , level = self.level + 1, max_level = self.max_level))
        self.children.append(Quadtree(Rect(x+w,y+h,w,h) , level = self.level + 1, max_level = self.max_level))
        self.divided = True
        return True

    # obj = pair(collider : Collider, aabb : Rect)
    def insert(self, obj):
        collider, aabb = obj
        # そもそも担当領域内に入っているか
        if not self.bounds.contains(aabb):
            return

        # 分割線を跨いでいたら自分に登録
        x = self.bounds.x
        y = self.bounds.y
        w = self.bounds.w
        h = self.bounds.h
        if ((aabb.x <= x + w/2 and x + w/2 <= aabb.x + aabb.w)
        or (aabb.y <= y + h/2 and y + h/2 <= aabb.y + aabb.h)):
            self.objects.append(obj)
            return
        
        # 跨いでいなければ子に委譲
        if self._split():
            for c in self.children:
                c.insert(obj)
        else:
            # これ以上深くできなかったら仕方ない
            self.objects.append(obj)
        return 
        
    def query(self, search_aabb, found_list):
        # 枝切り
        if not self.bounds.intersects(search_aabb):
            return

        for collider, aabb in self.objects:
            if aabb.intersects(search_aabb):
                found_list.append(collider)

        for child in self.children:
            child.query(search_aabb, found_list)

