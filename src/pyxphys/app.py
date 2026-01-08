import pyxel
from typing import List
from .world import World

class App:
    screen_x : int
    screen_y : int
    worlds : list[World]

    def __init__(self,screen_x,screen_y):
        self.screen_x = screen_x
        self.screen_y = screen_y
        pyxel.init(screen_x, screen_y)
        self.worlds = []
    
    def add_world(self, world : World):
        self.worlds.append(world)
        world.app = self
    
    def run(self):
        pyxel.run(self.update, self.draw)
    
    def update(self):
        for w in self.worlds: 
            w.update_physics()
            
    def draw(self):
        pyxel.cls(7)
        for w in self.worlds:
            w.draw()