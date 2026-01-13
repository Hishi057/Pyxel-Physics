from __future__ import annotations
from .geometry import Rect, Ray, intersect_ray_aabb, RaycastHit
    
class Quadtree:
    bounds : Rect # 担当領域
    objects : list[("Collider", Rect)]
    children : list["Quadtree"]
    divided : bool
    level : int
    max_level : int
    capacity : int = 3
    query_count : int = 0 # 手動でリセットする必要があるので注意

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
            if self.level == 0:
                self.objects.append(obj)
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
        
    def query(self, search_aabb, found_list, source_id):
        # 枝切り
        if not self.bounds.intersects(search_aabb):
            return

        for collider, aabb in self.objects:
            # 重複カウントを避けるため
            if source_id > collider.id:
                continue
            Quadtree.query_count += 1
            if aabb.intersects(search_aabb):
                found_list.append(collider)

        for child in self.children:
            child.query(search_aabb, found_list, source_id)

    def query_ray(self, ray: Ray, distance_limit: float):
        best_hit = self._query_lay_local(ray, distance_limit)
        if best_hit:
            distance_limit = best_hit.distance

        if self.divided:
            for distance_near, child in self._get_sorted_children(ray):
                if distance_near > distance_limit:
                    break

                result = child.query_ray(ray, distance_limit)
                
                if result:
                    best_hit = result
                    distance_limit = result.distance
        
        return best_hit

    def _query_lay_local(self, ray : Ray, distance_limit):
        best_hit = None
        for collider, aabb in self.objects:
            hit = collider.intersect_ray(ray)
            if hit and 0 <= hit.distance < distance_limit:
                distance_limit = hit.distance
                best_hit = RaycastHit(collider.parent, hit.distance, hit.point, hit.normal)
        return best_hit
    
    def _get_sorted_children(self, ray : Ray):
        hit_children = []

        for child in self.children:
            hit_info = intersect_ray_aabb(ray, child.bounds)
            
            if hit_info:
                hit_children.append((hit_info.distance, child))
        hit_children.sort(key=lambda pair: pair[0])

        return hit_children