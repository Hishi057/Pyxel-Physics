import pyxel
from typing import List
from .world import World

class App:
    screen_x : int
    screen_y : int
    background_color : int
    worlds : list[World]
    

    def __init__(self,screen_x = 200,screen_y = 200, background_color = 7):
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.background_color = background_color
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
        pyxel.cls(self.background_color)
        for w in self.worlds:
            w.draw()