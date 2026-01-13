import pyxel
from typing import List
from .world import World
import os
import inspect

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

    def load_resource(self, filename: str):
        frame = inspect.stack()[1]
        caller_dir = os.path.dirname(os.path.abspath(frame.filename))
        
        # 絶対パス
        full_path = os.path.join(caller_dir, filename)
        
        # ロード
        if os.path.exists(full_path):
            pyxel.load(full_path)
            print(f"Resource loaded: {full_path}")
        else:
            raise FileNotFoundError(f"Asset not found: {full_path}")