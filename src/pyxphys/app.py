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
    debug_mode : bool
    debug_color : int
    cam_x : float
    cam_y : float
    cam_speed : float

    def __init__(self,screen_x = 200,screen_y = 200, background_color = 7, debug_mode = False, debug_color = pyxel.COLOR_RED):
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.background_color = background_color
        pyxel.init(screen_x, screen_y)
        self.worlds = []
        self.debug_mode = debug_mode
        self.debug_color = debug_color
        self.cam_x = 0
        self.cam_y = 0
        self.cam_speed = 3
    
    def add_world(self, world : World):
        self.worlds.append(world)
        world.app = self
    
    def run(self):
        pyxel.run(self.update, self.draw)
    
    def update(self):
        for w in self.worlds: 
            w.update_physics()
        if self.debug_mode:
            self.update_debug()
    
    def update_debug(self):
        if pyxel.btn(pyxel.KEY_W): self.cam_y -= self.cam_speed
        if pyxel.btn(pyxel.KEY_S): self.cam_y += self.cam_speed
        if pyxel.btn(pyxel.KEY_A): self.cam_x -= self.cam_speed
        if pyxel.btn(pyxel.KEY_D): self.cam_x += self.cam_speed
            
    def draw(self):
        pyxel.camera(self.cam_x, self.cam_y)
        pyxel.cls(self.background_color)
        for w in self.worlds:
            w.draw()
        if self.debug_mode:
            self.draw_debug()

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
    
    def draw_debug(self):
        color = self.debug_color
        pyxel.text(4 + self.cam_x,self.screen_y - 8 - 4 + self.cam_y,"APP DEBUG MODE", color)