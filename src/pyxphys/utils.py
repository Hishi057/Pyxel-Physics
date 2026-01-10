import math

def distance_object(go1, go2):
    return distance(go1.x, go1.y, go2.x, go2.y)

def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) **2)

# クランプ処理
def clamp(c, min_val, max_val):
    return max(min_val, min(c, max_val))